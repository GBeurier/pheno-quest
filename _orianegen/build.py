#!/usr/bin/env python3
"""raw/ (Codex image_gen) -> assets/sprites/ for the ORIANE campaign.

Mechanical only (chroma key / crop / scale / seam), sizes = existing analogues:
  oriane_sheet  4x4 magenta sheet -> oriane_<state>.png, 224x224 cells (= marcos_*)
  oriane_bike   4 frames          -> oriane_bike.png, 256x224 cells, same scale as the hero
  tile_simu     -> 144x88 cap (= tile_panel), front ledge on the walk line
  simu_leg      -> 96x48 (= panel_leg), 2 beams at x 24 / 60
  bg_simu_*     -> parallax bands (seam window + cross-fade), cf. _javagen/build.py
  tile_sol_*    -> 224x296 floor tile via _levelgen/postprocess.py (do_sol)
  olab_p1..p3   -> panorama (do_panorama) cut in 2 halves bg_olab_a / bg_olab_b (<= 4096 px)
  bg_oriane_*   -> full screens, cover-fit, JPEG
Usage: python _orianegen/build.py [name ...]   then   python gen_assets_data.py
"""
import os, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, '_javagen'))
sys.path.insert(0, os.path.join(ROOT, '_levelgen'))
import build as jb            # _javagen/build.py helpers (key_magenta, trim, resize_rgba, seam band...)
import postprocess as lp      # _levelgen/postprocess.py (do_sol, do_panorama)

RAW = os.path.join(HERE, 'raw')
SPR = os.path.join(ROOT, 'assets', 'sprites')
jb.RAW = RAW
jb.FINAL = os.path.join(HERE, 'final')
jb.BANDS = {
    'bg_simu_far': (960, 480, True, (0.45, 0.70)),    # = bg_mountains
    'bg_simu_mid': (2027, 370, False, (0.70, 0.96)),  # = bg_field
}
jb.NO_DARK_KEY = {'bg_simu_far', 'bg_simu_mid'}       # dark navy pixels must survive the key
jb.SCREENS = {'bg_oriane_map': (1920, 1056), 'bg_oriane_chapter': (1672, 941), 'bg_oriane_win': (1672, 941)}

CELL, FIG_H, BASE = 224, 200, 220
STATES = {'idle': [0, 1], 'run': [4, 5, 6, 7], 'jump': [8, 9], 'hurt': [10], 'throw': [2, 3],
          'duck': [0, 12, 13], 'dash': [11], 'dead': [14, 15]}


def grid_cells(im, cols, rows):
    W, H = im.size
    out = []
    for r in range(rows):
        for c in range(cols):
            cell = im.crop((round(c * W / cols), round(r * H / rows), round((c + 1) * W / cols), round((r + 1) * H / rows)))
            bb = cell.getbbox()
            out.append(cell.crop(bb) if bb else cell)
    return out


def hero_factor():
    im = jb.key_magenta(Image.open(os.path.join(RAW, 'oriane_sheet.png')))
    cells = grid_cells(im, 4, 4)
    return cells, FIG_H / cells[0].height


def build_hero():
    cells, f = hero_factor()
    frames = []
    for i, c in enumerate(cells):
        c = jb.resize_rgba(c, (max(1, round(c.width * f)), max(1, round(c.height * f))), nearest=True)
        fr = Image.new('RGBA', (CELL, CELL))
        x = (CELL - c.width) // 2 + (12 if i == 3 else 0)    # throw release: arm forward, body stays put
        x = max(0, min(CELL - c.width, x))
        fr.alpha_composite(c.crop((0, 0, min(c.width, CELL), min(c.height, BASE))), (x, BASE - min(c.height, BASE)))
        frames.append(fr)
    for st, idx in STATES.items():
        sheet = Image.new('RGBA', (CELL * len(idx), CELL))
        for k, i in enumerate(idx):
            sheet.paste(frames[i], (k * CELL, 0))
        sheet.save(os.path.join(SPR, 'oriane_' + st + '.png'), optimize=True)
        print('wrote oriane_%s %s' % (st, sheet.size))


