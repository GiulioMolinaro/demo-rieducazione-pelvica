# Genera le pagine statiche del sito del Dott. Croci da un unico insieme di parti condivise
# (testata, menu, footer, meta SEO). Uso, dalla cartella del sito:
#
#     python tools/build_site.py
#
# Scrive nella cartella del sito: le pagine .html, sitemap.xml e robots.txt.
# Il testo di ogni pagina è in questo file; stili e immagini restano in style.css e img/.
import os, sys, json, datetime

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.dirname(os.path.abspath(__file__))

# Dominio di pubblicazione: usato per canonical, anteprima social, sitemap e dati strutturati.
# Da cambiare qui se il sito esce su un altro indirizzo.
SITE = 'https://www.rieducazionepelvica.it'
TODAY = datetime.date.today()
TITLE_SUFFIX = 'Dott. Croci, Gorla Minore'
PAGES = []   # pagine indicizzabili, per la sitemap

def head(title, desc):
    return f'''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="@@URL@@">
<meta property="og:type" content="website">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="Dott. Samuele Mirko Croci, fisioterapista">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="@@URL@@">
<meta property="og:image" content="{SITE}/share.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#2b3990">
<link rel="icon" href="img/logo.svg" type="image/svg+xml">
<link rel="preload" href="fonts/jost-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/public-sans-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="style.css">
@@JSONLD@@</head>
<body>
'''

JSONLD = {
    '@context': 'https://schema.org',
    '@type': 'Physiotherapy',
    'name': 'Dott. Samuele Mirko Croci, fisioterapista',
    'description': 'Fisioterapista dal 2000 a Gorla Minore (VA): rieducazione del pavimento pelvico per donna, uomo e bambino, ambito colon-proctologico e Metodo Mézières.',
    'url': SITE + '/',
    'image': SITE + '/share.jpg',
    'telephone': '+39 348 976 9578',
    'email': 'crocimirko@yahoo.it',
    'vatID': 'IT02361960020',
    'address': {
        '@type': 'PostalAddress',
        'streetAddress': 'Via Cesare Battisti 12',
        'postalCode': '21055',
        'addressLocality': 'Gorla Minore',
        'addressRegion': 'VA',
        'addressCountry': 'IT',
    },
    'hasMap': 'https://www.google.com/maps/search/?api=1&query=Via+Cesare+Battisti+12,+21055+Gorla+Minore+VA',
    'medicalSpecialty': 'https://schema.org/PhysicalTherapy',
    'paymentAccepted': 'Contanti, carta (POS)',
    'knowsAbout': ['Rieducazione del pavimento pelvico', 'Incontinenza urinaria', 'Prolasso degli organi pelvici',
                   'Dolore pelvico cronico', 'Rieducazione colon-proctologica', 'Metodo Mézières'],
}

NAV = [
    ('il-professionista.html', 'Il professionista'),
    ('tecniche.html', 'Tecniche'),
    ('index.html#ambiti', 'Ambiti di cura'),
    ('mezieres.html', 'Metodo Mézières'),
    ('index.html#faq', 'Domande frequenti'),
]

def header(current=None):
    links = ''
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ''
        links += f'      <a href="{href}"{cur}>{label}</a>\n'
    return f'''
<header class="site">
  <div class="wrap">
    <a class="brand" href="index.html">
      <img src="img/logo.svg" alt="" width="50" height="48">
      <span><strong>Dott. Samuele Mirko Croci</strong><small>Fisioterapista</small></span>
    </a>
    <button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
    <nav class="main" id="nav">
{links}      <a class="cta" href="index.html#contatti">Prenota</a>
    </nav>
  </div>
</header>
'''

FOOTER = '''
<footer>
  <div class="wrap">
    <div class="footer-map" id="map">
      <div class="map-consent">
        <h2>La mappa dello studio</h2>
        <p>È fornita da Google Maps. Finché non la carica, nessun dato va a Google. Caricandola, Google riceve il suo indirizzo IP e può impostare cookie (<a href="privacy.html#cookie">dettagli</a>).</p>
        <div class="map-actions">
          <button class="btn solid" type="button" id="map-load" hidden>Mostra la mappa</button>
          <a class="link-more" href="https://www.google.com/maps/search/?api=1&amp;query=Via+Cesare+Battisti+12,+21055+Gorla+Minore+VA" target="_blank" rel="noopener">Apri in Google Maps</a>
        </div>
      </div>
    </div>
    <div class="legal">
      <strong>Dott. Samuele Mirko Croci · Fisioterapista</strong>
      <span>Iscritto all’Albo OFI (Ordine dei Fisioterapisti Italiani) n° 7133</span>
      <span>P.IVA 02361960020</span>
    </div>
    <div class="legal">
      <span>Via Cesare Battisti 12, 21055 Gorla Minore (VA)</span>
      <span><a href="tel:+393489769578">348 976 9578</a> · <a href="mailto:crocimirko@yahoo.it">crocimirko@yahoo.it</a></span>
      <span><a href="privacy.html">Privacy e cookie</a></span>
      <span>Designed by <a href="https://0seidigital.com" target="_blank" rel="noopener">0seidigital.com</a></span>
    </div>
  </div>
</footer>

<script src="script.js"></script>
</body>
</html>
'''

