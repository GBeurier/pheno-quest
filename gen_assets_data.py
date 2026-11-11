"""Embarque tous les assets (PNG + WAV + MID + TTF) en base64 dans js/assets_data.js.
=> le jeu tourne en double-cliquant index.html (file://), sans aucun serveur,
   et se deploie tel quel sur n'importe quel hebergeur statique.

A relancer apres avoir change/ajoute un asset dans assets/sprites, assets/sounds
ou assets/music.

Les PNG sont recompresses en WebP LOSSLESS (strictement les memes pixels,
~25% plus petit) au moment de l'embed si Pillow est dispo ; on garde le PNG
quand il est plus petit (rare) ou si Pillow manque. Les sources restent des
PNG dans assets/sprites/ : rien ne change pour les pipelines d'art.
"""
import base64
import hashlib
import io
import json
import os

try:
    from PIL import Image
except ImportError:
    Image = None

ROOT = os.path.dirname(os.path.abspath(__file__))
SPR = os.path.join(ROOT, "assets", "sprites")
SND = os.path.join(ROOT, "assets", "sounds")
MUS = os.path.join(ROOT, "assets", "music")
FNT = os.path.join(ROOT, "assets", "fonts")
OUT = os.path.join(ROOT, "js", "assets_data.js")

os.makedirs(MUS, exist_ok=True)   # le script ne casse jamais si le repertoire manque
os.makedirs(FNT, exist_ok=True)


def datauri(data, mime):
    return "data:%s;base64,%s" % (mime, base64.b64encode(data).decode())


# AI-generated art is not palette pixel-art: a high-quality LOSSY WebP is visually
#  identical in game and 2-3x smaller than the lossless one (perf pass "le jeu est
#  gros"). Painted pictures (panoramas / screens bg_*, boss sheets boss_*) at q88,
#  character / enemy / NPC body sheets at q90 (checked side by side, x4 zoom).
#  Tiles, icons, heads, UI stay pixel-exact (lossless WebP).
LOSSY = {"bg_": 88, "boss_": 88, "enemy_": 90, "hero_": 90, "marcos_": 90, "oriane_": 90, "body_": 90}


def lossy_q(name):
    return next((q for pre, q in LOSSY.items() if name.startswith(pre)), None)


# Encoding cache (local only, gitignored): WebP method 6 on 300+ sprites takes
#  minutes; the result only depends on the source bytes + the encoding settings.
CACHE = os.path.join(ROOT, ".cache", "assets")
CACHE_TAG = "v1-q88"   # + per-file lossy quality when it is not 88 (cf. best_image)
SEP = bytes([10])    # cache file = mime + newline + bytes


def best_image(path, mime):
    with open(path, "rb") as f:
        raw = f.read()
    if Image is None:
        return raw, mime          # no Pillow: as is
    q = lossy_q(os.path.basename(path))
    tag = CACHE_TAG + ("" if q in (None, 88) else "-l%d" % q)
    key = hashlib.sha1(raw + tag.encode() + os.path.basename(path).encode()).hexdigest()
    cpath = os.path.join(CACHE, key)
    if os.path.exists(cpath):
        with open(cpath, "rb") as f:
            blob = f.read()
        m, _, data = blob.partition(SEP)
        return data, m.decode()
    data, m = encode_image(path, raw, mime)
    os.makedirs(CACHE, exist_ok=True)
    with open(cpath, "wb") as f:
        f.write(m.encode() + SEP + data)
    return data, m


def encode_image(path, raw, mime):
    """Bytes + mime of the most compact version (original / WebP lossless / lossy for painted art)."""
    name = os.path.basename(path)
    cands = [(raw, mime)]
    im = Image.open(path)
    if mime == "image/png":
        buf = io.BytesIO()
        im.save(buf, "WEBP", lossless=True, quality=100, method=6)
        cands.append((buf.getvalue(), "image/webp"))
    q = lossy_q(name)
    if q:
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=q, method=6, alpha_quality=100)
        cands.append((buf.getvalue(), "image/webp"))
    return min(cands, key=lambda c: len(c[0]))


# PNG = sprites/transparence ; JPG = fonds plein-cadre sans alpha (bien plus leger).
IMG_MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}
sprites, sounds = {}, {}
png_total = out_total = 0
for fn in sorted(os.listdir(SPR)):
    name, ext = os.path.splitext(fn)
    if ext.lower() in IMG_MIME and not fn.startswith("_"):
        data, mime = best_image(os.path.join(SPR, fn), IMG_MIME[ext.lower()])
        png_total += os.path.getsize(os.path.join(SPR, fn))
        out_total += len(data)
        sprites[name] = datauri(data, mime)
for fn in sorted(os.listdir(SND)):
    if fn.endswith(".wav"):
        with open(os.path.join(SND, fn), "rb") as f:
            sounds[fn[:-4]] = datauri(f.read(), "audio/wav")

# Musiques : .mid en base64 BRUT (pas de prefixe data: — le lecteur chiptune
#  js/music.js fait atob() et parse les octets lui-meme).
music, mus_total = {}, 0
for fn in sorted(os.listdir(MUS)):
    name, ext = os.path.splitext(fn)
    # casse-insensible (.MID exporte par un DAW) + .midi, comme les sprites
    if ext.lower() in (".mid", ".midi") and not fn.startswith("_"):
        with open(os.path.join(MUS, fn), "rb") as f:
            raw = f.read()
        mus_total += len(raw)
        music[name] = base64.b64encode(raw).decode()

# Fonts : .ttf/.otf en data-URI (FontFace marche en file://). Subsettees a la
#  source (cf. CLAUDE.md, bulles BD des PNJ) -> quelques dizaines de Ko piece.
fonts, fnt_total = {}, 0
for fn in sorted(os.listdir(FNT)):
    name, ext = os.path.splitext(fn)
    if ext.lower() in (".ttf", ".otf") and not fn.startswith("_"):
        with open(os.path.join(FNT, fn), "rb") as f:
            raw = f.read()
        fnt_total += len(raw)
        fonts[name] = datauri(raw, "font/ttf" if ext.lower() == ".ttf" else "font/otf")

with open(OUT, "w") as f:
    f.write("/* AUTO-GENERE par gen_assets_data.py — ne pas editer a la main.\n")
    f.write("   Assets embarques en base64 : le jeu marche sans serveur (file://). */\n")
    f.write("window.ASSETS = ")
    json.dump({"sprites": sprites, "sounds": sounds, "music": music, "fonts": fonts}, f)
    f.write(";\n")

size = os.path.getsize(OUT)
print("js/assets_data.js : %d sprites (%.1f -> %.1f Mo, webp), %d sons, "
      "%d musiques (%.1f Ko), %d fonts (%.1f Ko), %.0f Ko"
      % (len(sprites), png_total / 1e6, out_total / 1e6, len(sounds),
         len(music), mus_total / 1024, len(fonts), fnt_total / 1024, size / 1024))