def build_bike():
    _, f = hero_factor()
    # oriane_bike_cannon = the same sheet with the chili cannon on the handlebars
    src = 'oriane_bike_cannon.png' if os.path.exists(os.path.join(RAW, 'oriane_bike_cannon.png')) else 'oriane_bike.png'
    im = jb.key_magenta(Image.open(os.path.join(RAW, src)), dark=False)
    cells = grid_cells(im, 4, 1)
    # the rider on her bike is drawn at a different scale than the standing sheet:
    #  normalise the tallest frame to ~0.98 x the standing figure height
    k = (FIG_H * 0.98) / max(c.height for c in cells)
    W = 256
    sheet = Image.new('RGBA', (W * 4, CELL))
    muzzles = []
    for i, c in enumerate(cells):
        c = jb.resize_rgba(c, (max(1, round(c.width * k)), max(1, round(c.height * k))), nearest=True)
        if c.width > W:
            c = jb.resize_rgba(c, (W, round(c.height * W / c.width)))
        # centre on the WHEELS (bottom 30%), not on the whole bbox: the cannon
        #  sticking out in front must not push the bike backwards
        a = np.array(c)[..., 3] > 0
        cols = np.where(a[int(c.height * 0.7):].any(axis=0))[0]
        mid = (cols[0] + cols[-1]) / 2 if len(cols) else c.width / 2
        x = int(round(W / 2 - mid))
        x = max(0, min(W - c.width, x))
        y = BASE - c.height
        sheet.alpha_composite(c, (i * W + x, y))
        # muzzle = rightmost opaque pixel in the handlebar band (35%-60% height)
        band = a[int(c.height * 0.35):int(c.height * 0.60)]
        rr, cc = np.where(band)
        if len(cc):
            j = cc.argmax()
            muzzles.append((x + cc[j] - W / 2, y + int(c.height * 0.35) + rr[j]))
    sheet.save(os.path.join(SPR, 'oriane_bike.png'), optimize=True)
    print('wrote oriane_bike from', src, sheet.size, 'hero factor %.3f bike factor %.3f' % (f, k))
    if muzzles:   # cell px, origin = cell centre-x / top; game units = /2 (art.scale), feet at BASE
        mx = sum(m[0] for m in muzzles) / len(muzzles); my = sum(m[1] for m in muzzles) / len(muzzles)
        print('muzzle (cell px from centre / from feet): x %+.1f  y %+.1f' % (mx, my - BASE))


WALK_Y = 60


def build_cap(name):
    """Cap scaled to tile_panel's width (129) with its front ledge on the walk line."""
    im = jb.trim(jb.key_magenta(Image.open(os.path.join(RAW, name + '.png')), dark=False))
    im = jb.resize_rgba(im, (129, max(1, round(im.height * 129 / im.width))))
    frac = (np.array(im)[..., 3] > 0).mean(axis=1)
    y = im.height - 1
    while y > 0 and frac[y] < 0.75:
        y -= 1
    while y > 0 and frac[y - 1] >= 0.75:
        y -= 1
    top = WALK_Y - y
    cv = Image.new('RGBA', (144, 88), (0, 0, 0, 0))
    if top < 0:
        im = im.crop((0, -top, im.width, im.height)); top = 0
    cv.alpha_composite(im.crop((0, 0, im.width, min(im.height, 88 - top))), (0, top))
    jb.save(cv, name)


