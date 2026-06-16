"""Local paper-card cache + hybrid retrieval (RAG) for the digest harness.

Goal: never re-send full papers to Claude for synthesis. Each paper is reduced
ONCE (at digest time) to a compact "card" — title · venue · year · impact ·
tags · TL;DR. Cards are cached here and are the only thing fed to downstream
LLM steps (monthly/yearly trend synthesis, related-paper lookup, etc.).

Retrieval is hybrid:
  * SQLite FTS5 (BM25) — keyword recall, always available, offline, instant.
  * model2vec static embeddings — semantic re-rank, when the (numpy-only,
    torch-free) model is installed. Degrades gracefully to FTS5-only.

Both indexes live in the same papers.db:
  card      — structured card + normalized embedding (BLOB) + a content hash
  card_fts  — FTS5 virtual table over the searchable card text
"""
from __future__ import annotations

import hashlib
import logging
import re
import struct

from . import config, state

log = logging.getLogger("harness.rag")

EMBED_MODEL = "minishlab/potion-base-8M"   # static embeddings: numpy-only, no torch
_MODEL = None          # lazy singleton; False once we know it's unavailable
_TAG_RE = re.compile(r"#([A-Za-z][\w-]+)")


# --------------------------------------------------------------------------- #
# Embeddings (optional)
# --------------------------------------------------------------------------- #
def _model():
    global _MODEL
    if _MODEL is None:
        try:
            from model2vec import StaticModel
            _MODEL = StaticModel.from_pretrained(EMBED_MODEL)
            log.info("rag: embeddings enabled (%s)", EMBED_MODEL)
        except Exception as e:  # noqa: BLE001 — missing dep, no network, etc.
            log.info("rag: embeddings unavailable (%s); FTS5-only", type(e).__name__)
            _MODEL = False
    return _MODEL or None


def embed_available() -> bool:
    return _model() is not None


def embed(texts: list[str]):
    """Return an L2-normalized float32 ndarray (n, dim), or None if unavailable."""
    m = _model()
    if m is None or not texts:
        return None
    try:
        import numpy as np
        v = np.asarray(m.encode(texts), dtype="float32")
        v /= (np.linalg.norm(v, axis=1, keepdims=True) + 1e-9)
        return v
    except Exception as e:  # noqa: BLE001
        log.warning("rag: embed failed: %s", e)
        return None


def _pack(vec) -> bytes:
    return struct.pack(f"<{len(vec)}f", *vec.tolist())


def _unpack(blob: bytes):
    import numpy as np
    return np.frombuffer(blob, dtype="<f4")


