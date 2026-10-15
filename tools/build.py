#!/usr/bin/env python3
"""Genera le pagine HTML statiche di Capanna Gigliola (header e footer condivisi).

Uso:  python3 tools/build.py
Richiede Pillow (solo per leggere width/height delle immagini).
Le pagine generate sono file HTML normali: il sito funziona senza build a runtime.
"""
import html
import json
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = "assets/img/capanna-gigliola-"

# ------------------------------------------------------------------ dati verificati
NAME = "Capanna Gigliola"
TEL_DISPLAY = "0332 602266"
TEL_HREF = "tel:+390332602266"
WA_DISPLAY = "333 439 0998"
WA_HREF = "https://wa.me/393334390998"
EMAIL = "ristorantegigliola@libero.it"
FB = "https://www.facebook.com/RistoranteGigliola/"
ADDR_1 = "Frazione Casere 2, Strada per Vararo"
ADDR_2 = "21014 Laveno-Mombello (VA)"
MAPS = "https://www.google.com/maps/search/?api=1&query=Capanna+Gigliola+Frazione+Casere+2+Laveno-Mombello"
TRAMONTIS = "https://tramontis.netlify.app/"
DEMO_MSG = "Proposta di sito non ancora attiva. Per averla online sul vostro dominio contatta"

NAV = [("index.html", "Home"), ("storia.html", "La storia"), ("menu.html", "Menu"),
       ("galleria.html", "Galleria"), ("contatti.html", "Contatti")]

ICON = {
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A15 15 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12h16M14 6l6 6-6 6"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20l1.4-4.2A8 8 0 1 1 8.2 18.6z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s7-6.2 7-11a7 7 0 0 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>',
}
RIDGE = '<svg class="ridge" viewBox="0 0 1200 28" preserveAspectRatio="none" aria-hidden="true"><path d="M0 22 L90 14 L170 20 L260 6 L350 18 L430 10 L520 21 L620 4 L700 16 L790 9 L880 20 L980 8 L1070 17 L1200 12"/></svg>'


def esc(s):
    return html.escape(s, quote=True)


def dims(name):
    with Image.open(os.path.join(ROOT, IMG + name + ".webp")) as im:
        return im.size


def img(name, alt, cls="", loading="lazy", extra=""):
    w, h = dims(name)
    c = f' class="{cls}"' if cls else ""
    fp = ' fetchpriority="high"' if loading == "eager" else ""
    return (f'<img{c} src="{IMG}{name}.webp" width="{w}" height="{h}" alt="{esc(alt)}" '
            f'loading="{loading}" decoding="async"{fp}{extra}>')


# ------------------------------------------------------------------ componenti
def head(title, desc, jsonld=None, og_img="panorama-lago-hero"):
    ld = ""
    if jsonld:
        ld = f'\n<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>'
    return f"""<!doctype html>
<html lang="it">
<head>
<script src="assets/js/demo.js"></script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>[DEMO] {esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#1d362b">
<meta property="og:type" content="website">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="[DEMO] {esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{IMG}{og_img}.webp">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/cormorant-garamond-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/dm-sans-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">{ld}
</head>"""


def banner():
    return (f'<div class="demo-banner" data-demo-only role="note"><p><strong>VERSIONE DEMO -</strong> {DEMO_MSG} '
            f'<a href="{TRAMONTIS}" target="_blank" rel="noopener">Tramontis</a>.</p></div>')


def header(current):
    def li(href, label, mobile=False):
        cur = ' aria-current="page"' if href == current else ""
        return f'<li><a href="{href}"{cur}>{label}</a></li>'
    desk = "".join(li(h, l) for h, l in NAV)
    mob = "".join(li(h, l) for h, l in NAV)
    return f"""<a class="skip-link" href="#contenuto">Vai al contenuto</a>
{banner()}
<header class="site-header">
  <div class="wrap header-inner">
    <a class="wordmark" href="index.html" aria-label="{NAME}, home"><b>{NAME}</b><span>Ristorante a Casere, Laveno-Mombello</span></a>
    <nav class="nav-desktop" aria-label="Navigazione principale"><ul>{desk}</ul></nav>
    <div class="header-actions">
      <a class="btn header-cta" href="{TEL_HREF}">{ICON['phone']}<span>Prenota<span class="cta-long"> al telefono</span></span></a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav-mobile" aria-label="Apri il menu di navigazione"><span></span></button>
    </div>
  </div>
</header>
<nav class="nav-mobile" id="nav-mobile" aria-label="Navigazione principale (mobile)">
  <ul>{mob}</ul>
  <div class="nav-foot">
    <a class="btn btn--ivory" href="{TEL_HREF}">{ICON['phone']}Chiama {TEL_DISPLAY}</a>
    <p>{ADDR_1}<br>{ADDR_2}</p>
  </div>
</nav>"""


