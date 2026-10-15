/* ==========================================================================
   INTERRUTTORE MODALITA' DEMO - unico punto di controllo.
   true  = banner, filigrana, prefisso [DEMO] nel titolo e noindex attivi.
   false = la pagina torna "normale" (vedi README per i passi completi,
           inclusi robots.txt e la direttiva noindex scritta nell'HTML).
   Il link a Tramontis nel footer NON dipende da questo interruttore.
   ========================================================================== */
(function () {
  var DEMO = true;

  var root = document.documentElement;
  root.classList.add("js");
  if (DEMO) { root.setAttribute("data-demo", ""); return; }

  document.addEventListener("DOMContentLoaded", function () {
    document.title = document.title.replace(/^\[DEMO\]\s*/, "");
    var robots = document.querySelector('meta[name="robots"]');
    if (robots) robots.remove();
    var banner = document.querySelector(".demo-banner");
    if (banner) banner.remove();
  });
})();
