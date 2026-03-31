(function () {
  function getCookie(name) {
    var nameEq = name + "=";
    var parts = document.cookie ? document.cookie.split(";") : [];
    for (var i = 0; i < parts.length; i++) {
      var cookie = parts[i].trim();
      if (cookie.indexOf(nameEq) === 0) {
        return decodeURIComponent(cookie.substring(nameEq.length));
      }
    }
    return null;
  }

  function normalizeTheme(value) {
    if (!value) {
      return "auto";
    }
    var normalized = String(value).replace(/['"]/g, "").trim().toLowerCase();
    if (normalized === "dark" || normalized === "light" || normalized === "auto") {
      return normalized;
    }
    return "auto";
  }

  function resolveTheme(theme) {
    if (theme === "dark" || theme === "light") {
      return theme;
    }
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function applyTheme(theme) {
    var root = document.documentElement;
    var resolved = resolveTheme(theme);
    root.setAttribute("data-theme", resolved);
    root.style.colorScheme = resolved;
  }

  function getStoredTheme() {
    return normalizeTheme(getCookie("adminTheme") || localStorage.getItem("adminTheme"));
  }

  function persistTheme(theme) {
    var normalized = normalizeTheme(theme);
    var persisted = '"' + normalized + '"';
    localStorage.setItem("adminTheme", persisted);
    document.cookie = "adminTheme=" + encodeURIComponent(persisted) + "; path=/; max-age=31536000; samesite=lax";
    return normalized;
  }

  window.PublicTheme = {
    getCookie: getCookie,
    normalizeTheme: normalizeTheme,
    resolveTheme: resolveTheme,
    applyTheme: applyTheme,
    getStoredTheme: getStoredTheme,
    persistTheme: persistTheme,
  };

  applyTheme(getStoredTheme());
})();
