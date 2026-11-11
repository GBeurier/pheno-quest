#!/usr/bin/env python3
"""Codex (image_gen) prompts for the ORIANE campaign icons -> prompts_oriane/<name>.txt.

Same style contract as make_prompts_marcos.py (shared PRE / SHOT text). Then
_icongen/build_oriane.py builds the sheets:
  ammo_chili / ammo_chili_fire -> 6 frames 52 / 56 (= ammo_graine / _fire)
  ammo_pbjar / shot_darkjar    -> 1 frame 80x80, rotated by the engine while rolling
  shot_*                       -> 1 frame 96x96, pointing RIGHT, dark halo (= shot_error)
Usage: python _icongen/make_prompts_oriane.py ; bash _icongen/run_oriane.sh [name ...]
"""
import os
from make_prompts_marcos import PRE, SHOT, RAW, ROOT

OUT = os.path.join(ROOT, '_icongen', 'prompts_oriane')
PRE_O = PRE.replace('set in the rice fields of Java (Indonesia)', 'about a PhD student in crop modelling')

ROLL = ('\nThis object ROLLS along the ground like a wheel (the game spins it), so draw it as a compact, almost ROUND '
        'silhouette seen from the side, BOLD and readable at small size, very thick dark outline.')

ICONS = {
 'ammo_chili': ('75%', '\nThis is the hero\'s ammo: a hot CHILI PEPPER she throws. Compact, reads well while wobbling.',
   'ONE single glossy bright RED CHILI PEPPER (slightly curved, a short green stem and calyx), a white shine highlight, '
   'thick dark outline, a couple of tiny orange heat sparkles around it. Spicy and joyful.'),
 'ammo_chili_fire': ('75%', '\nThis is the hero\'s POWERED-UP ammo (level 3). Use the ATTACHED image as the exact reference: the '
   'SAME chili pepper, now ON FIRE.',
   'the SAME glossy red CHILI PEPPER as the attached reference, now wrapped in bright orange-and-yellow pixel FLAMES '
   'licking around it, a few embers, a glowing white-yellow hot core. Extremely spicy, still clearly a chili.'),
 'ammo_pbjar': ('80%', ROLL,
   'a chunky glass JAR of PEANUT BUTTER: a round squat jar full of creamy tan-brown peanut butter, a bright RED screw '
   'lid, a cute yellow label with a cartoon PEANUT drawing (no letters), a white glass shine highlight.'),
 'shot_packet': ('85%', SHOT,
   'a glowing DATA PACKET of a crop-simulation server: a small cyan-and-white glowing pixel CUBE with tiny binary 0 and 1 '
   'digits on its faces, crackling with electricity, a short cyan light trail behind it on the left.'),
 'shot_nitrogen': ('85%', SHOT,
   'a falling NITROGEN FERTILIZER drop: a fat glossy lime-green liquid DROPLET with a bold white capital letter N on '
   'it (the only letter allowed), a few small green droplets trailing behind.'),
 'shot_darkchili': ('85%', SHOT,
   'a CURSED dark CHILI PEPPER: a deep PURPLE-BLACK chili with a sickly violet glow and small dark smoke wisps, an angry '
   'little frown carved on it.'),
 'shot_darkjar': ('80%', ROLL,
   'a CURSED dark JAR of burnt peanut butter: a round squat jar full of nearly-black tar-like peanut butter, a dark '
   'PURPLE lid, a torn grey label with a sad scribble, a sickly violet glow around it.'),
 'shot_doubt': ('85%', SHOT,
   'a small dark STORM CLOUD OF DOUBT: a puffy charcoal-grey and violet cloud with a big white QUESTION MARK on it (the '
   'only symbol allowed) and a tiny lightning bolt below, drifting toward the right.'),
}

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, (fill, extra, subj) in ICONS.items():
        p = os.path.join(OUT, name + '.txt')
        open(p, 'w', encoding='utf-8').write(PRE_O.format(fill=fill, extra=extra, subj=subj, raw=RAW, name=name))
        print('wrote', p)
