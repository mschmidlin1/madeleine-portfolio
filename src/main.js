(function () {
  const THEME_KEY = "theme";
  const navToggle = document.querySelector(".nav-toggle");
  const siteNav = document.querySelector("#site-nav");
  const navLinks = document.querySelectorAll("#site-nav a");
  const yearEl = document.querySelector("#year");
  const themeToggle = document.querySelector(".theme-toggle");
  const colorSchemeQuery = window.matchMedia("(prefers-color-scheme: dark)");

  if (yearEl) {
    yearEl.textContent = String(new Date().getFullYear());
  }

  function getSystemTheme() {
    return colorSchemeQuery.matches ? "dark" : "light";
  }

  function getEffectiveTheme() {
    const saved = document.documentElement.getAttribute("data-theme");
    if (saved === "light" || saved === "dark") {
      return saved;
    }
    return getSystemTheme();
  }

  function updateThemeToggle() {
    if (!themeToggle) return;
    const isDark = getEffectiveTheme() === "dark";
    themeToggle.setAttribute(
      "aria-label",
      isDark ? "Switch to light mode" : "Switch to dark mode"
    );
  }

  function setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(THEME_KEY, theme);
    updateThemeToggle();
  }

  if (themeToggle) {
    updateThemeToggle();

    themeToggle.addEventListener("click", () => {
      setTheme(getEffectiveTheme() === "dark" ? "light" : "dark");
    });

    colorSchemeQuery.addEventListener("change", () => {
      if (!localStorage.getItem(THEME_KEY)) {
        updateThemeToggle();
      }
    });
  }

  function closeNav() {
    if (!navToggle || !siteNav) return;
    siteNav.classList.remove("is-open");
    navToggle.setAttribute("aria-expanded", "false");
    navToggle.setAttribute("aria-label", "Open menu");
  }

  if (navToggle && siteNav) {
    navToggle.addEventListener("click", () => {
      const isOpen = siteNav.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
      navToggle.setAttribute("aria-label", isOpen ? "Close menu" : "Open menu");
    });
  }

  navLinks.forEach((link) => {
    link.addEventListener("click", closeNav);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeNav();
    }
  });
})();
