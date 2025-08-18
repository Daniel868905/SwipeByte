(() => {
  try { new URL('/'); }
  catch {
    const _URL = URL;
    // Patch only the 1-arg relative form; keep normal behavior otherwise.
    // eslint-disable-next-line no-global-assign
    URL = function(u, b) {
      if (arguments.length === 1 && typeof u === 'string' && u.startsWith('/')) {
        return new _URL(u, window.location.origin);
      }
      return new _URL(u, b);
    };
    URL.prototype = _URL.prototype;
  }
})();
