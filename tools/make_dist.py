# Prepara la cartella dist/ da caricare sull'hosting (Aruba): solo i file del sito, niente file di lavoro.
#
#     python tools/make_dist.py
#
# 1. rigenera le pagine (tools/build_site.py)
# 2. svuota e ricrea dist/
# 3. copia pagine, stili, script, immagini, font, anteprima social, sitemap e robots
# 4. aggiunge .htaccess (hosting Linux) e web.config (hosting Windows): ognuno è ignorato dal server sbagliato
import os, shutil, subprocess, sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
DIST = os.path.join(ROOT, 'dist')

subprocess.run([sys.executable, os.path.join(TOOLS, 'build_site.py'), ROOT], check=True)

if os.path.isdir(DIST):
    shutil.rmtree(DIST)
os.makedirs(DIST)

files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html')) + [
    'style.css', 'script.js', 'share.jpg', 'sitemap.xml', 'robots.txt']
for f in files:
    shutil.copy2(os.path.join(ROOT, f), os.path.join(DIST, f))
for d in ('img', 'fonts'):
    shutil.copytree(os.path.join(ROOT, d), os.path.join(DIST, d))
for f in ('.htaccess', 'web.config'):
    shutil.copy2(os.path.join(TOOLS, 'server', f), os.path.join(DIST, f))

total = 0
for base, _, names in os.walk(DIST):
    for n in names:
        total += os.path.getsize(os.path.join(base, n))
count = sum(len(n) for _, _, n in os.walk(DIST))
print(f'dist/ pronta: {count} file, {total / 1024:.0f} KB')