def footer():
    links = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in NAV)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand"><b>{NAME}</b><p>Cucina casalinga di montagna a Casere, sopra Laveno-Mombello, sul Lago Maggiore.</p></div>
      <nav aria-label="Sezioni del sito"><h2>Il sito</h2><ul>{links}</ul></nav>
      <div class="footer-contact"><h2>Contatti</h2><ul>
        <li><a href="{TEL_HREF}">{TEL_DISPLAY}</a></li>
        <li><a href="{WA_HREF}" target="_blank" rel="noopener">WhatsApp {WA_DISPLAY}</a></li>
        <li>{ADDR_1}<br>{ADDR_2}</li>
        <li><a href="contatti.html">Come prenotare e arrivare</a></li>
      </ul></div>
      <div><h2>Informazioni</h2><ul>
        <li><a href="privacy.html">Privacy</a></li>
        <li><a href="note-legali.html">Note legali</a></li>
        <li><a href="{FB}" target="_blank" rel="noopener">Facebook</a></li>
      </ul></div>
    </div>
    <div class="footer-bottom">
      <p class="credit">proposta di sito realizzata da <a href="{TRAMONTIS}" target="_blank" rel="noopener">Tramontis</a></p>
    </div>
  </div>
</footer>
<script src="assets/js/main.js" defer></script>
</body>
</html>"""


def page(fname, title, desc, current, body, body_cls="", jsonld=None, og_img="panorama-lago-hero"):
    out = head(title, desc, jsonld, og_img) + f'\n<body{(" class=%s" % chr(34) + body_cls + chr(34)) if body_cls else ""}>\n'
    out += header(current) + '\n<main id="contenuto">\n' + body + '\n</main>\n' + footer() + "\n"
    with open(os.path.join(ROOT, fname), "w", encoding="utf-8") as f:
        f.write(out)


def restaurant_ld():
    return {
        "@context": "https://schema.org", "@type": "Restaurant", "name": NAME,
        "telephone": "+390332602266",
        "address": {"@type": "PostalAddress", "streetAddress": "Frazione Casere 2, Strada per Vararo",
                    "postalCode": "21014", "addressLocality": "Laveno-Mombello", "addressCountry": "IT"},
        "hasMap": MAPS, "sameAs": [FB],
    }


def reserve_block(title="Prenota il tuo tavolo", text=None):
    text = text or ("Lavoriamo solo su prenotazione, perché la conduzione è familiare. Il modo più rapido è chiamare "
                    "o scrivere su WhatsApp. Il martedì il ristorante è chiuso.")
    return f"""<section class="reserve section" aria-labelledby="prenota-t">
  <div class="reserve-bg">{img('tramonto-dorato-lago', 'Tramonto dorato sul Lago Maggiore visto dalla montagna', loading='lazy')}</div>
  <div class="wrap">
    <h2 id="prenota-t" data-reveal>{title}</h2>
    <p data-reveal style="--d:.1s">{text}</p>
    <a class="reserve-phone" href="{TEL_HREF}" data-reveal style="--d:.2s">{TEL_DISPLAY}</a>
    <div class="btn-row" data-reveal style="--d:.3s">
      <a class="btn" href="{TEL_HREF}">{ICON['phone']}Chiama ora</a>
      <a class="btn btn--ghost" href="{WA_HREF}" target="_blank" rel="noopener">{ICON['chat']}Scrivi su WhatsApp</a>
    </div>
    <small>{ADDR_1}, {ADDR_2}</small>
  </div>