# --------------------------------------------------------------------------- #
# Schema + card construction
# --------------------------------------------------------------------------- #
def _ensure_tables(conn) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS card (
            canonical_id TEXT, topic_slug TEXT, year INTEGER, published TEXT, title TEXT,
            venue TEXT, citations INTEGER, tldr TEXT, tags TEXT, text TEXT,
            vec BLOB, text_hash TEXT,
            PRIMARY KEY (canonical_id, topic_slug)
        )""")
    conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS card_fts USING fts5("
                 "canonical_id UNINDEXED, topic_slug UNINDEXED, year UNINDEXED, text)")


def _parse_digest(row) -> tuple[str, str]:
    """Parse (tl;dr, tags) from the paper's digest file once — so the card holds
    the compact summary even for older papers digested before TL;DR was cached."""
    path = config.ROOT / (row["digest_path"] or "")
    if not path.exists():
        return "", ""
    try:
        txt = path.read_text(encoding="utf-8")
    except OSError:
        return "", ""
    mt = re.search(r"(?ims)^##\s*TL;DR\s*\n(.+?)(?=^##\s|\Z)", txt)
    tldr = " ".join(mt.group(1).split()) if mt else ""
    mg = re.search(r"(?ims)^##\s*Tags\s*\n(.+?)(?=^##\s|\Z)", txt)
    tags = " ".join(dict.fromkeys(t.lower() for t in _TAG_RE.findall(mg.group(1) if mg else "")))
    return tldr, tags


def _card_text(title: str, venue: str, year, tldr: str, tags: str) -> str:
    bits = [title or ""]
    if venue:
        bits.append(str(venue))
    if year:
        bits.append(str(year))
    if tldr:
        bits.append(tldr)
    if tags:
        bits.append(tags)
    return ". ".join(b for b in bits if b).strip()


def _hash(*parts) -> str:
    return hashlib.sha1("␟".join(str(p or "") for p in parts).encode()).hexdigest()


# --------------------------------------------------------------------------- #
# Index build (incremental)
# --------------------------------------------------------------------------- #
def build_index(conn, embed_new: bool = True) -> dict:
    """(Re)build the card cache + indexes from the current digested corpus.

    Incremental: a card is re-embedded only when its title/TL;DR changed; cards
    for papers that were dropped/compacted-away are removed (so retrieval never
    surfaces stale papers — matching the site/Obsidian cleanup)."""
    _ensure_tables(conn)
    rows = conn.execute(
        """SELECT canonical_id, topic_slug, year, title, venue, tldr, digest_path, published
           FROM papers WHERE digest_status IN ('digested','compacted')"""
    ).fetchall()

    current = {(r["canonical_id"], r["topic_slug"]) for r in rows}
    existing = {(r["canonical_id"], r["topic_slug"]): r["text_hash"]
                for r in conn.execute("SELECT canonical_id, topic_slug, text_hash FROM card")}

    # Drop cards whose papers are gone.
    removed = 0
    for cid, slug in set(existing) - current:
        conn.execute("DELETE FROM card WHERE canonical_id=? AND topic_slug=?", (cid, slug))
        conn.execute("DELETE FROM card_fts WHERE canonical_id=? AND topic_slug=?", (cid, slug))
        removed += 1

    impacts = {}
    try:
        from .sources import impact
        impacts = impact.lookup(conn, [r["canonical_id"] for r in rows])
    except Exception as e:  # noqa: BLE001
        log.warning("rag: impact lookup skipped: %s", e)

    pending = []   # (key, fields...) needing (re)embedding
    fresh = 0
    for r in rows:
        key = (r["canonical_id"], r["topic_slug"])
        file_tldr, tags = _parse_digest(r)
        tldr = r["tldr"] or file_tldr
        text = _card_text(r["title"], r["venue"], r["year"], tldr, tags)
        h = _hash(r["title"], tldr, tags)
        cites = impacts.get(r["canonical_id"], (0, 0))[0]
        if existing.get(key) == h:
            # unchanged text — just refresh the (cheap) citation count
            conn.execute("UPDATE card SET citations=? WHERE canonical_id=? AND topic_slug=?",
                         (cites, *key))
            continue
        fresh += 1
        conn.execute("DELETE FROM card_fts WHERE canonical_id=? AND topic_slug=?", key)
        conn.execute("INSERT INTO card_fts (canonical_id, topic_slug, year, text) VALUES (?,?,?,?)",
                     (r["canonical_id"], r["topic_slug"], r["year"], text))
        conn.execute(
            """INSERT OR REPLACE INTO card
               (canonical_id, topic_slug, year, published, title, venue, citations, tldr, tags, text, vec, text_hash)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (r["canonical_id"], r["topic_slug"], r["year"], r["published"], r["title"], r["venue"],
             cites, tldr, tags, text, None, h),
        )
        pending.append((key, text))
    conn.commit()

    embedded = 0
    if embed_new and pending and embed_available():
        vecs = embed([t for _, t in pending])
        if vecs is not None:
            for (key, _), v in zip(pending, vecs):
                conn.execute("UPDATE card SET vec=? WHERE canonical_id=? AND topic_slug=?",
                             (_pack(v), *key))
                embedded += 1
            conn.commit()

    log.info("rag: index built — %d cards (%d new/changed, %d embedded, %d removed)",
             len(current), fresh, embedded, removed)
    return {"cards": len(current), "changed": fresh, "embedded": embedded, "removed": removed}


# --------------------------------------------------------------------------- #
# Retrieval
# --------------------------------------------------------------------------- #
def _fts_query(query: str) -> str:
    toks = re.findall(r"[A-Za-z0-9][A-Za-z0-9+\-]*", query or "")
    return " OR ".join(f'"{t}"' for t in toks) if toks else ""


