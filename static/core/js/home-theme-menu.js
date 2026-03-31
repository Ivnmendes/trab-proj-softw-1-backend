(function () {
  var themeApi = window.PublicTheme;
  if (!themeApi) {
    return;
  }

  function paint(theme) {
    var icon = document.getElementById("theme-trigger-icon");
    var options = document.querySelectorAll("[data-theme-option]");
    var iconMap = { light: "light_mode", dark: "dark_mode", auto: "computer" };
    if (icon) {
      icon.textContent = iconMap[theme] || "computer";
    }
    options.forEach(function (option) {
      option.classList.toggle("active", option.getAttribute("data-theme-option") === theme);
    });
  }

  function setTheme(theme) {
    var normalized = themeApi.persistTheme(theme);
    themeApi.applyTheme(normalized);
    paint(normalized);
  }

  var trigger = document.getElementById("theme-trigger");
  var menu = document.getElementById("theme-menu");
  if (!trigger || !menu) {
    return;
  }

  var currentTheme = themeApi.getStoredTheme();
  paint(currentTheme);

  trigger.addEventListener("click", function () {
    menu.classList.toggle("open");
  });

  document.querySelectorAll("[data-theme-option]").forEach(function (option) {
    option.addEventListener("click", function () {
      var selectedTheme = option.getAttribute("data-theme-option");
      setTheme(selectedTheme);
      menu.classList.remove("open");
    });
  });

  document.addEventListener("click", function (event) {
    if (!menu.contains(event.target) && !trigger.contains(event.target)) {
      menu.classList.remove("open");
    }
  });
})();