</section>"""


def tl_items():
    return [
        ("1882", "Una villa per riposare",
         "La Capanna Gigliola viene fatta costruire dal proprietario della ceramica Revelli di Laveno Mombello, "
         "che cercava un «angolo di paradiso» dove riposare il corpo e la mente dopo le giornate di lavoro in riva al lago."),
        ("1945", "Da villa a locanda",
         "Alla fine della seconda guerra mondiale la villa diventa una locanda. La rileva il gestore del bar Giglio, "
         "sul golfo di Laveno, allora sede del CAI: la nuova attività prende il nome di Giglio-Là, a indicare la montagna."),
        ("1970", "La famiglia Papini",
         "Dopo alcuni cambi di gestione, Vittorio e Desolina Papini rilevano la Capanna Gigliola. "
         "A marito e moglie si aggiungono i figli Daniela e Alessandro."),
        ("1996", "L'ampliamento",
         "Importanti lavori di ampliamento portano la Capanna alla configurazione attuale. E, come dice la famiglia, la storia non si ferma qui."),
    ]


# ------------------------------------------------------------------ galleria
GALLERY = [
    # file, alt, categorie, forma
    ("terrazza-tavoli-lago", "Lunghi tavoli e panche di legno sulla terrazza, con il lago in lontananza", "ambienti panorama", "wide"),
    ("sala-taverna-camino", "La taverna in sasso e legno, con travi a vista, lampade a muro e il camino in fondo alla sala", "ambienti", "wide"),
    ("tramonto-geranei-lago", "Cielo rosato al tramonto sul lago, con gerani rossi in primo piano", "panorama", ""),
    ("capanna-inverno-neve", "La Capanna Gigliola dopo una nevicata, con l'edificio giallo e gli abeti carichi di neve", "ristorante", ""),
    ("tagliatelle-gnocchetti-balcone", "Due ciotole di pasta fatta in casa su un tavolo di legno, con il panorama del lago alle spalle", "cucina", "tall"),
    ("sala-carro-prodotti-tipici", "Sala del ristorante con un carro di legno che espone bottiglie e prodotti, sotto le travi del soffitto", "ambienti", ""),
    ("tortino-cioccolato-vista-lago", "Tortino al cioccolato con panna e fragole, sullo sfondo il lago tra le montagne", "cucina panorama", "wide"),
    ("panorama-riflessi-sole", "Il sole che scende sul Lago Maggiore, con ortensie in primo piano", "panorama", ""),
    ("carne-alla-griglia", "Tagli di carne alla griglia su un tagliere, decorati con foglie di alloro", "cucina", "tall"),
    ("lago-blu-primavera", "Il lago azzurro incorniciato dai rami di un albero, in una giornata limpida", "panorama", ""),
    ("funghi-porcini", "Un cesto pieno di funghi porcini freschi", "cucina", ""),
    ("tramonto-rosso-lago", "Tramonto rosso sulla valle e sul lago, con le montagne in controluce", "panorama", ""),
    ("caffe-valdostana-grolla", "Caffè alla valdostana nella grolla, con la fiamma accesa sul bordo", "cucina", "tall"),
    ("mare-di-nebbia", "Un mare di nebbia sotto il cielo azzurro, con le Alpi innevate in lontananza", "panorama", "tall"),
    ("prato-giochi-gerani", "Il prato con altalene, scivolo e casetta di legno, e gerani rossi in primo piano", "ambienti", ""),
    ("controluce-geranei-lago", "Il sole tra le montagne sopra il lago, con gerani rossi in controluce", "panorama", ""),
    ("storia-capanna-foto-antica", "Fotografia d'epoca della Capanna: la villa con il portico ad archi e un'auto parcheggiata davanti", "ristorante", ""),
    ("storia-cartolina-vararo", "Cartolina d'epoca con la Capanna e le montagne di Vararo", "ristorante", ""),
    ("tramonto-dorato-lago", "Nuvole dorate al tramonto sul lago, viste dalla montagna", "panorama", ""),
    ("camera-chalet-letto", "Camera matrimoniale in legno con letto dalle lenzuola gialle e porta-finestra sul terrazzo", "ambienti", "wide"),
    ("panorama-staccionata", "Il lago e il sole tra le nuvole, visti oltre una staccionata di legno", "panorama", "tall"),
    ("asino-nel-prato", "Un asino al pascolo in un prato fiorito", "ristorante", ""),
]
CAT_LABEL = [("tutte", "Tutte"), ("ristorante", "Il ristorante"), ("ambienti", "Gli ambienti"),
             ("cucina", "La cucina"), ("panorama", "Il panorama")]


def g_item(f, alt, cats, shape, auto_tall=True):
    w, h = dims(f)
    if auto_tall and not shape and w / h < .85:
        shape = "tall"
    cls = "g-item" + (f" {shape}" if shape else "")
    return (f'<button type="button" class="{cls}" data-lb data-cat="{cats}" aria-label="Ingrandisci: {esc(alt)}">'
            f'{img(f, alt)}</button>')


# ------------------------------------------------------------------ pagine
def home():
    tiles = f"""<div class="tiles">
  <a class="tile tile--a" href="menu.html#primi" data-reveal>{img('tagliatelle-gnocchetti-balcone', 'Due ciotole di pasta fatta in casa su un tavolo di legno')}
    <div class="tile-body"><h3>Paste all'uovo fatte in casa</h3><p>Tagliatelle al ragù di cinghiale, gnocchetti di pane con ortiche alle erbe aromatiche, mezze maniche di mirtillo con speck croccante.</p></div></a>
  <a class="tile tile--b" href="menu.html#dolci" data-reveal style="--d:.08s">{img('tortino-cioccolato-vista-lago', 'Tortino al cioccolato con panna e fragole, con il lago sullo sfondo')}
    <div class="tile-body"><h3>Dolci fatti in casa</h3><p>Tiramisù, panna cotta con mirtilli, tortino caldo al cioccolato. Il gelato è di produzione propria, anche con latte di capra.</p></div></a>
  <a class="tile tile--c" href="menu.html#secondi" data-reveal style="--d:.12s">{img('carne-alla-griglia', 'Carne alla griglia su un tagliere con foglie di alloro')}
    <div class="tile-body"><h3>Selvaggina e brace</h3><p>Bocconcini di cervo, bruscit di cinghiale, grigliata con salsiccia di cinghiale.</p></div></a>
  <a class="tile tile--d" href="menu.html#polenta" data-reveal style="--d:.16s">{img('funghi-porcini', 'Un cesto di funghi porcini freschi')}
    <div class="tile-body"><h3>Polenta e montagna</h3><p>Montanara, ai quattro formaggi, con farina macinata al sasso.</p></div></a>
