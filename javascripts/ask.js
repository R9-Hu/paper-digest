(function () {
  var h = location.hostname;
  if (h !== 'localhost' && h !== '127.0.0.1') return;     // local bridge only
  if (!/\/papers\//.test(location.pathname)) return;     // paper pages only

  function ctx() {
    var h1 = document.querySelector('.md-content h1') || document.querySelector('h1');
    var title = h1 ? h1.textContent.trim() : document.title;
    var tldr = '', hs = document.querySelectorAll('.md-content h2');
    for (var i = 0; i < hs.length; i++) {
      if (/tl;?dr/i.test(hs[i].textContent)) {
        var el = hs[i].nextElementSibling, buf = [];
        while (el && el.tagName !== 'H2') { if (el.textContent) buf.push(el.textContent.trim()); el = el.nextElementSibling; }
        tldr = buf.join(' '); break;
      }
    }
    return { title: title, url: location.href, tldr: tldr.slice(0, 1200) };
  }

  var c = ctx(), history = [];
  var fab = document.createElement('button'); fab.id = 'ask-fab'; fab.textContent = '✦ Ask Claude';
  var panel = document.createElement('div'); panel.id = 'ask-panel'; panel.style.display = 'none';
  panel.innerHTML =
    '<div id="ask-head">✦ Ask Claude <span style="opacity:.65;font-weight:400">· local · your subscription</span><button id="ask-x" title="close">×</button></div>' +
    '<div id="ask-msgs"></div>' +
    '<div id="ask-actions"><button id="ask-next" type="button">📋 What to read next</button></div>' +
    '<form id="ask-form"><textarea id="ask-in" rows="2" placeholder="Ask a follow-up about this paper…"></textarea><button id="ask-send">Send</button></form>';
  document.body.appendChild(fab); document.body.appendChild(panel);
  var msgs = panel.querySelector('#ask-msgs');

  function add(role, text) {
    var d = document.createElement('div'); d.className = 'ask-msg ask-' + role;
    d.textContent = text; msgs.appendChild(d); msgs.scrollTop = msgs.scrollHeight; return d;
  }
  fab.onclick = function () { panel.style.display = 'flex'; fab.style.display = 'none'; panel.querySelector('#ask-in').focus(); };
  panel.querySelector('#ask-x').onclick = function () { panel.style.display = 'none'; fab.style.display = 'block'; };

  panel.querySelector('#ask-form').onsubmit = function (e) {
    e.preventDefault();
    var inp = panel.querySelector('#ask-in'), q = inp.value.trim(); if (!q) return;
    inp.value = ''; add('user', q);
    var pending = add('assistant', '…'), btn = panel.querySelector('#ask-send'); btn.disabled = true;
    fetch('/ask', { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: c.title, url: c.url, tldr: c.tldr, history: history, question: q }) })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        pending.textContent = j.answer || ('\u26a0 ' + (j.error || 'no response'));
        if (j.answer) { history.push({ role: 'user', content: q }); history.push({ role: 'assistant', content: j.answer }); }
      })
      .catch(function (err) { pending.textContent = '\u26a0 ' + err; })
      .finally(function () { btn.disabled = false; });
  };

  function topicSlug() { return location.pathname.replace(/^\/+/, '').split('/')[0] || ''; }
  panel.querySelector('#ask-next').onclick = function () {
    panel.style.display = 'flex'; fab.style.display = 'none';
    var pending = add('assistant', '…finding what to read next');
    var b = panel.querySelector('#ask-next'); b.disabled = true;
    fetch('/recommend', { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic: topicSlug() }) })
      .then(function (r) { return r.json(); })
      .then(function (j) { pending.textContent = j.answer || ('\u26a0 ' + (j.error || 'no response')); })
      .catch(function (err) { pending.textContent = '\u26a0 ' + err; })
      .finally(function () { b.disabled = false; });
  };

  var css = document.createElement('style');
  css.textContent =
    '#ask-fab{position:fixed;right:18px;bottom:18px;z-index:1000;background:#d97757;color:#fff;border:none;border-radius:24px;padding:.6rem 1rem;font-weight:600;cursor:pointer;box-shadow:0 2px 10px rgba(0,0,0,.25)}' +
    '#ask-panel{position:fixed;right:18px;bottom:18px;z-index:1001;width:370px;max-width:92vw;height:500px;max-height:80vh;display:flex;flex-direction:column;background:var(--md-default-bg-color,#fff);border:1px solid rgba(0,0,0,.15);border-radius:12px;box-shadow:0 10px 34px rgba(0,0,0,.32);overflow:hidden}' +
    '#ask-head{padding:.6rem .8rem;background:#d97757;color:#fff;font-weight:600;display:flex;align-items:center;gap:.35rem;font-size:.9rem}' +
    '#ask-x{margin-left:auto;background:none;border:none;color:#fff;font-size:1.25rem;cursor:pointer;line-height:1}' +
    '#ask-msgs{flex:1;overflow-y:auto;padding:.6rem;font-size:.85rem;display:flex;flex-direction:column;gap:.5rem}' +
    '.ask-msg{padding:.5rem .7rem;border-radius:10px;white-space:pre-wrap;line-height:1.45}' +
    '.ask-user{align-self:flex-end;background:#d97757;color:#fff;max-width:85%}' +
    '.ask-assistant{align-self:flex-start;background:rgba(127,127,127,.16);max-width:96%}' +
    '#ask-actions{padding:.4rem .5rem 0}' +
    '#ask-next{width:100%;background:rgba(217,119,87,.12);color:#d97757;border:1px solid rgba(217,119,87,.5);border-radius:8px;padding:.4rem;font-weight:600;cursor:pointer;font-size:.8rem}' +
    '#ask-form{display:flex;gap:.4rem;padding:.5rem;border-top:1px solid rgba(127,127,127,.25)}' +
    '#ask-in{flex:1;resize:none;border:1px solid rgba(127,127,127,.35);border-radius:8px;padding:.4rem;font:inherit;background:transparent;color:inherit}' +
    '#ask-send{background:#d97757;color:#fff;border:none;border-radius:8px;padding:0 .9rem;font-weight:600;cursor:pointer}';
  document.head.appendChild(css);
})();
