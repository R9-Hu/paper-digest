(function () {
  function mark() {
    // Any link to an individual paper page (content tables/digests AND the
    // 'Key papers' entries in the left nav). 'papers-list' is left as-is.
    document.querySelectorAll('a[href*="papers/"]').forEach(function (a) {
      a.target = '_blank';
      a.rel = 'noopener';
    });
  }
  if (document.readyState !== 'loading') mark();
  else document.addEventListener('DOMContentLoaded', mark);
})();