</div>"""

    tl = "".join(f'<li class="tl-item" data-reveal><div class="tl-year">{y}</div><h3>{t}</h3><p>{d}</p></li>'
                 for y, t, d in tl_items())
    prev = [GALLERY[0], GALLERY[2], GALLERY[5], GALLERY[4], GALLERY[7], GALLERY[6]]
    gprev = "".join(g_item(f, a, c, "", False) for f, a, c, s in prev)

    body = f"""<section class="hero" aria-labelledby="hero-t">
  <div class="hero-media"><picture><source media="(max-width: 700px)" srcset="{IMG}panorama-lago-hero-816.webp"><img src="{IMG}panorama-lago-hero.webp" width="1632" height="918" alt="Il Lago Maggiore visto dall'alto tra i boschi, con le montagne sullo sfondo" fetchpriority="high" decoding="async"></picture></div>
  <div class="wrap hero-inner">
    <p class="kicker">Laveno-Mombello · Lago Maggiore</p>
    <h1 id="hero-t">I sapori della tradizione, con vista sul lago</h1>
    <p class="hero-text">Una villa del 1882 diventata locanda nel 1945, a Casere sopra Laveno-Mombello. Cucina casalinga: pasta all'uovo fatta in casa, polenta, selvaggina e dolci della casa.</p>
    <div class="btn-row">
      <a class="btn" href="menu.html">Scopri il menu</a>
      <a class="btn btn--ghost" href="contatti.html#prenotazioni">Prenota un tavolo</a>
    </div>
  </div>
  <div class="hero-quota" aria-hidden="true"><span>Casere, 768 m</span><i></i></div>
</section>

<section class="section" aria-labelledby="intro-t">
  <div class="wrap intro-grid">
    <div>
      <p class="kicker" data-reveal>La Capanna</p>
      <h2 class="title" id="intro-t" data-reveal>Una tavola di montagna davanti al camino, o sul balcone del lago</h2>
      <div class="prose" style="margin-top:1.8rem" data-reveal>
        <p>Oggi la Capanna Gigliola è il posto giusto per una cena di lavoro, per un ristoro dopo una camminata in montagna, per un pranzo romantico affacciati sul «più bel balcone del Lago Maggiore» o davanti al camino, nella taverna in sasso e legno.</p>
        <p>La cucina è casalinga: antipasti con salumi, sottoli e sottaceti, pasta fatta in casa, polenta con selvaggina e funghi porcini, grigliate, dolci e gelato di produzione propria.</p>
      </div>
      <ul class="intro-facts" data-reveal>
        <li><b>Alla carta</b><span>Specialità rustiche dal menu, con piatti di selvaggina e polenta.</span></li>
        <li><b>Menu fissi</b><span>Due menu da prenotare in anticipo. Chiedi i dettagli al ristorante.</span></li>
        <li><b>All'aperto</b><span>Gli amici a quattro zampe sono benvenuti fuori, non nel locale.</span></li>
      </ul>
    </div>
    <div class="intro-photos" data-reveal>
      <div class="arch">{img('sala-taverna-camino', 'La taverna in sasso e legno con travi a vista e il camino in fondo alla sala', extra=' style="object-position:50% 40%"')}</div>
      <div class="wide">{img('terrazza-tavoli-lago', 'Tavoli e panche di legno sulla terrazza, con il lago sullo sfondo')}</div>
    </div>
  </div>
</section>

<section class="section section--stone" aria-labelledby="cucina-t">
  <div class="wrap">
    <div class="cucina-head">
      <div><p class="kicker" data-reveal>La cucina</p><h2 class="title" id="cucina-t" data-reveal>Pasta all'uovo, polenta, selvaggina e dolci della casa</h2></div>
      <p class="prose" data-reveal>Piatti della tradizione di montagna, come li trovi nel menu del ristorante. I prezzi sono quelli del menu online, che può differire da quello proposto in sala.</p>
    </div>
    {tiles}
    <div class="cucina-foot" data-reveal>
      <p>Antipasti con salumi e formaggi, caffè alla valdostana nella coppa dell'amicizia: il menu completo raccoglie tutto.</p>
      <a class="link-arrow" href="menu.html">Sfoglia il menu completo {ICON['arrow']}</a>
    </div>
  </div>
</section>

<section class="section--dark panorama" aria-labelledby="pan-t">
  <div class="wrap">
    <div class="panorama-grid">
      <div>
        <p class="kicker" data-reveal>Il panorama</p>
        <h2 class="title" id="pan-t" data-reveal>Il lago cambia con le ore</h2>
        <div class="prose" style="margin-top:1.6rem" data-reveal>
          <p>La Capanna sorge a Casere, antico nucleo montano a 768 metri sopra Laveno-Mombello. Da qui lo sguardo scende verso il Lago Maggiore: all'alba, a mezzogiorno, al tramonto, sempre con una luce diversa.</p>
        </div>
      </div>
      <div class="panorama-photos" data-reveal>
        <figure class="p1">{img('tramonto-rosso-lago', 'Tramonto rosso sulla valle e sul lago, con le montagne in controluce')}</figure>
        <figure class="p2">{img('mare-di-nebbia', 'Un mare di nebbia sotto il cielo azzurro, con le Alpi innevate in lontananza')}</figure>
      </div>
    </div>
    <figure class="panorama-wide" data-reveal>{img('tramonto-geranei-lago', 'Cielo rosato al tramonto sul lago, con gerani rossi in primo piano')}</figure>
  </div>
</section>

