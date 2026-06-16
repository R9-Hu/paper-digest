(function () {
  function mark() {
    document.querySelectorAll('.md-content a[href*="papers/"]').forEach(function (a) {
      a.target = '_blank';
      a.rel = 'noopener';
    });
  }
  if (document.readyState !== 'loading') mark();
  else document.addEventListener('DOMContentLoaded', mark);
})();
