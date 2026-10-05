/* Interacciones minimas del sitio (todo el estilo vive en base.css). */
(function () {
  "use strict";

  const navbar = document.getElementById("navbar");
  const toggle = document.querySelector("[data-nav-toggle]");
  const nav = document.querySelector(".nav");

  /* --- Menu movil ------------------------------------------------------ */
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      const abierto = nav.classList.toggle("abierto");
      toggle.classList.toggle("abierto", abierto);
      toggle.setAttribute("aria-expanded", abierto ? "true" : "false");
    });

    nav.addEventListener("click", function (evento) {
      if (evento.target.closest("a")) {
        nav.classList.remove("abierto");
        toggle.classList.remove("abierto");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* --- Sombra de la navbar al hacer scroll ---------------------------- */
  if (navbar) {
    const alScroll = function () {
      navbar.classList.toggle("con-fijo", window.scrollY > 8);
    };
    alScroll();
    window.addEventListener("scroll", alScroll, { passive: true });
  }

  /* --- Confirmacion al cerrar sesion ----------------------------------- */
  document.querySelectorAll('form[action*="logout"]').forEach(function (formulario) {
    formulario.addEventListener("submit", function (evento) {
      if (!window.confirm("Cerrar sesion ahora?")) {
        evento.preventDefault();
      }
    });
  });
})();