def build_leg(name):
    im = jb.trim(jb.key_magenta(Image.open(os.path.join(RAW, name + '.png')), dark=False))
    a = np.array(im)[..., 3] > 0
    cols = np.flatnonzero(a.mean(axis=0) > 0.5)
    im = im.crop((int(cols[0]), 0, int(cols[-1]) + 1, im.height))
    pw = 13
    seg_h = round(im.width * 48 / pw)
    y0 = max(0, (im.height - seg_h) // 2)
    seg = jb.resize_rgba(im.crop((0, y0, im.width, min(im.height, y0 + seg_h))), (pw, 48))
    arr = np.array(seg); arr[..., 3] = 255
    seg = Image.fromarray(arr)
    cv = Image.new('RGBA', (96, 48), (0, 0, 0, 0))
    for x in (24, 60):
        cv.alpha_composite(seg, (x, 0))
    jb.save(cv, name)


def build_floor(name):
    lp.do_sol(os.path.join(RAW, name + '.png'), os.path.join(SPR, name + '.png'))


def wall_band(path):
    """(wall top, skirting top) rows of a corridor panel, measured on its plain-wall
    side edges (the prompt keeps the far-left 8% free): first cream-wall row, then
    the first grey skirting row in the lower half."""
    a = np.array(Image.open(path).convert('RGB')).astype(int)
    H, W, _ = a.shape
    col = a[:, int(W * 0.01):int(W * 0.05)].mean(axis=1)
    cream = (col[:, 0] > 215) & (col[:, 1] > 195) & (col[:, 2] > 150) & (col[:, 2] < 215) & (col[:, 0] - col[:, 2] > 25)
    grey = (np.abs(col[:, 0] - col[:, 2]) < 18) & (col[:, 0] < 190)
    top = int(np.flatnonzero(cream)[0])
    skirt = int([y for y in np.flatnonzero(grey) if y > H * 0.5][0])
    return H, top, skirt


def align_panels(paths):
    """Piecewise vertical resize (ceiling / wall / floor bands) so the panels share
    the same ceiling and skirting heights (= the mean of the three) and join
    without a step. Returns paths of the aligned copies."""
    bands = [wall_band(p) for p in paths]
    H = bands[0][0]
    t = round(sum(b[1] for b in bands) / len(bands))
    k = round(sum(b[2] for b in bands) / len(bands))
    out = []
    for p, (h, top, skirt) in zip(paths, bands):
        im = Image.open(p).convert('RGB')
        im = im.resize((im.width, h * H // h)) if h != H else im
        parts = [(0, top, t), (top, skirt, k - t), (skirt, h, H - k)]
        cv = Image.new('RGB', (im.width, H))
        y = 0
        for y0, y1, nh in parts:
            cv.paste(im.crop((0, y0, im.width, y1)).resize((im.width, nh), Image.LANCZOS), (0, y))
            y += nh
        q = os.path.join(HERE, 'final', os.path.basename(p).replace('.png', '_aligned.png'))
        cv.save(q)
        out.append(q)
        print('  aligned %s: ceiling %d->%d, skirting %d->%d' % (os.path.basename(p), top, t, skirt, k))
    return out


def build_lab():
    panels = [os.path.join(RAW, 'olab_p%d.png' % i) for i in (1, 2, 3)]
    tmp = os.path.join(HERE, 'final', 'bg_olab_full.png')
    os.makedirs(os.path.dirname(tmp), exist_ok=True)
    lp.do_panorama(align_panels(panels), tmp)
    pano = Image.open(tmp)
    half = pano.width // 2
    for suf, box in (('a', (0, 0, half, pano.height)), ('b', (half, 0, half * 2, pano.height))):
        out = pano.crop(box)
        assert out.width <= 4096
        out.save(os.path.join(SPR, 'bg_olab_%s.png' % suf), optimize=True)
        print('wrote bg_olab_%s %s' % (suf, out.size))


def main():
    names = sys.argv[1:] or ['oriane_sheet', 'oriane_bike', 'tile_simu', 'simu_leg', 'bg_simu_far', 'bg_simu_mid',
                             'tile_sol_simu', 'olab', 'tile_sol_olab', *jb.SCREENS]
    have = lambda n: os.path.exists(os.path.join(RAW, n + '.png'))
    for n in names:
        if n == 'olab':
            if all(have('olab_p%d' % i) for i in (1, 2, 3)): build_lab()
            else: print('skip olab (panels missing)')
            continue
        if not have(n):
            print('skip (no raw)', n); continue
        if n == 'oriane_sheet': build_hero()
        elif n == 'oriane_bike': build_bike()
        elif n == 'tile_simu': build_cap(n)
        elif n == 'simu_leg': build_leg(n)
        elif n.startswith('tile_sol_'): build_floor(n)
        elif n in jb.BANDS: jb.build_band(n)
        elif n in jb.SCREENS: jb.build_screen(n)


if __name__ == '__main__':
    main()