<section class="section" aria-labelledby="storia-t">
  <div class="wrap storia-grid">
    <figure class="storia-photo" data-reveal style="margin:0">
      <div class="arch">{img('storia-capanna-foto-antica', "Fotografia d'epoca della Capanna: la villa con il portico ad archi e un'auto parcheggiata davanti", extra=' style="object-position:22% 50%"')}</div>
      <figcaption>Una fotografia d'epoca della Capanna.</figcaption>
    </figure>
    <div>
      <p class="kicker" data-reveal>La storia</p>
      <h2 class="title" id="storia-t" data-reveal>Dal 1882, un angolo di paradiso sopra il lago</h2>
      <ol class="timeline" style="margin-top:2.6rem">{tl}</ol>
      <p style="margin-top:2.4rem" data-reveal><a class="link-arrow" href="storia.html">Leggi la storia completa {ICON['arrow']}</a></p>
    </div>
  </div>
</section>

<section class="section section--stone" aria-labelledby="gal-t">
  <div class="wrap">
    <div class="cucina-head">
      <div><p class="kicker" data-reveal>La galleria</p><h2 class="title" id="gal-t" data-reveal>Sala, piatti e panorama</h2></div>
      <p class="prose" data-reveal>Alcune immagini della Capanna. Tocca una foto per ingrandirla.</p>
    </div>
    <div class="gallery-preview" data-lb-group data-reveal>{gprev}</div>
    <p style="margin-top:2.4rem" data-reveal><a class="link-arrow" href="galleria.html">Vai alla galleria completa {ICON['arrow']}</a></p>
  </div>
</section>

{reserve_block()}"""
    page("index.html", "Capanna Gigliola | Ristorante a Laveno-Mombello, Lago Maggiore",
         "Capanna Gigliola, ristorante a Casere di Laveno-Mombello: cucina casalinga di montagna, pasta all'uovo fatta in casa, polenta, selvaggina e vista sul Lago Maggiore.",
         "index.html", body, jsonld=restaurant_ld())


def storia():
    items = tl_items()
    ch = []
    figs = [
        f'<figure><div class="photo-frame">{img("storia-capanna-foto-antica", "Fotografia d_epoca della Capanna: la villa con il portico ad archi e un_auto parcheggiata davanti".replace("_", chr(39)))}</div><p class="figcap">Fotografia d\'epoca della villa.</p></figure>',
        f'<figure><div class="photo-frame small">{img("storia-facciata-bianco-nero", "Fotografia in bianco e nero della facciata con balcone e archi del portico")}</div><p class="figcap">La facciata con il balcone e gli archi.</p></figure>',
        f'<figure><div class="photo-frame">{img("storia-cartolina-vararo", "Cartolina d_epoca con la Capanna e le montagne di Vararo".replace("_", chr(39)))}</div><p class="figcap">Cartolina d\'epoca con la Capanna e le montagne di Vararo.</p></figure>',
        f'<figure><div class="photo-frame">{img("capanna-inverno-neve", "La Capanna Gigliola dopo una nevicata, con l_edificio giallo e gli abeti innevati".replace("_", chr(39)))}</div><p class="figcap">La Capanna in inverno.</p></figure>',
    ]
    for (y, t, d), fg in zip(items, figs):
        extra = ""
        if y == "1945":
            extra = ("<p>Il nome racconta da dove arrivava il nuovo gestore: «Giglio» per il bar, «Là» per la montagna.</p>")
        ch.append(f'<article class="story-chapter" data-reveal><div><div class="tl-year">{y}</div><h2>{t}</h2>'
                  f'<div class="prose"><p>{d}</p>{extra}</div></div>{fg}</article>')
    body = f"""<section class="page-hero">
  <div class="wrap split split--photo">
    <div>
      <p class="kicker">La storia</p>
      <h1>Un angolo di paradiso, dal 1882</h1>
      <p class="lead">Da villa di riposo a locanda, da locanda a ristorante di famiglia: la Capanna Gigliola in quattro date.</p>
    </div>
    <div class="arch" style="aspect-ratio:4/5;max-width:380px;justify-self:end;width:100%">{img('storia-capanna-foto-antica', "Fotografia d'epoca della Capanna: la villa con il portico ad archi e un'auto parcheggiata davanti", loading='eager', extra=' style="object-position:22% 50%"')}</div>
  </div>
</section>
<section class="section" style="padding-top:clamp(48px,7vw,96px)">
  <div class="wrap">
    <p class="story-quote" data-reveal>Un «angolo di paradiso» per riposare il corpo e la mente dopo le giornate di lavoro in riva al lago.</p>
    <div style="margin-top:clamp(32px,5vw,64px)">{''.join(ch)}</div>
  </div>
