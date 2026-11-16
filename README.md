# Sito del Dott. Samuele Mirko Croci

Sito statico (HTML, CSS, un po' di JavaScript) per lo studio di fisioterapia di Gorla Minore.
Si pubblica su Netlify (vedi `netlify.toml`).

## Come si modifica

Le pagine `.html` **non si modificano a mano**: le genera lo script `tools/build_site.py`,
così testata, menu, footer e meta SEO restano uguali ovunque.

```bash
python tools/build_site.py
```

Lo script richiede solo Python 3.11 o più recente, nessun pacchetto da installare.
Riscrive tutte le pagine, `sitemap.xml` e `robots.txt`.

- **Testi delle pagine**: dentro `tools/build_site.py` (la pagina Mézières è in `tools/_mezieres_main.html`).
- **Menu e footer**: `NAV` e `FOOTER` in `tools/build_site.py`.
- **Dominio** (canonical, anteprima social, sitemap): `SITE` in `tools/build_site.py`.
- **Grafica**: `style.css`. **Immagini**: `img/`. **Font**: `fonts/` (licenza OFL).
- Lo script avvisa se un titolo supera 60 caratteri o una descrizione 160.

## Pubblicare su Aruba

```bash
python tools/make_dist.py
```

Crea la cartella `dist/` (non è su GitHub: si rigenera quando serve) con solo i file del sito, 26 file in tutto.
Si carica **il contenuto** di `dist/` nella cartella principale del sito sull'hosting (via FTP o dal File Manager
del pannello Aruba), non la cartella `dist` in sé: `index.html` deve stare nella radice.

`dist/` contiene sia `.htaccess` (per hosting Linux/Apache) sia `web.config` (per hosting Windows/IIS):
ogni server usa il suo e ignora l'altro. Dopo il caricamento:

- aprire la home, una pagina interna e una pagina che non esiste (deve comparire la 404 del sito);
- sull'hosting **Windows** il `web.config` è volutamente minimo: il passaggio a HTTPS e i reindirizzamenti dei
  vecchi indirizzi (`chi è il dott. mirko croci.html` → `il-professionista.html`, `le tecniche e la strumentazione.html`
  → `tecniche.html`, `campi di applicazione.html` e `dove ricevo.html` → home) vanno impostati dal pannello Aruba;
- sull'hosting **Linux** li fa già `.htaccess`.

`netlify.toml` serve solo se si torna a pubblicare su Netlify: su Aruba non ha effetto.

## Privacy

Nessun cookie, nessuna statistica, font ospitati qui. L'unico servizio di terzi è la mappa di Google,
che si carica solo dopo il clic su «Mostra la mappa» (`script.js`). Il testo dell'informativa è in
`tools/build_site.py` (pagina `privacy.html`): va fatto rivedere dal titolare prima della pubblicazione,
e aggiornato se si aggiungono moduli, statistiche o altri servizi.

## Cartelle fuori dal sito

`materiali-cliente/` e `FIleVari/` (brochure, documenti di lavoro) non sono su GitHub e, se per errore
finissero online, `netlify.toml` risponde «non trovato».
