"""Local-only bridge: serve the built site + an /ask endpoint backed by `claude -p`
(your Claude *subscription*, the same auth the digester uses — no API key, no cost
beyond your plan's usage). For self-use on your own machine; do NOT expose publicly.

    .venv/bin/python -m harness.ask_server [--port 8765] [--rebuild]

Then open http://localhost:8765/, go to any paper page, and click the floating
'✦ Ask Claude' button. The panel is local-only — the public github.io site shows
just the ChatGPT/Claude deep-link buttons.

Note: answers spend the same weekly subscription session the digests use.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import datetime as dt

from . import config, llm, publish, rag, skills, state

SERVE_DIR = config.SITE_DIR / "_build"
SYSTEM = (
    "You are a precise research assistant answering follow-up questions about one "
    "specific paper. Be concise and technical, ground answers in the provided context, "
    "and say clearly when something cannot be determined from it."
)
_WTRN_SYSTEM = (
    "You are a research reading-list curator. From a set of candidate papers you pick "
    "the few that best repay a busy researcher's limited attention, ordered by what to "
    "read first, with a one-line reason each. Honor the user's stated values and what "
    "they want to avoid."
)
_WTRN_PROMPT = (
    'Topic: "{topic}". From the {n} candidate papers below, recommend the top 5 to read '
    "next, most important first. For each: \"**Title** — one-line reason (what you'll learn "
    '/ why it matters to me)\". Prefer papers that match what I value and skip what I avoid. '
    "Output only the list.\n\n{cards}"
)


def _answer(payload: dict, cfg) -> dict:
    title = (payload.get("title") or "").strip()
    url = (payload.get("url") or "").strip()
    tldr = (payload.get("tldr") or "").strip()
    question = (payload.get("question") or "").strip()
    history = payload.get("history") or []
    if not question:
        return {"error": "empty question"}
    lines = [f'Paper: "{title}"' + (f" ({url})" if url else "")]
    if tldr:
        lines.append(f"TL;DR: {tldr}")
    if history:
        lines.append("\nConversation so far:")
        for m in history[-10:]:
            who = "User" if m.get("role") == "user" else "Assistant"
            lines.append(f'{who}: {m.get("content", "")}')
    lines.append(f"\nUser: {question}\nAssistant:")
    sk = skills.load_skill("followup-qa", {"system": SYSTEM})
    try:
        # allow_tools=False keeps it fast/grounded; wait_on_limit=False so a hit
        # weekly limit returns an error instead of blocking the panel.
        ans = llm.run_claude("\n".join(lines), cfg.digest_model, cfg,
                             system=skills.with_profile(sk.system, cfg),
                             allow_tools=False, wait_on_limit=False)
        return {"answer": ans}
    except llm.LLMError as e:
        return {"error": str(e)}


def _recommend(payload: dict, cfg) -> dict:
    """'What to read next' for a topic — runs the what-to-read-next skill over the
    topic's recent high-impact cards (profile-aware)."""
    slug = (payload.get("topic") or "").strip()
    if not slug:
        return {"error": "no topic"}
    t = cfg.topic(slug)
    name = t.name if t else slug
    with state.connect() as conn:
        cards = rag.cards_for(conn, slug, year=dt.date.today().year, limit=30, order="impact")
        if not cards:
            cards = rag.cards_for(conn, slug, limit=30, order="impact")
    if not cards:
        return {"error": f"no papers tracked for '{slug}' yet"}
    lines = []
    for c in cards:
        v = f" [{c['venue']}]" if c.get("venue") else ""
        tl = " ".join((c.get("tldr") or "").split())[:160]
        lines.append(f"- {c['title']}{v} — {tl}")
    sk = skills.load_skill("what-to-read-next", {"system": _WTRN_SYSTEM, "prompt": _WTRN_PROMPT})
    prompt = sk.prompt.format(topic=name, n=len(cards), cards="\n".join(lines))
    try:
        ans = llm.run_claude(prompt, cfg.digest_model, cfg,
                             system=skills.with_profile(sk.system, cfg),
                             allow_tools=False, wait_on_limit=False)
        return {"answer": ans}
    except llm.LLMError as e:
        return {"error": str(e)}


class Handler(SimpleHTTPRequestHandler):
    cfg = None

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        route = self.path.split("?")[0]
        if route not in ("/ask", "/recommend"):
            self.send_error(404)
            return
        n = int(self.headers.get("Content-Length") or 0)
        try:
            payload = json.loads(self.rfile.read(n) or b"{}")
        except ValueError:
            payload = {}
        result = _recommend(payload, self.cfg) if route == "/recommend" else _answer(payload, self.cfg)
        body = json.dumps(result).encode("utf-8")
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass  # quiet


def _build_html(cfg, rebuild: bool) -> None:
    SERVE_DIR.mkdir(parents=True, exist_ok=True)
    cfgyml = config.SITE_DIR / "mkdocs.yml"
    if rebuild or not cfgyml.exists():
        with state.connect() as conn:
            publish.build_site(conn, cfg)   # regenerate docs + mkdocs.yml (no deploy)
    subprocess.run([sys.executable, "-m", "mkdocs", "build", "-f", str(cfgyml),
                    "-d", str(SERVE_DIR), "--quiet"], check=True)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Local Ask-Claude bridge for the paper digest site")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--rebuild", action="store_true",
                    help="regenerate the site docs from the DB before serving")
    args = ap.parse_args(argv)
    cfg = config.load_config()
    print("building site HTML…", flush=True)
    _build_html(cfg, args.rebuild)
    Handler.cfg = cfg
    srv = ThreadingHTTPServer(("127.0.0.1", args.port), partial(Handler, directory=str(SERVE_DIR)))
    print(f"\n  ✦ Ask-Claude bridge ready  →  http://localhost:{args.port}/", flush=True)
    print("    Open a paper page, click '✦ Ask Claude' (uses your subscription). Ctrl-C to stop.\n",
          flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