</section>
<section class="section section--stone" aria-labelledby="oggi-t">
  <div class="wrap storia-grid">
    <figure class="storia-photo" style="margin:0" data-reveal>
      <div class="arch">{img('sala-taverna-camino', 'La taverna in sasso e legno con il camino acceso in fondo alla sala', extra=' style="object-position:50% 45%"')}</div>
    </figure>
    <div>
      <p class="kicker" data-reveal>Oggi</p>
      <h2 class="title" id="oggi-t" data-reveal>La cucina di casa, nella taverna in sasso e legno</h2>
      <div class="prose" style="margin-top:1.6rem" data-reveal>
        <p>La Capanna Gigliola è il posto ideale per cene di lavoro, per il ristoro dopo una bella camminata in montagna, per pranzi romantici sul balcone del lago o davanti al camino.</p>
        <p>Si può scegliere tra due menu fissi da prenotare in anticipo oppure tra le specialità rustiche del menu alla carta. La cucina è casalinga: antipasti a base di salumi, sottoli e sottaceti, pasta fatta in casa, polenta con selvaggina, funghi porcini, grigliate, dolci e gelato di produzione propria, anche con latte di capra.</p>
        <p>Chi vuole chiudere il pasto in modo classico può ordinare il caffè alla valdostana, servito nell'originale coppa dell'amicizia.</p>
      </div>
      <div class="btn-row" style="margin-top:2.2rem" data-reveal>
        <a class="btn btn--forest" href="menu.html">Guarda il menu</a>
        <a class="btn btn--ghost" href="contatti.html#prenotazioni" style="color:var(--forest)">Come prenotare</a>
      </div>
    </div>
  </div>
</section>
{reserve_block("Vieni a conoscere la Capanna")}"""
    page("storia.html", "La storia | Capanna Gigliola",
         "Dal 1882 a oggi: la storia della Capanna Gigliola, villa costruita sopra Laveno-Mombello, locanda dal 1945 e ristorante della famiglia Papini dal 1970.",
         "storia.html", body, og_img="storia-capanna-foto-antica")


def menu():
    body = f"""<section class="page-hero">
  <div class="wrap">
    <p class="kicker">Il menu</p>
    <h1>Cucina casalinga, piatti di montagna</h1>
    <p class="lead">Pasta all'uovo fatta in casa, polenta, selvaggina, salumi e dolci della casa.</p>
  </div>
</section>
<div class="menu-nav"><div class="wrap"><nav aria-label="Categorie del menu"><ul id="menu-nav-list"></ul></nav></div></div>
<section class="section" style="padding-top:clamp(32px,5vw,56px)">
  <div class="wrap">
    <p class="menu-note" role="note"><span>Il menu online è indicativo e potrebbe differire da quello proposto in loco. Prezzi in euro.</span></p>
    <div id="menu-root" aria-live="polite"><p class="menu-state">Caricamento del menu in corso.</p></div>
    <noscript><p class="menu-state">Per visualizzare il menu serve JavaScript. Chiama il ristorante al <a href="{TEL_HREF}">{TEL_DISPLAY}</a> per conoscere i piatti.</p></noscript>
  </div>
</section>
{reserve_block("Vuoi assaggiarli?", "Il ristorante lavora su prenotazione. Chiama o scrivi su WhatsApp per riservare il tavolo e chiedere dei due menu fissi.")}"""
    page("menu.html", "Menu | Capanna Gigliola",
         "Il menu della Capanna Gigliola: antipasti, paste all'uovo fatte in casa, selvaggina, polenta, panini, dolci, vini e bevande. Menu indicativo.",
         "menu.html", body, og_img="tagliatelle-gnocchetti-balcone")


def galleria():
    filters = "".join(f'<button type="button" class="filter-btn" data-filter="{k}" aria-pressed="{"true" if k=="tutte" else "false"}">{l}</button>'
                      for k, l in CAT_LABEL)
    items = "".join(g_item(*g) for g in GALLERY)
    body = f"""<section class="page-hero">
  <div class="wrap">
    <p class="kicker">La galleria</p>
    <h1>Il ristorante, la cucina, il lago</h1>
    <p class="lead">Sala, piatti e panorami della Capanna Gigliola.</p>
  </div>
</section>
<section class="section" style="padding-top:clamp(40px,6vw,72px)">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Filtra le fotografie per categoria">{filters}</div>
    <p class="visually-hidden" id="gallery-count" aria-live="polite"></p>
    <div class="gallery-grid" data-lb-group>{items}</div>
  </div>
</section>
{reserve_block()}"""
    page("galleria.html", "Galleria fotografica | Capanna Gigliola",
         "Le fotografie della Capanna Gigliola: la taverna in sasso e legno, i piatti della casa e i panorami sul Lago Maggiore.",
         "galleria.html", body, og_img="terrazza-tavoli-lago")


def contatti():
    body = f"""<section class="page-hero">
  <div class="wrap">
    <p class="kicker">Contatti e posizione</p>
    <h1>Prenota e vieni a trovarci</h1>
    <p class="lead">Un tavolo alla Capanna si prenota per telefono o su WhatsApp.</p>
  </div>