MARK = '<svg class="mark" viewBox="28 22 134 138" aria-hidden="true"><use href="img/logo-mark.svg#m"/></svg>'

def page_hero(eyebrow, h1, lead):
    return f'''
<main>

<div class="page-hero">
  <div class="wrap">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{h1}</h1>
    <p>{lead}</p>
  </div>
  {MARK}
</div>
'''

def cta_band(h2='Prenoti la sua visita', p='Chiami lo studio dal lunedì al venerdì, in orario d’ufficio.'):
    return f'''
<div class="cta-band">
  <div class="wrap">
    <div>
      <h2>{h2}</h2>
      <p>{p}</p>
    </div>
    <a class="btn yellow" href="tel:+393489769578">Chiama 348 976 9578</a>
  </div>
</div>

</main>
'''

def write(name, html, index=True):
    """Scrive una pagina: riempie URL canonico e dati strutturati, e registra la pagina per la sitemap."""
    url = SITE + '/' + ('' if name == 'index.html' else name)
    ld = ''
    if name == 'index.html':
        ld = '<script type="application/ld+json">\n' + json.dumps(JSONLD, ensure_ascii=False, indent=2) + '\n</script>\n'
    html = html.replace('@@URL@@', url).replace('@@JSONLD@@', ld)
    if not index:   # pagine da non indicizzare (404): niente canonical né URL social, noindex
        html = html.replace(f'<link rel="canonical" href="{url}">\n', '<meta name="robots" content="noindex">\n')
        html = html.replace(f'<meta property="og:url" content="{url}">\n', '')
    else:
        PAGES.append(name)
    # titoli e descrizioni: i limiti oltre i quali Google li taglia
    import re
    t = re.search(r'<title>(.*?)</title>', html).group(1)
    d = re.search(r'<meta name="description" content="(.*?)">', html).group(1)
    if len(t) > 60 or len(d) > 160:
        print(f'  attenzione {name}: titolo {len(t)} car. (max 60), descrizione {len(d)} car. (max 160)')
    with open(os.path.join(ROOT, name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)

# ------------------------------------------------------------------ ambito pages
def checklist(items):
    out = '<ul class="list-check">\n'
    for it in items:
        if isinstance(it, tuple):
            out += f'        <li>{it[0]}<span>{it[1]}</span></li>\n'
        else:
            out += f'        <li>{it}</li>\n'
    return out + '      </ul>'

OTHER = {
    'donna.html': 'Nella donna', 'uomo.html': 'Nell’uomo', 'bambino.html': 'Nel bambino',
    'colon-proctologia.html': 'In ambito colon-proctologico',
}

def ambito(slug, short, title, desc, eyebrow, h1, lead, h2, items, note=None):
    note_html = f'\n      <p class="note-box">{note}</p>' if note else ''
    others = ''.join(
        f'<a class="card card--link" href="{s}"><h3>{n}</h3><p>Condizioni trattate e come si lavora.</p></a>'
        for s, n in OTHER.items() if s != slug)
    html = head(f'{title} | {TITLE_SUFFIX}', desc) + header('index.html#ambiti') + page_hero(eyebrow, h1, lead) + f'''
<section>
  <div class="wrap">
    <div class="split">
      <div>
        <div class="eyebrow">Condizioni trattate</div>
        <h2>{h2}</h2>{note_html}
      </div>
      {checklist(items)}
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="sec-head">
      <div>
        <div class="eyebrow">Come si lavora</div>
        <h2>Dalla valutazione all’autonomia.</h2>
      </div>
      <p>Ogni percorso parte da un’anamnesi accurata e da un esame obiettivo, per definire un protocollo di lavoro personale.</p>
    </div>
    <div class="cards">
      <a class="card card--link" href="index.html#faq"><h3>La prima visita</h3><p>Porti tutta la documentazione clinica in suo possesso: visite ed eventuali esami eseguiti.</p></a>
      <a class="card card--link" href="tecniche.html"><h3>Le tecniche</h3><p>Biofeedback, elettrostimolazione, terapia manuale.</p></a>
      <a class="card card--link" href="il-professionista.html"><h3>Il professionista</h3><p>Fisioterapista dal 2000, in dialogo con gli specialisti che seguono il paziente.</p></a>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head">
      <div>
        <div class="eyebrow">Altri ambiti</div>
        <h2>Gli altri campi di applicazione.</h2>
      </div>
      <p>La rieducazione perineale non tratta soltanto l’ambito ginecologico femminile, ma anche quello maschile, pediatrico e colon-proctologico.</p>
    </div>
    <div class="cards">
      {others}
      <a class="card card--link" href="mezieres.html"><h3>Rieducazione posturale</h3><p>Il Metodo Mézières per mal di schiena, sciatica e scoliosi.</p></a>
    </div>
  </div>
</section>
''' + cta_band() + FOOTER
    write(slug, html)

ambito(
    'donna.html', 'Donna',
    'Rieducazione pelvica nella donna',
    'Incontinenza, prolassi, rapporti dolorosi, gravidanza e post partum, dolore pelvico: rieducazione del pavimento pelvico nella donna a Gorla Minore (VA).',
    'Rieducazione pelvica · Donna',
    'Rieducazione pelvica nella donna',
    'Incontinenza, prolasso, dolore e disturbi della sfera sessuale, dalla gravidanza alla menopausa: trattamenti di rinforzo, consapevolezza perineale e recupero dopo la chirurgia.',
    'Quando può essere utile.',
    [
        ('Incontinenza urinaria', 'Da sforzo, da urgenza, mista, neurologica'),
        ('Prevenzione e cura dei prolassi', 'Di utero, vescica e retto, causati da un cedimento della muscolatura pelvica'),
        ('Rapporti sessuali dolorosi', 'Vaginismo, dispareunia'),
        'Gravidanza e post partum',
        'Esiti di chirurgia pelvica',
        ('Infiammazioni recidivanti', 'Vaginiti e cistiti, spesso legate a una tensione o a uno spasmo della muscolatura locale'),
        ('Sindromi dolorose pelviche', 'Cistite interstiziale, vestibolite vulvare, vulvodinia, neuropatia del nervo pudendo'),
        'Vescica iperattiva',
        'Coccigodinia',
        ('Vescica neurologica', 'Anche negli esiti di sindrome della cauda equina'),
    ])

ambito(
    'uomo.html', 'Uomo',
    'Rieducazione pelvica nell’uomo',
    'Recupero dopo prostatectomia, prostatiti abatteriche, disturbi urinari e dolore pelvico: rieducazione pelvica nell’uomo a Gorla Minore (VA).',
    'Rieducazione pelvica · Uomo',
    'Rieducazione pelvica nell’uomo',
    'Recupero funzionale dopo la chirurgia della prostata, rieducazione nelle malattie dell’apparato urinario e gestione del dolore pelvico cronico.',
    'Quando può essere utile.',
    [
        ('Trattamento dopo prostatectomia', 'Radicale o parziale: incontinenza urinaria e disfunzione sessuale'),
        'Prostatiti abatteriche e dolore pelvico',
        ('Malattie dell’apparato urinario', 'Ipertrofia prostatica benigna, stenosi dell’uretra, nicturia'),
        'Incontinenza urinaria e/o fecale',
        'Neuropatia del nervo pudendo',
        ('Vescica neurologica', 'Anche negli esiti di sindrome della cauda equina'),
    ])

ambito(
    'bambino.html', 'Bambino',
    'Rieducazione pelvica nel bambino',
    'Enuresi notturna e vescica iperattiva nel bambino: rieducazione pelvica dopo la valutazione dello specialista. Studio a Gorla Minore (VA).',
    'Rieducazione pelvica · Bambino',
    'Rieducazione pelvica nel bambino',
    'Disturbi della minzione nel bambino, valutati prima di tutto dallo specialista di riferimento.',
    'Quando può essere utile.',
    [
        ('Enuresi notturna', 'Perdita del controllo notturno della minzione dopo i tre anni'),
        ('Sindrome della vescica iperattiva', 'Presente in circa il 50% dei bambini con enuresi'),
    ],
    note='La valutazione di pediatra, urologo o neuropsichiatra infantile distingue la forma organica da quella comportamentale. La rieducazione è indicata nella forma organica non di origine psicologica.')

ambito(
    'colon-proctologia.html', 'Colon-proctologia',
    'Rieducazione colon-proctologica',
    'Stipsi, defecazione ostruita, incontinenza ano-rettale e recupero dopo un intervento: rieducazione colon-proctologica a Gorla Minore (VA).',
    'Rieducazione pelvica · Colon-proctologia',
    'Rieducazione in ambito colon-proctologico',
    'Interventi rieducativi per ritrovare controllo e regolarità intestinale, anche prima e dopo un intervento chirurgico.',
    'Quando può essere utile.',
    [
        'Stipsi',
        ('Sindrome da defecazione ostruita', 'Evacuazione difficoltosa, scarsa o ritardata'),
        ('Incontinenza ano-rettale', 'Di gas, liquidi o feci'),
        ('Trattamento preventivo e post-chirurgico', 'Per esempio per emorroidi e ragadi anali, e dopo chirurgia anorettale'),
        ('Esiti di enterostomia', 'Ciclo rieducativo per il recupero della continenza anale'),
    ])

# ------------------------------------------------------------------ tecniche
write('tecniche.html', head(
    f'Tecniche di rieducazione pelvica | {TITLE_SUFFIX}',
    'Biofeedback, elettrostimolazione funzionale, terapia manuale e auto-trattamento: gli strumenti non invasivi della rieducazione del pavimento pelvico.'
) + header('tecniche.html') + page_hero(
    'Tecniche e strumentazioni',
    'Strumenti semplici e non invasivi',
    'Un solo obiettivo: ripristinare la funzione. Dopo un’accurata anamnesi e un esame obiettivo si elabora un protocollo di lavoro personale.'
) + '''
<section>
  <div class="wrap">
    <div class="split">
      <div>
        <div class="eyebrow">Il pavimento pelvico</div>
        <h2>Una struttura, tre funzioni.</h2>
      </div>
      <div class="prose">
        <p>Il pavimento pelvico è la struttura muscolo-tendinea che chiude inferiormente il bacino e interviene in tre funzioni: <strong>urinaria, defecatoria e sessuale</strong>.</p>
        <p>La rieducazione è una branca della fisioterapia che permette di risolvere in modo non invasivo tutta una serie di disfunzioni di questa struttura.</p>
      </div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="method">
      <article><span class="no">01</span><h3>Terapia manuale</h3><p>Delicate manovre e mobilizzazioni pelviche, anche intravaginali e intrarettali, mirate alla normalizzazione muscolare e articolare del bacino. Include il Protocollo Stanford per i trigger point.</p><span class="tag">Manuale</span></article>
      <article><span class="no">02</span><h3>Biofeedback</h3><p>Uno strumento che facilita la presa di coscienza del perineo e del suo funzionamento: rende visibile l’attività muscolare, così da poterla controllare.</p><span class="tag">Strumentale</span></article>
      <article><span class="no">03</span><h3>Elettrostimolazione funzionale (SEF)</h3><p>Un neuromodulatore capace di agire sui circuiti neurologici che regolano il perineo, per via intravaginale, intra-anale o transcutanea.</p><span class="tag">Strumentale</span></article>
      <article><span class="no">04</span><h3>Stimolazione del nervo tibiale posteriore</h3><p>Indicata nella vescica iperattiva: innalza la soglia di percezione dello stimolo urinario, riducendo frequenza e urgenza della minzione.</p><span class="tag">Neuromodulazione</span></article>
      <article><span class="no">05</span><h3>Auto-trattamento domiciliare</h3><p>Programmi di esercizi personalizzati e indicazioni comportamentali, per rendere il paziente autonomo nella gestione del proprio disturbo.</p><span class="tag">Educazione</span></article>
      <article><span class="no">06</span><h3>Approccio globale</h3><p>La rieducazione posturale <a href="mezieres.html">Metodo Mézières</a> integra il trattamento del pavimento pelvico, per intervenire sia sul sintomo sia sulla causa.</p><span class="tag">Integrato</span></article>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="split">
      <div>
        <div class="eyebrow">Gli attrezzi dello studio</div>
        <h2>Pochi attrezzi, tutti semplici.</h2>
        <p class="note-box">Palline, strumenti in legno e in vetro, gli elettrodi per l’elettrostimolazione: lavoro non invasivo, che si può imparare a ripetere anche a casa.</p>
      </div>
      <picture class="photo-frame">
        <source srcset="img/strumenti-studio.webp" type="image/webp">
        <img src="img/strumenti-studio.jpg" width="1024" height="768" loading="lazy" alt="Sul piano di lavoro dello studio: tre palline gialle con il sorriso su una scatola blu piena di elettrodi, un pestello di legno e una ventosa di vetro con la pompetta rossa.">
      </picture>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head">
      <div>
        <div class="eyebrow">Dove si applicano</div>
        <h2>Per ogni fase della vita.</h2>
      </div>
      <p>Le stesse tecniche si adattano a donne, uomini e bambini, con un protocollo personale per ciascuno.</p>
    </div>
    <div class="cards">
      <a class="card card--link" href="donna.html"><h3>Nella donna</h3><p>Incontinenza, prolassi, dolore, gravidanza e post partum.</p></a>
      <a class="card card--link" href="uomo.html"><h3>Nell’uomo</h3><p>Recupero dopo prostatectomia, prostatiti, dolore pelvico.</p></a>
      <a class="card card--link" href="bambino.html"><h3>Nel bambino</h3><p>Enuresi notturna e vescica iperattiva.</p></a>
    </div>
  </div>
</section>
''' + cta_band() + FOOTER)

# ------------------------------------------------------------------ il professionista
write('il-professionista.html', head(
    f'Il professionista | {TITLE_SUFFIX}',
    'Fisioterapista dal 2000: laurea all’Insubria, formazione UROG di Verona, fisioterapista federale svizzero, Metodo Mézières. Studio a Gorla Minore.'
) + header('il-professionista.html') + page_hero(
    'Il professionista',
    'Dott. Samuele Mirko Croci',
    'Fisioterapista specializzato in rieducazione del pavimento pelvico dal 2000, riceve nel proprio studio di Gorla Minore.'
) + '''
<section>
  <div class="wrap">
    <div class="about">
      <figure class="portrait">
        <img src="img/mirko-croci.jpg" alt="Il Dott. Samuele Mirko Croci" width="768" height="1024">
        <figcaption>Dott. Samuele Mirko Croci<br><span>Fisioterapista</span></figcaption>
      </figure>
      <div>
        <div class="eyebrow">Chi è</div>
        <blockquote>Il modo più efficace di trattare un paziente con problematiche del pavimento pelvico è un approccio multidisciplinare.</blockquote>
        <p>Fisioterapista specializzato in rieducazione del pavimento pelvico dal 2000, il Dott. Croci tratta pazienti di ogni età con sintomi vescicali, anorettali, sessuali e dolore perineale. Riceve nel proprio studio di Gorla Minore e lavora in dialogo con le altre figure che seguono il paziente: ginecologo, urologo, sessuologo, neurologo.</p>
        <p>Accanto alla rieducazione perineale si occupa di rieducazione posturale con il <a href="mezieres.html">Metodo Mézières</a>, per il trattamento del mal di schiena e dei dismorfismi come scoliosi e ipercifosi, soprattutto in età evolutiva.</p>
        <p>La comunicazione è chiara e accessibile: disturbi che incidono sulla vita personale, relazionale e sociale vanno spiegati, compresi e affrontati senza imbarazzo.</p>
        <ol class="timeline">
          <li><time>1999</time><span><strong>Diploma Universitario in Fisioterapia</strong>, Università di Pavia, 110/110 e lode.</span></li>
          <li><time>2000</time><span><strong>Formazione UROG di Verona</strong>: attestati di I e II livello in riabilitazione uro-ginecologica, urologica, colonproctologica e pediatrica; dal 2006 tutor e poi docente.</span></li>
          <li><time>2004</time><span><strong>Fisioterapista Federale Svizzero</strong>: quattro anni di pratica a Lugano, con perfezionamento in terapia manuale e patologie della spalla.</span></li>
          <li><time>2006</time><span><strong>Laurea in Fisioterapia</strong>, Università dell’Insubria, 110/110 e lode.</span></li>
          <li><time>2009</time><span><strong>Diploma Metodo Mézières</strong> (rieducazione posturale) e formazione sul Protocollo Stanford per il dolore pelvico cronico.</span></li>
        </ol>
      </div>
    </div>
  </div>
</section>
''' + cta_band() + FOOTER)

# ------------------------------------------------------------------ domande frequenti
def qa(q, a):
    return f'''      <details>
        <summary>{q}</summary>
        <div class="answer">{a}</div>
      </details>
'''
faq_items = [
    ('Cosa devo portare alla prima visita e alle sedute successive?',
     '<p>Alla prima visita porti tutta la documentazione clinica in suo possesso, cioè visite ed eventuali esami eseguiti. Il Dott. Croci valuterà se e quali esami guardare.</p>\n        <p>Durante il ciclo di sedute si ricordi di portare un grande asciugamano pulito o un telo mare e, se necessaria, la sonda vaginale o anale.</p>'),
    ('Dove si trova lo studio?',
     '<p>Lo studio si trova in Via Cesare Battisti 12, 21055 Gorla Minore (VA). Trova la mappa in fondo alla pagina.</p>'),
    ('Quali disturbi tratta?',
     '<p>Disfunzioni del pavimento pelvico nella donna, nell’uomo e nel bambino, e disturbi in ambito colon-proctologico: incontinenza urinaria e fecale, prolassi, dolore pelvico, rapporti dolorosi, recupero dopo la chirurgia, enuresi, stipsi. Le pagine dedicate: <a href="donna.html">donna</a>, <a href="uomo.html">uomo</a>, <a href="bambino.html">bambino</a>, <a href="colon-proctologia.html">colon-proctologia</a>.</p>'),
    ('In che cosa consiste la rieducazione pelvica?',
     '<p>È una branca della fisioterapia che permette di risolvere in modo non invasivo tutta una serie di disfunzioni del pavimento pelvico, la struttura muscolo-tendinea che chiude inferiormente il bacino.</p>\n        <p>Utilizza strumentazioni semplici e non invasive, come il biofeedback e l’elettrostimolazione funzionale, insieme alla terapia manuale. L’approccio dovrebbe essere multidisciplinare e coinvolgere, quando serve, ginecologo, urologo, sessuologo e neurologo. Vedi le <a href="tecniche.html">tecniche</a>.</p>'),
    ('In cosa consiste la rieducazione posturale Mézières?',
     '<p>È una tecnica di rieducazione posturale globale che mira a riequilibrare il corpo, migliorare la postura e ridurre le tensioni muscolari legate a compensi cronici. È indicata per mal di schiena, nevralgie, dolori articolari e dismorfismi come la scoliosi. Tutti i dettagli nella pagina <a href="mezieres.html">Metodo Mézières</a>.</p>'),
    ('Come posso prenotare o disdire un appuntamento?',
     '<p>Telefonando al <a href="tel:+393489769578">348 976 9578</a>, dal lunedì al venerdì in orario d’ufficio. Se il dottore è impegnato con un paziente risponde la segreteria telefonica: lasci nome e recapito e sarà richiamato appena possibile. Per fissare o disdire un appuntamento non è possibile utilizzare gli SMS.</p>'),
    ('Come posso pagare?',
     '<p>Il pagamento si effettua in studio, con carta tramite POS oppure in contanti.</p>'),
]
faq_html = ''.join(qa(q, a) for q, a in faq_items)
FAQ_SECTION = f'''<section id="faq">
  <div class="wrap">
    <div class="sec-head">
      <div>
        <div class="eyebrow">Domande frequenti</div>
        <h2>Le risposte alle domande più comuni.</h2>
      </div>
      <p>Se non trova la risposta che cerca, può chiamare lo studio: le spiegheremo tutto prima della visita.</p>
    </div>
    <div class="faq">
{faq_html}    </div>
  </div>
</section>

'''

# ------------------------------------------------------------------ home (short)
HOME_AMBITI = [
    ('donna.html', 'Nella donna', 'Incontinenza, prolassi, dolore, gravidanza e post partum.'),
    ('uomo.html', 'Nell’uomo', 'Dopo la prostatectomia, prostatiti, incontinenza.'),
    ('bambino.html', 'Nel bambino', 'Enuresi notturna e vescica iperattiva.'),
    ('colon-proctologia.html', 'In ambito colon-proctologico', 'Stipsi, defecazione ostruita, incontinenza.'),
    ('mezieres.html', 'Rieducazione posturale', 'Metodo Mézières per mal di schiena e postura.'),
    ('tecniche.html', 'Tecniche e strumenti', 'Biofeedback, elettrostimolazione, terapia manuale.'),
]
cards = '\n      '.join(
    f'<a class="card card--link" href="{h}"><h3>{t}</h3><p>{p}</p></a>'
    for h, t, p in HOME_AMBITI)

home = head(
    'Rieducazione pelvica a Gorla Minore | Dott. Croci',
    'Fisioterapista dal 2000 a Gorla Minore (VA): rieducazione del pavimento pelvico per donna, uomo e bambino e Metodo Mézières. Su appuntamento.'
) + header() + '''
<main id="top">

<section class="hero">
  <div class="wrap">
    <div class="grid">
      <div>
        <div class="eyebrow">Fisioterapia a Gorla Minore (VA) · dal 2000</div>
        <h1>Il benessere pelvico, trattato con <em>competenza</em> e riservatezza.</h1>
        <p class="lead">Rieducazione non invasiva e personalizzata per disturbi urinari, anorettali, sessuali e dolore pelvico, in donne, uomini e bambini. E, per la postura, il Metodo Mézières.</p>
        <div class="btns">
          <a class="btn solid" href="#contatti">Richiedi un appuntamento</a>
          <a class="btn line" href="#ambiti">Scopri gli ambiti di cura</a>
        </div>
      </div>
      <aside class="hero-card">
        <p class="cover-title">La Rieducazione <b>PELVICA</b></p>
        <svg class="mark" viewBox="28 22 134 138" aria-hidden="true"><use href="img/logo-mark.svg#m"/></svg>
      </aside>
    </div>
  </div>
</section>

<section id="ambiti">
  <div class="wrap">
    <div class="sec-head">
      <div>
        <div class="eyebrow">I campi di applicazione</div>
        <h2>Per ogni fase della vita, un percorso dedicato.</h2>
      </div>
      <p>Donna, uomo, bambino e intestino: scelga l’ambito per leggere le condizioni trattate.</p>
    </div>
    <div class="cards">
      ''' + cards + '''
    </div>
  </div>
</section>

<section id="medico">
  <div class="wrap">
    <div class="about">
      <figure class="portrait">
        <img src="img/mirko-croci.jpg" alt="Il Dott. Samuele Mirko Croci" width="768" height="1024">
        <figcaption>Dott. Samuele Mirko Croci<br><span>Fisioterapista</span></figcaption>
      </figure>
      <div>
        <div class="eyebrow">Il professionista</div>
        <blockquote>Il modo più efficace di trattare un paziente con problematiche del pavimento pelvico è un approccio multidisciplinare.</blockquote>
        <p>Fisioterapista specializzato in rieducazione del pavimento pelvico dal 2000, il Dott. Croci tratta pazienti di ogni età e riceve nel proprio studio di Gorla Minore, in dialogo con le altre figure che seguono il paziente: ginecologo, urologo, sessuologo, neurologo.</p>
        <p><a class="link-more" href="il-professionista.html">Leggi la sua formazione</a></p>
      </div>
    </div>
  </div>
</section>

<section id="percorso">
  <div class="wrap">
    <div class="sec-head">
      <div>
        <div class="eyebrow">Il percorso</div>
        <h2>Un metodo chiaro, dalla prima visita all’autonomia.</h2>
      </div>
      <p>Ogni fase è spiegata con un linguaggio semplice, nel rispetto della sfera più riservata della persona.</p>
    </div>
    <div class="steps">
      <div class="step"><h3>Primo contatto</h3><p>Una telefonata, dal lunedì al venerdì in orario d’ufficio, per fissare la prima visita.</p></div>
      <div class="step"><h3>Valutazione</h3><p>Anamnesi dettagliata ed esame obiettivo, partendo dalla documentazione clinica che porta con sé.</p></div>
      <div class="step"><h3>Trattamento</h3><p>Tecniche manuali e strumentali scelte sul caso, in dialogo con gli specialisti che la seguono.</p></div>
      <div class="step"><h3>Autonomia</h3><p>Esercizi e indicazioni comportamentali per mantenere i risultati nel tempo.</p></div>
    </div>
    <p class="steps-link"><a class="link-more" href="#faq">Leggi le domande frequenti</a></p>
  </div>
</section>

''' + FAQ_SECTION + '''<section id="contatti">
  <div class="wrap">
    <div class="contact">
      <div>
        <div class="eyebrow">Contatti</div>
        <h2>Prenota una visita</h2>
        <dl class="dl">
          <div><dt>Telefono</dt><dd><a href="tel:+393489769578">348 976 9578</a></dd></div>
          <div><dt>Email</dt><dd><a href="mailto:crocimirko@yahoo.it">crocimirko@yahoo.it</a></dd></div>
          <div><dt>Studio</dt><dd><a href="https://www.google.com/maps/search/?api=1&amp;query=Via+Cesare+Battisti+12,+21055+Gorla+Minore+VA" target="_blank" rel="noopener">Via Cesare Battisti 12<br>21055 Gorla Minore (VA)</a></dd></div>
          <div><dt>Visite</dt><dd>Su appuntamento, dal lunedì al venerdì</dd></div>
        </dl>
      </div>
      <div>
        <h3>Come fissare o disdire</h3>
        <p>Il dottore risponde al telefono dal lunedì al venerdì, in orario d’ufficio. Se è impegnato con un paziente risponde la segreteria telefonica: lasci nome e recapito, sarà richiamato appena possibile.</p>
        <p>Per fissare o disdire un appuntamento non è possibile utilizzare gli SMS.</p>
        <a class="btn yellow" href="tel:+393489769578">Chiama ora</a>
      </div>
    </div>
  </div>
</section>

</main>
''' + FOOTER
write('index.html', home)
# ------------------------------------------------------------------ metodo mézières
# Il corpo della pagina è in tools/_mezieres_main.html; testata, menu e footer sono quelli comuni.
with open(os.path.join(TOOLS, '_mezieres_main.html'), encoding='utf-8') as f:
    MEZIERES_MAIN = f.read()
write('mezieres.html', head(
    f'Metodo Mézières a Gorla Minore | {TITLE_SUFFIX}',
    'Rieducazione posturale globale per mal di schiena, sciatica, dolori articolari e scoliosi. Dott. Samuele Mirko Croci, fisioterapista.'
) + header('mezieres.html') + '\n' + MEZIERES_MAIN + FOOTER)

# ------------------------------------------------------------------ privacy e cookie
UPDATED = f'{TODAY.day} {["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"][TODAY.month-1]} {TODAY.year}'
write('privacy.html', head(
    f'Privacy e cookie | {TITLE_SUFFIX}',
    'Come il sito del Dott. Samuele Mirko Croci tratta i dati personali: nessun cookie di profilazione, mappa di Google caricata solo su richiesta.'
) + header() + page_hero(
    'Informativa', 'Privacy e cookie',
    'Quali dati tratta questo sito, perché e per quanto tempo. In breve: pochissimi, e nessun cookie di profilazione.'
) + f'''
<section>
  <div class="wrap">
    <div class="legal-doc">
      <h2>Chi è il titolare</h2>
      <p>Il titolare del trattamento è il Dott. Samuele Mirko Croci, fisioterapista, con studio in Via Cesare Battisti 12, 21055 Gorla Minore (VA), P.IVA 02361960020. Per qualsiasi richiesta sui suoi dati può scrivere a <a href="mailto:crocimirko@yahoo.it">crocimirko@yahoo.it</a>.</p>

      <h2>Quali dati tratta il sito</h2>
      <ul>
        <li><strong>Dati di navigazione.</strong> Il sito è pubblicato da un fornitore di hosting, i cui sistemi registrano in modo automatico alcuni dati tecnici delle visite: indirizzo IP, data e ora, pagina richiesta, tipo di browser. Servono a far funzionare il sito e a proteggerlo da abusi. Base giuridica: legittimo interesse del titolare (art. 6.1.f del Regolamento UE 2016/679, GDPR). Non vengono usati per profilarla.</li>
        <li><strong>Dati che ci comunica lei.</strong> Il sito non ha moduli. Se telefona o scrive per email, usiamo il suo nome e il suo recapito soltanto per risponderle e per fissare o disdire un appuntamento (art. 6.1.b GDPR).</li>
      </ul>
      <p>Il sito non raccoglie dati sanitari. I dati relativi alla salute trattati durante le visite in studio sono oggetto di un’informativa separata.</p>

      <h2 id="cookie">Cookie e servizi di terze parti</h2>
      <p>Questo sito non usa cookie di profilazione, strumenti di statistica o pulsanti dei social, e non imposta cookie propri. Per questo non c’è un banner per il consenso ai cookie.</p>
      <p>I caratteri (font) sono ospitati sul sito stesso: per mostrarli il suo browser non contatta altri server.</p>
      <p><strong>Mappa di Google Maps.</strong> In fondo a ogni pagina c’è la mappa dello studio. Non viene caricata finché non preme «Mostra la mappa». Solo da quel momento Google riceve il suo indirizzo IP e può impostare cookie, secondo la <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">propria informativa</a>. Se non la carica, nessun dato va a Google. In alternativa può usare il link «Apri in Google Maps», che la porta direttamente sul sito di Google.</p>

      <h2>Chi riceve i dati</h2>
      <p>I dati di navigazione sono trattati dal fornitore di hosting del sito, in qualità di responsabile del trattamento. Google riceve dati solo se lei carica la mappa. I suoi dati non vengono venduti né ceduti ad altri.</p>

      <h2>Per quanto tempo</h2>
      <p>I dati di navigazione sono conservati per il tempo tecnico stabilito dal fornitore di hosting. I dati di contatto per il tempo necessario a risponderle e per rispettare gli obblighi di legge.</p>

      <h2>I suoi diritti</h2>
      <p>Può chiedere l’accesso ai suoi dati, la rettifica, la cancellazione, la limitazione del trattamento, opporsi al trattamento e, dove previsto, la portabilità (artt. 15-22 GDPR), scrivendo a <a href="mailto:crocimirko@yahoo.it">crocimirko@yahoo.it</a>. Ha inoltre il diritto di proporre reclamo al Garante per la protezione dei dati personali (<a href="https://www.garanteprivacy.it" target="_blank" rel="noopener">garanteprivacy.it</a>).</p>

      <p class="legal-doc__date">Ultimo aggiornamento: {UPDATED}.</p>
    </div>
  </div>
</section>
''' + cta_band() + FOOTER)

# ------------------------------------------------------------------ pagina 404
write('404.html', head(
    f'Pagina non trovata | {TITLE_SUFFIX}',
    'La pagina cercata non esiste o è stata spostata. Torni alla home del sito del Dott. Samuele Mirko Croci.'
) + header() + page_hero(
    'Errore 404', 'Pagina non trovata',
    'Il collegamento che ha seguito non esiste più o è stato spostato.'
) + '''
<section>
  <div class="wrap">
    <div class="sec-head">
      <div>
        <div class="eyebrow">Da dove ripartire</div>
        <h2>Alcune pagine utili.</h2>
      </div>
      <p>Può tornare alla home oppure scegliere direttamente un argomento.</p>
    </div>
    <div class="cards">
      <a class="card card--link" href="index.html"><h3>Home</h3><p>Il sito dall’inizio.</p></a>
      <a class="card card--link" href="index.html#ambiti"><h3>Ambiti di cura</h3><p>Donna, uomo, bambino, intestino.</p></a>
      <a class="card card--link" href="index.html#contatti"><h3>Contatti</h3><p>Telefono e indirizzo dello studio.</p></a>
    </div>
  </div>
</section>
</main>
''' + FOOTER, index=False)

# ------------------------------------------------------------------ sitemap e robots
urls = ''.join(
    f'  <url>\n    <loc>{SITE}/{"" if n == "index.html" else n}</loc>\n    <lastmod>{TODAY.isoformat()}</lastmod>\n  </url>\n'
    for n in PAGES)
with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
with open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(f'User-agent: *\nAllow: /\nDisallow: /materiali-cliente/\nDisallow: /FIleVari/\nDisallow: /tools/\n\nSitemap: {SITE}/sitemap.xml\n')
print(f'ok: {len(PAGES)} pagine + 404, sitemap.xml, robots.txt')
