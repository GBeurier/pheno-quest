#!/usr/bin/env python3
"""Post-process the ORIANE campaign icons: raw/ magenta -> assets/sprites.

Reuses build_marcos.py helpers (chroma key, ammo wobble sheet, haloed shot):
  ammo_chili / ammo_chili_fire  6 frames 52 / 56   (= ammo_graine / _fire)
  ammo_pbjar / shot_darkjar     1 frame 80x80      (round, spun by the engine)
  shot_*                        1 frame 96x96      (pointing RIGHT, dark halo)
Idempotent: only processes raws that exist. Then: python gen_assets_data.py
"""
import os
from PIL import Image
from build_marcos import RAW, CUT, OUT, key, fit, build_ammo, build_shot

AMMO = {'ammo_chili': 52, 'ammo_chili_fire': 56}
ROLLERS = ['ammo_pbjar', 'shot_darkjar']
SHOTS = ['shot_packet', 'shot_nitrogen', 'shot_darkchili', 'shot_doubt']


def build_roller(name, cell=80, fill=0.92):
    icon = fit(key(name), round(cell * fill))
    cv = Image.new('RGBA', (cell, cell), (0, 0, 0, 0))
    cv.alpha_composite(icon, ((cell - icon.width) // 2, (cell - icon.height) // 2))
    cv.save(os.path.join(OUT, name + '.png'))
    return cv.size


def main():
    os.makedirs(CUT, exist_ok=True)
    have = lambda n: os.path.exists(os.path.join(RAW, n + '.png'))
    for n, c in AMMO.items():
        if have(n): print(n, build_ammo(n, c), '6 frames')
    for n in ROLLERS:
        if have(n): print(n, build_roller(n), '1 frame')
    for n in SHOTS:
        if have(n): print(n, build_shot(n), '1 frame')


if __name__ == '__main__':
    main()