</section>
<section class="section" id="prenotazioni" aria-labelledby="pren-t" style="padding-top:clamp(48px,7vw,96px)">
  <div class="wrap contact-grid">
    <div>
      <h2 class="title" id="pren-t" style="font-size:clamp(2.2rem,4.4vw,3.6rem)" data-reveal>Come prenotare</h2>
      <p class="prose" style="margin:1.2rem 0 2rem" data-reveal>Essendo un'attività a conduzione prettamente familiare, il ristorante lavora solo su prenotazione. La soluzione migliore è telefonare o scrivere su WhatsApp; il ristorante cerca di rispondere in fretta anche su Facebook.</p>
      <ul class="contact-list" data-reveal>
        <li><span class="contact-label">Telefono</span><a href="{TEL_HREF}">{TEL_DISPLAY}</a></li>
        <li><span class="contact-label">Telefono o WhatsApp</span><a href="{WA_HREF}" target="_blank" rel="noopener">{WA_DISPLAY}</a></li>
        <li><span class="contact-label">Email</span><a class="plain plain-link" href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><span class="contact-label">Indirizzo</span><span class="plain">{ADDR_1}<br>{ADDR_2}</span></li>
        <li><span class="contact-label">Giorno di chiusura</span><span class="plain">Martedì. Per gli orari di apertura chiama o scrivi su WhatsApp.</span></li>
        <li><span class="contact-label">Facebook</span><a class="plain plain-link" href="{FB}" target="_blank" rel="noopener">Ristorante Gigliola</a></li>
      </ul>
      <div class="btn-row" style="margin-top:2rem" data-reveal>
        <a class="btn" href="{TEL_HREF}">{ICON['phone']}Chiama {TEL_DISPLAY}</a>
        <a class="btn btn--forest" href="{MAPS}" target="_blank" rel="noopener">{ICON['pin']}Apri su Google Maps</a>
      </div>
    </div>
    <aside class="info-card" data-reveal aria-labelledby="arr-t">
      <h3 id="arr-t">Come arrivare a Casere</h3>
      <p>Il nucleo montano di Casere si trova a 768 metri. Si raggiunge in tre modi:</p>
      <ul class="check-list" style="color:var(--on-dark-soft)">
        <li style="color:var(--on-dark-soft)">in auto, seguendo la SP8 da Cittiglio;</li>
        <li style="color:var(--on-dark-soft)">con la bidonvia da Laveno fino a Poggio Sant'Elia;</li>
        <li style="color:var(--on-dark-soft)">a piedi, dalla piazza Fontana di Laveno Mombello.</li>
      </ul>
      <p style="margin-top:1.4rem">Gli amici a quattro zampe sono benvenuti all'aperto, con le dovute cautele. Nel locale non sono ammessi, a causa di problemi di allergia.</p>
    </aside>
  </div>
</section>

<section class="section section--stone" aria-labelledby="camera-t">
  <div class="wrap">
    <div class="cucina-head">
      <div><p class="kicker" data-reveal>Dormire a Casere</p><h2 class="title" id="camera-t" data-reveal>Camera matrimoniale con bagno privato</h2></div>
      <div class="prose" data-reveal>
        <p>In un contesto montano, con giardino privato e un comodo terrazzo soleggiato che guarda al Sasso del Ferro.</p>
        <ul class="check-list">
          <li>Doccia, televisione con decoder satellitare, wi-fi gratuito</li>
          <li>Bollitore, sdraio, giardino privato e terrazzo</li>
          <li>Animali non ammessi</li>
        </ul>
        <p style="margin-top:1rem">Per disponibilità e condizioni, contatta il ristorante.</p>
      </div>
    </div>
    <div class="room-photos" data-lb-group data-reveal>
      <button type="button" class="g-item r1" style="aspect-ratio:16/8;grid-column:1/-1" data-lb aria-label="Ingrandisci la camera matrimoniale">{img('camera-chalet-letto', 'Camera matrimoniale in legno con letto dalle lenzuola gialle e porta-finestra sul terrazzo')}</button>
      <button type="button" class="g-item r2" style="aspect-ratio:16/9" data-lb aria-label="Ingrandisci il soppalco della camera">{img('camera-chalet-soppalco', 'Camera in legno con letto matrimoniale e scala del soppalco')}</button>
      <button type="button" class="g-item" style="aspect-ratio:16/9" data-lb aria-label="Ingrandisci il bagno">{img('camera-chalet-bagno', 'Bagno privato con rivestimento in pietra e finiture di legno')}</button>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="hike-t">
  <div class="wrap">
    <div class="cucina-head">
      <div><p class="kicker" data-reveal>Camminate</p><h2 class="title" id="hike-t" data-reveal>Itinerari che passano da Casere</h2></div>
      <p class="prose" data-reveal>Tre percorsi descritti sul sito della Capanna. Prima di partire controlla condizioni del sentiero e meteo.</p>
    </div>
    <ul class="hike-list" data-reveal>
      <li><h3>Pizzoni di Laveno</h3><p class="hike-meta">3 ore, 7 km circa, difficoltà E</p><p>Da Casere (768 m) al Passo del Curvignone (1.050 m), lungo la cresta dei Pizzoni, fino al rifugio CAI di Besozzo. Attenzione sul terreno bagnato.</p></li>
      <li><h3>Zuigno, Cittiglio, Vararo</h3><p class="hike-meta">4 ore 30, 10,5 km circa, difficoltà E</p><p>Da Zuigno a Vararo attraverso Casale, San Quirico e Cittiglio, passando per Casere davanti al ristorante.</p></li>
      <li><h3>Laveno, Sasso del Ferro, Casere</h3><p class="hike-meta">4 ore, 11,5 km circa, difficoltà EE</p><p>Un anello da Laveno (205 m) a Casere passando dal Poggio Sant'Elsa e dal Sasso del Ferro (1.062 m). La discesa è ripida: serve attenzione.</p></li>
    </ul>
  </div>
