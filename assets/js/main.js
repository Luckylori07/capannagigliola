/* Capanna Gigliola - comportamento del sito (vanilla JS, nessuna dipendenza) */
(function () {
  "use strict";
  var doc = document;
  var $ = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- Header: solido dopo lo scroll ---- */
  var header = $(".site-header");
  var hasHero = !!$(".hero, .page-hero");
  function onScroll() {
    if (!header) return;
    header.classList.toggle("is-solid", !hasHero || window.scrollY > 40);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ---- Menu mobile ---- */
  var toggle = $(".menu-toggle");
  var panel = $("#nav-mobile");
  function setMenu(open) {
    if (!toggle || !panel) return;
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Chiudi il menu di navigazione" : "Apri il menu di navigazione");
    doc.body.classList.toggle("menu-open", open);
    if (open) { panel.removeAttribute("inert"); } else { panel.setAttribute("inert", ""); }
  }
  if (toggle && panel) {
    panel.setAttribute("inert", "");
    toggle.addEventListener("click", function () { setMenu(toggle.getAttribute("aria-expanded") !== "true"); });
    $$("a", panel).forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });
    doc.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && doc.body.classList.contains("menu-open")) { setMenu(false); toggle.focus(); }
    });
    window.matchMedia("(min-width: 960px)").addEventListener("change", function (m) { if (m.matches) setMenu(false); });
  }

  /* ---- Reveal allo scroll e linea del tempo ---- */
  var revealEls = $$("[data-reveal], .timeline");
  if ("IntersectionObserver" in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---- Lightbox accessibile (dialog nativo) ---- */
  var lbItems = [], lbIndex = 0, lbOpener = null, dlg = null;
  var icons = {
    close: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 5l14 14M19 5L5 19"/></svg>',
    prev: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>',
    next: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>'
  };
  function buildLightbox() {
    dlg = doc.createElement("dialog");
    dlg.className = "lightbox";
    dlg.setAttribute("aria-label", "Galleria fotografica");
    dlg.innerHTML =
      '<button type="button" class="lb-btn lb-close" aria-label="Chiudi la foto">' + icons.close + "</button>" +
      '<button type="button" class="lb-btn lb-prev" aria-label="Foto precedente">' + icons.prev + "</button>" +
      '<button type="button" class="lb-btn lb-next" aria-label="Foto successiva">' + icons.next + "</button>" +
      '<div class="lb-stage"><img alt=""></div>' +
      '<div class="lb-bar"><span class="lb-cap"></span><span class="lb-count" aria-live="polite"></span></div>';
    doc.body.appendChild(dlg);
    $(".lb-close", dlg).addEventListener("click", function () { dlg.close(); });
    $(".lb-prev", dlg).addEventListener("click", function () { step(-1); });
    $(".lb-next", dlg).addEventListener("click", function () { step(1); });
    dlg.addEventListener("click", function (e) {
      if (e.target === dlg || e.target.classList.contains("lb-stage")) dlg.close();
    });
    dlg.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") { e.preventDefault(); step(-1); }
      if (e.key === "ArrowRight") { e.preventDefault(); step(1); }
    });
    dlg.addEventListener("close", function () {
      doc.body.style.overflow = "";
      if (lbOpener && doc.contains(lbOpener)) lbOpener.focus();
    });
  }
  function show(i) {
    lbIndex = (i + lbItems.length) % lbItems.length;
    var it = lbItems[lbIndex], img = $(".lb-stage img", dlg), src = $("img", it);
    var fresh = img.cloneNode(false);
    fresh.src = src.currentSrc || src.src;
    fresh.alt = src.alt;
    img.replaceWith(fresh);
    $(".lb-cap", dlg).textContent = src.alt;
    $(".lb-count", dlg).textContent = "Foto " + (lbIndex + 1) + " di " + lbItems.length;
  }
  function step(d) { show(lbIndex + d); }
  function openLightbox(item) {
    var group = item.closest("[data-lb-group]");
    lbItems = $$("[data-lb]", group).filter(function (el) { return !el.classList.contains("is-hidden"); });
    lbOpener = item;
    if (!dlg) buildLightbox();
    show(lbItems.indexOf(item));
    var multi = lbItems.length > 1;
    $(".lb-prev", dlg).hidden = !multi; $(".lb-next", dlg).hidden = !multi;
    doc.body.style.overflow = "hidden";
    if (typeof dlg.showModal === "function") dlg.showModal(); else dlg.setAttribute("open", "");
    $(".lb-close", dlg).focus();
  }
  $$("[data-lb]").forEach(function (el) {
    el.addEventListener("click", function () { openLightbox(el); });
  });

  /* ---- Filtri galleria ---- */
  var filterBar = $(".filters");
  if (filterBar) {
    var live = $("#gallery-count");
    $$(".filter-btn", filterBar).forEach(function (btn) {
      btn.addEventListener("click", function () {
        $$(".filter-btn", filterBar).forEach(function (b) { b.setAttribute("aria-pressed", String(b === btn)); });
        var cat = btn.dataset.filter, n = 0;
        $$(".g-item").forEach(function (it) {
          var on = cat === "tutte" || it.dataset.cat.split(" ").indexOf(cat) > -1;
          it.classList.toggle("is-hidden", !on);
          if (on) n++;
        });
        if (live) live.textContent = n + (n === 1 ? " fotografia" : " fotografie") + " in “" + btn.textContent.trim() + "”";
      });
    });
  }

  /* ---- Menu da data/menu.json ---- */
  var menuRoot = $("#menu-root");
  if (menuRoot) loadMenu(menuRoot);

  function el(tag, cls, text) {
    var n = doc.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function priceText(p) { return "€ " + p; }
  function dishNode(d) {
    var li = el("li", "dish");
    li.appendChild(el("h4", "dish-name", d.name));
    if (d.price) li.appendChild(el("span", "dish-price", priceText(d.price)));
    if (d.desc) li.appendChild(el("p", "dish-desc", d.desc));
    if (d.variants) {
      var v = el("div", "dish-variants");
      d.variants.forEach(function (x) {
        var s = el("span", null, x.label + " ");
        s.appendChild(el("b", null, priceText(x.price)));
        v.appendChild(s);
      });
      li.appendChild(v);
    }
    return li;
  }
  function renderMenu(data, root) {
    root.textContent = "";
    var nav = $("#menu-nav-list");
    if (nav) nav.textContent = "";
    var photos = data.photos || {};
    data.categories.forEach(function (cat) {
      var sec = el("section", "menu-cat");
      sec.id = cat.id;
      sec.setAttribute("aria-labelledby", cat.id + "-t");
      var head = el("div", "menu-cat-head");
      var h = el("h2", null, cat.title); h.id = cat.id + "-t";
      head.appendChild(h);
      if (cat.intro) head.appendChild(el("p", null, cat.intro));
      if (photos[cat.id]) {
        var fig = el("div", "menu-cat-photo"), img = el("img");
        img.src = photos[cat.id].src; img.alt = photos[cat.id].alt;
        img.width = photos[cat.id].w; img.height = photos[cat.id].h; img.loading = "lazy";
        fig.appendChild(img); head.appendChild(fig);
      }
      var body = el("div", "menu-cat-body");
      (cat.groups || [{ items: cat.items }]).forEach(function (g) {
        if (g.title) body.appendChild(el("h3", "menu-sub", g.title));
        var ul = el("ul");
        g.items.forEach(function (d) { ul.appendChild(dishNode(d)); });
        body.appendChild(ul);
      });
      sec.appendChild(head); sec.appendChild(body);
      root.appendChild(sec);
      if (nav) {
        var li = el("li"), a = el("a", null, cat.title);
        a.href = "#" + cat.id; li.appendChild(a); nav.appendChild(li);
      }
    });
    spy();
    if (location.hash) {
      var t = doc.getElementById(decodeURIComponent(location.hash.slice(1)));
      if (t) t.scrollIntoView();
    }
  }
  function spy() {
    var links = $$("#menu-nav-list a");
    if (!links.length || !("IntersectionObserver" in window)) return;
    var map = {};
    links.forEach(function (a) { map[a.hash.slice(1)] = a; });
    var so = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          links.forEach(function (a) { a.classList.remove("is-active"); a.removeAttribute("aria-current"); });
          var a = map[en.target.id];
          if (a) {
            a.classList.add("is-active"); a.setAttribute("aria-current", "true");
            var bar = a.closest("ul");
            if (bar && bar.scrollWidth > bar.clientWidth) bar.scrollTo({ left: a.offsetLeft - 24, behavior: reduceMotion ? "auto" : "smooth" });
          }
        }
      });
    }, { rootMargin: "-30% 0px -60% 0px" });
    $$(".menu-cat").forEach(function (s) { so.observe(s); });
  }
  function loadMenu(root) {
    fetch("data/menu.json", { cache: "no-cache" })
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(function (data) {
        if (!data || !Array.isArray(data.categories) || !data.categories.length) throw new Error("Formato non valido");
        renderMenu(data, root);
      })
      .catch(function () {
        root.textContent = "";
        var p = el("p", "menu-state", "Non riusciamo a caricare il menu in questo momento. Riprova tra poco oppure chiama il ristorante al ");
        var a = el("a", null, "0332 602266"); a.href = "tel:+390332602266";
        p.appendChild(a); p.appendChild(doc.createTextNode("."));
        p.setAttribute("role", "alert");
        root.appendChild(p);
      });
  }
})();
