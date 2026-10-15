# Capanna Gigliola - sito demo (Tramontis)

Proposta di restyling per il ristorante **Capanna Gigliola** (Casere, Laveno-Mombello, Lago Maggiore).
Sito statico: HTML, CSS e JavaScript vanilla, senza dipendenze a runtime e senza backend.
È una **DEMO commerciale**, non un sito ufficiale.

## Avvio in locale

```bash
python3 -m http.server 8000
# poi apri http://localhost:8000
```

Serve un server (anche solo questo): aprendo i file con `file://` il browser blocca il caricamento di `data/menu.json` e il menu mostra il messaggio di errore con il telefono.

## Struttura

| Percorso | Contenuto |
|---|---|
| `index.html`, `camere.html`, `storia.html`, `menu.html`, `galleria.html`, `contatti.html`, `privacy.html`, `note-legali.html` | Pagine **generate** da `tools/build.py` |
| `tools/build.py` | Testi, header, footer, galleria e dati di contatto: **qui si modificano i contenuti** |
| `data/menu.json` | Piatti, descrizioni e prezzi |
| `assets/css/style.css` | Stile e variabili (colori e font in `:root`) |
| `assets/js/demo.js` | Interruttore della modalità demo |
| `assets/js/main.js` | Header, menu mobile, reveal, lightbox, filtri, rendering del menu |
| `assets/img/` | Fotografie in WebP |
| `assets/fonts/` | Cormorant Garamond e DM Sans (licenza SIL OFL, self-hosted) |

## Modificare i contenuti

Le pagine HTML sono prodotte da `tools/build.py` così header e footer restano identici ovunque.

1. Modifica `tools/build.py` (testi delle pagine, costanti dei recapiti in cima al file).
2. Rigenera: `python3 tools/build.py` (serve `pip install pillow`, usato solo per leggere le dimensioni delle immagini).
3. Pubblica i file HTML generati: i file sono già nella repository, il build non serve a runtime.

Si possono anche ritoccare a mano i file `.html`, ma al prossimo build le modifiche vengono sovrascritte.

## Aggiornare menu e prezzi

Il link Menu è l'ultimo della navigazione. Il menu attuale riprende il vecchio sito e in pagina c'è una nota (visibile solo in modalità demo) che avvisa che Tramontis lo sostituirà col menu aggiornato appena il ristorante lo invia: la nota è nella funzione `menu()` di `tools/build.py`, attributo `data-demo-only`.

Tutto è in `data/menu.json`. Ogni categoria ha `id`, `title` e `items` (oppure `groups` con sotto-titoli). Una voce ha `name`, `desc` (facoltativa) e `price` come testo (`"14,00"`); per più formati usa `variants: [{"label": "1/2 litro", "price": "6,00"}]`. L'ordine del file è l'ordine in pagina e la barra delle categorie si aggiorna da sola. La sezione `photos` associa una fotografia alla categoria.

> **Da confermare col titolare prima della pubblicazione:** piatti e prezzi sono stati ripresi dal menu online del vecchio sito, che dichiara di non essere sempre aggiornato.

## Immagini

Metti i file in `assets/img/` (WebP consigliato, nome `capanna-gigliola-<soggetto>.webp`). Le fotografie in pagina si indicano per nome in `tools/build.py` (funzione `img(...)`, elenco `GALLERY`). La foto principale della home è `capanna-gigliola-panorama-notturno-hero.webp` (la stessa del vecchio sito, con la variante `-900` per mobile; riporta la firma "Mirko Forza Photography": autorizzazione da confermare). Le larghezze/altezze vengono lette in automatico dal build.

## Recapiti

Telefono, WhatsApp, email, indirizzo, Facebook e link di Google Maps sono costanti all'inizio di `tools/build.py` (`TEL_*`, `WA_*`, `EMAIL`, `ADDR_*`, `FB`, `MAPS`). Cambiale lì e rigenera.

## Modalità DEMO

Un solo interruttore: in `assets/js/demo.js` la variabile `DEMO`.

- `true`: banner fisso in alto, filigrana "DEMO" diagonale, prefisso `[DEMO]` nel titolo, `noindex, nofollow`.
- `false`: lo script toglie banner, filigrana (il CSS dipende da `html[data-demo]`), prefisso `[DEMO]` e meta robots.

Per una messa online definitiva, oltre a `DEMO = false`:

1. In `tools/build.py` togli dal template `head()` il prefisso `[DEMO] ` e la riga `<meta name="robots" ...>`, poi la riga di `banner()` nell'header; rigenera (così il codice HTML non contiene più tracce della demo).
2. Sostituisci `robots.txt` (ora `Disallow: /`) e, quando c'è il dominio definitivo, crea `sitemap.xml` e canonical con gli URL reali.
3. Il link a Tramontis nel **footer** ("proposta di sito realizzata da Tramontis") non dipende dall'interruttore: toglilo solo se vuoi davvero rimuoverlo.

Il banner, nei due layout, è alto 58 px su mobile e 40 px da 760 px in su (`--demo-h` in `style.css`).

## Pubblicare su GitHub Pages

1. Repository > Settings > Pages > Deploy from a branch > branch e cartella `/ (root)`.
2. Il file `.nojekyll` è già presente. Tutti i percorsi sono relativi, quindi il sito funziona anche sotto `https://utente.github.io/nome-repo/`.
3. Nessun segreto o variabile d'ambiente.

## Cose da confermare (non inventate nel sito)

- **Recapiti:** telefono 0332 602266, WhatsApp 333 439 0998 ed email vengono dal sito originale. L'indirizzo (Frazione Casere 2, Strada per Vararo, 21014 Laveno-Mombello) è quello fornito nel brief (Tripadvisor): il sito originale ha solo una mappa, senza indirizzo scritto.
- **Orari:** non pubblicati. Il sito originale indica solo "chiuso il martedì" e "lavoriamo solo su prenotazione".
- **Menu fissi:** il sito cita "due menu fissi da prenotare"; i contenuti non sono descritti (l'originale ospita solo un'immagine di un menu "Ferragosto 2026" a 60 euro, non riportata perché legata a una data).
- **Dati legali** (ragione sociale, P.IVA, titolare del trattamento, email privacy): non presenti, `privacy.html` e `note-legali.html` hanno note da completare.
- **Foto:** diritti e autori da confermare (vedi report). Escluse le immagini con firma di terzi o di stock.
- **Privacy:** la pagina descrive il comportamento reale della demo (nessun modulo, analytics o cookie propri). Va rivista se si aggiungono servizi esterni.