</section>
{reserve_block("Ci vediamo a Casere")}"""
    page("contatti.html", "Contatti e prenotazioni | Capanna Gigliola",
         "Come prenotare alla Capanna Gigliola e come raggiungerla: telefono, WhatsApp, indirizzo a Casere di Laveno-Mombello e indicazioni per arrivare.",
         "contatti.html", body, jsonld=restaurant_ld(), og_img="terrazza-tavoli-lago")


def legal_hero(t, lead):
    return f"""<section class="page-hero"><div class="wrap"><p class="kicker">Informazioni</p><h1>{t}</h1><p class="lead">{lead}</p></div></section>"""


def privacy():
    body = legal_hero("Privacy", "Come questa versione demo tratta i dati di chi la visita.") + f"""
<section class="section" style="padding-block:0"><div class="wrap legal">
<h2>Titolare del trattamento</h2>
<p>Questa è una versione dimostrativa realizzata da Tramontis. I dati identificativi del titolare del trattamento (denominazione, indirizzo, recapiti per l'esercizio dei diritti) saranno inseriti prima della pubblicazione definitiva del sito.</p>
<p class="todo">Da completare con il titolare prima della messa online: ragione sociale, indirizzo e contatto privacy.</p>
<h2>Dati trattati</h2>
<p>Il sito è composto da pagine statiche. Non contiene moduli di contatto o di prenotazione, non prevede registrazione e non utilizza strumenti di analisi o di pubblicità. Il sito stesso non imposta cookie.</p>
<p>Come per ogni sito web, il servizio che lo ospita può registrare dati tecnici di connessione (per esempio indirizzo IP, data e ora della richiesta, pagina richiesta) per garantire la sicurezza e il funzionamento del servizio.</p>
<h2>Font e risorse</h2>
<p>I caratteri tipografici e le immagini sono ospitati insieme al sito: la visita non richiede di contattare servizi esterni per caricarli.</p>
<h2>Collegamenti esterni</h2>
<p>Alcuni collegamenti portano a servizi di terze parti: Google Maps, WhatsApp, Facebook e il sito di Tramontis. Quando segui questi collegamenti, il trattamento dei dati è regolato dalle informative di quei servizi. Il telefono e il collegamento «tel:» aprono l'app di chiamata del tuo dispositivo.</p>
<h2>Prenotazioni</h2>
<p>Le prenotazioni avvengono per telefono, WhatsApp o altri canali del ristorante, non attraverso questo sito. I dati comunicati in quelle occasioni sono trattati dal ristorante secondo la propria informativa.</p>
<h2>I tuoi diritti</h2>
<p>Puoi chiedere l'accesso, la rettifica o la cancellazione dei tuoi dati e proporre reclamo al Garante per la protezione dei dati personali. Le modalità di contatto saranno indicate quando i dati del titolare saranno disponibili.</p>
<p class="todo">Questo testo è una bozza per la demo. Va verificato e completato prima della pubblicazione, in particolare se verranno aggiunti moduli, mappe incorporate, strumenti di analisi o servizi esterni.</p>
</div></section>"""
    page("privacy.html", "Privacy | Capanna Gigliola", "Informazioni sul trattamento dei dati nella versione demo del sito della Capanna Gigliola.", "", body)


def note_legali():
    body = legal_hero("Note legali", "Informazioni su questa versione demo del sito.") + f"""
<section class="section" style="padding-block:0"><div class="wrap legal">
<h2>Natura del sito</h2>
<p>Questo sito è una proposta grafica realizzata da <a href="{TRAMONTIS}" target="_blank" rel="noopener">Tramontis</a> per Capanna Gigliola. Non è un sito ufficiale pubblicato e non è indicizzabile dai motori di ricerca.</p>
<h2>Titolare e dati societari</h2>
<p>Ragione sociale, partita IVA e sede legale del ristorante non sono riportate in questa versione, perché non verificate. Saranno inserite prima della pubblicazione.</p>
<p class="todo">Da completare con il titolare: ragione sociale, partita IVA, sede legale, eventuali recapiti PEC.</p>
<h2>Contenuti</h2>
<p>Testi, prezzi e fotografie provengono dal sito attuale del ristorante (ristorante-gigliola.weebly.com) e sono stati riordinati per questa proposta. Il menu online è indicativo e può differire da quello proposto in sala: prezzi e piatti vanno confermati dal ristorante.</p>
<p>Le fotografie appartengono ai rispettivi autori. L'uso definitivo delle immagini va concordato con il titolare, che dovrà confermarne la disponibilità.</p>
<h2>Responsabilità</h2>
<p>Le informazioni su orari, prezzi e disponibilità possono cambiare: per conferma contatta direttamente il ristorante.</p>
<h2>Font</h2>
<p>I caratteri Cormorant Garamond e DM Sans sono distribuiti con licenza SIL Open Font License e ospitati insieme al sito.</p>
</div></section>"""
    page("note-legali.html", "Note legali | Capanna Gigliola", "Note legali della versione demo del sito della Capanna Gigliola, proposta di restyling realizzata da Tramontis.", "", body)


if __name__ == "__main__":
    home(); storia(); menu(); galleria(); contatti(); privacy(); note_legali()
    print("Pagine generate.")