def _scope_sql(topic_slug, year):
    where, args = [], []
    if topic_slug:
        where.append("topic_slug=?"); args.append(topic_slug)
    if year:
        where.append("year=?"); args.append(year)
    return (" WHERE " + " AND ".join(where) if where else ""), args


def _row_to_card(r) -> dict:
    keys = r.keys() if hasattr(r, "keys") else []
    return {"canonical_id": r["canonical_id"], "topic_slug": r["topic_slug"],
            "year": r["year"], "published": (r["published"] if "published" in keys else None),
            "title": r["title"], "venue": r["venue"],
            "citations": r["citations"], "tldr": r["tldr"], "tags": r["tags"]}


def retrieve(conn, query: str, topic_slug: str | None = None, year: int | None = None,
             k: int = 12, candidates: int = 60, alpha: float = 0.5) -> list[dict]:
    """Hybrid retrieval: FTS5 (BM25) recall ∪ vector recall, blended re-rank.

    `alpha` weights the semantic (cosine) score vs the lexical (BM25) score.
    Returns up to `k` compact cards, most relevant first."""
    _ensure_tables(conn)
    scope_sql, scope_args = _scope_sql(topic_slug, year)

    # (a) Lexical candidates via FTS5.
    lex: dict[tuple, float] = {}
    fq = _fts_query(query)
    if fq:
        sql = ("SELECT canonical_id, topic_slug, bm25(card_fts) AS b FROM card_fts "
               "WHERE card_fts MATCH ?")
        args = [fq]
        if topic_slug:
            sql += " AND topic_slug=?"; args.append(topic_slug)
        if year:
            sql += " AND year=?"; args.append(year)
        sql += " ORDER BY b LIMIT ?"; args.append(candidates)
        for r in conn.execute(sql, args):
            lex[(r["canonical_id"], r["topic_slug"])] = -float(r["b"])  # higher = better
    lo, hi = (min(lex.values()), max(lex.values())) if lex else (0.0, 1.0)
    lex_norm = {key: (v - lo) / (hi - lo) if hi > lo else 1.0 for key, v in lex.items()}

    # (b) Semantic candidates via embeddings (catches synonym-only matches).
    sem: dict[tuple, float] = {}
    qv = embed([query])
    if qv is not None:
        import numpy as np
        rows = conn.execute(f"SELECT canonical_id, topic_slug, vec FROM card{scope_sql}",
                            scope_args).fetchall()
        keys, mat = [], []
        for r in rows:
            if r["vec"]:
                keys.append((r["canonical_id"], r["topic_slug"]))
                mat.append(_unpack(r["vec"]))
        if mat:
            sims = np.asarray(mat) @ qv[0]
            order = sims.argsort()[::-1][:candidates]
            for i in order:
                sem[keys[i]] = float((sims[i] + 1.0) / 2.0)   # cosine [-1,1] -> [0,1]

    if not lex_norm and not sem:
        return []
    keys = set(lex_norm) | set(sem)
    blended = {key: alpha * sem.get(key, 0.0) + (1 - alpha) * lex_norm.get(key, 0.0)
               for key in keys}
    top = sorted(keys, key=lambda key: blended[key], reverse=True)[:k]

    out = []
    for cid, slug in top:
        r = conn.execute("SELECT * FROM card WHERE canonical_id=? AND topic_slug=?",
                         (cid, slug)).fetchone()
        if r:
            card = _row_to_card(r)
            card["score"] = round(blended[(cid, slug)], 4)
            out.append(card)
    return out


def cards_for(conn, topic_slug: str, year: int | None = None, limit: int | None = None,
              order: str = "impact") -> list[dict]:
    """Compact cards for a topic (no query) — the corpus for trend synthesis.

    `order='impact'` ranks by citations then recency (most important first);
    `order='recent'` by date. This is what we send to Claude instead of papers."""
    _ensure_tables(conn)
    scope_sql, args = _scope_sql(topic_slug, year)
    order_sql = ("ORDER BY citations DESC, published DESC" if order == "impact"
                 else "ORDER BY published DESC")
    sql = f"SELECT * FROM card{scope_sql} {order_sql}"
    if limit:
        sql += f" LIMIT {int(limit)}"
    return [_row_to_card(r) for r in conn.execute(sql, args)]
