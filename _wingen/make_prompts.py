"""Emit the Codex image_gen prompts for the Marcos / Oriane victory screens.

Each screen = the character's existing victory background (bench + props)
re-done with the hero JUMPING FOR JOY in the centre, in a graduation gown and
mortarboard, like Laura's bg_win. Refs (-i, listed in prompts/<name>.refs):
  1. the current background to keep (bg_<who>_win)
  2. the in-game sprite of the hero (identity: hair, face, clothes)
  3. Laura's bg_win (pose / gown / cap / framing reference only)
Usage: python _wingen/make_prompts.py ; bash _wingen/run.sh ; python _wingen/build.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE).replace('\\', '/')

HEAD = (
    'Use your built-in image_gen tool (the "imagegen" skill) to GENERATE raster pixel art. '
    'Do NOT use the CLI fallback (no OPENAI_API_KEY). Do NOT draw procedurally (no PIL/SVG/canvas). '
    'The artwork MUST come from your AI image generator. Generate exactly ONE image (ONE image_gen call), '
    'passing ALL the attached reference images to image_gen as references.\n\n'
    'STYLE: retro 16-bit pixel art, cozy and CUTE storybook warmth (LucasArts / SNES adventure vibe), crisp '
    'visible square pixels, bold dark outlines, limited warm vibrant palette, flat cel shading, soft chunky '
    'readable shapes. Match the look of the attached backgrounds exactly. NO smooth gradients, NO 3D render, '
    'NO painterly look, NO photographic realism.\n\n'
    'FORMAT: ONE wide LANDSCAPE illustration (16:9), full-bleed, filling the ENTIRE frame edge to edge '
    '(a full-screen GAME BACKGROUND: no padding, no border, NO magenta anywhere).\n\n'
)

WHO = {
    'bg_oriane_win': dict(
        refs=['bg_oriane_win.png', 'oriane_idle.png', 'oriane_face.png', 'bg_win.png'],
        hero=('ORIANE, the young woman PhD student shown in the attached game sprite and face reference: very long '
              'wavy auburn-brown hair, warm smile, red-orange patterned blouse, teal rolled-up jeans, yellow '
              'sneakers, a brown shoulder bag with a small red chili pepper charm. Keep her face, hair and colours '
              'recognisable'),
        props='the thesis book, the jar of peanut butter and the black bicycle helmet on the wooden bench',
        extra='a few red chili peppers fly among the confetti and thrown caps',
    ),
    'bg_marcos_win': dict(
        refs=['bg_marcos_win.png', 'marcos_idle.png', 'bg_win.png'],
        hero=('MARCOS, the young man PhD student shown in the attached game sprite: dark curly hair tied in a top '
              'bun, full dark beard, warm brown skin, big smile, green plaid shirt, khaki trousers, brown boots, '
              'a brown backpack. Keep his face, hair, beard and colours recognisable'),
        props='the acoustic guitar and the thesis book on the bamboo bench',
        extra='keep the bamboo shade nets, rice paddies and the blue volcano',
    ),
}


def prompt(name, d):
    return HEAD + (
        'REFERENCES: image 1 is the CURRENT background of this screen: KEEP its setting, palette, sky, sun, '
        'trees, fields and thrown graduation caps almost identical. Image 2' +
        (' (and image 3)' if len(d['refs']) > 3 else '') +
        ' show the HERO to draw. The LAST image is another character\'s victory screen, used ONLY as a reference '
        'for the pose, the outfit (black academic gown + mortarboard), the size and the framing: do NOT copy '
        'that girl, her cat, the solar panels or the rice.\n\n'
        'SCENE: the same joyful PhD graduation celebration at golden hour, now with the hero in it. In the CENTRE '
        'of the image, ' + d['hero'] + '. The hero is JUMPING FOR JOY, both feet off the ground, legs tucked, '
        'both arms raised high, one hand triumphantly holding up a thick bound thesis book, mouth wide open in a '
        'happy shout. The hero wears an OPEN black doctoral graduation GOWN with golden trim over the usual '
        'clothes and a black graduation CAP (mortarboard) with a golden tassel. The hero is BIG (about half of '
        'the image height), the head in the upper-middle part of the image, the whole body visible. '
        'Move ' + d['props'] + ' slightly aside or keep them small in the lower foreground so they do not hide '
        'the hero. Golden confetti, sparkles and thrown caps around; ' + d['extra'] + '. '
        'Keep the TOP ~12% calm (soft sky). Mood: festive, proud, heart-warming.\n\n'
        'NO text, NO letters, NO watermark, NO UI, NO frame, NO speech bubbles, only ONE person.\n\n'
        'After image_gen returns, copy ONLY the PNG created by THIS Codex session to:\n'
        '  ' + ROOT + '/_wingen/raw/' + name + '.png\n'
        'CRITICAL: do NOT select "the newest PNG" globally from ~/.codex/generated_images. Use only the '
        'generated_images subdirectory for YOUR OWN Codex session id, or otherwise verify the file was produced '
        'by your own image_gen call. If you cannot identify it unambiguously, print FAIL_UNSAFE_COPY instead.\n'
        'Do NOT run chroma-key removal, do NOT delete files. Finally print exactly:\n'
        '  RAW: ' + ROOT + '/_wingen/raw/' + name + '.png (<W>x<H>)\n'
    )


def main():
    os.makedirs(os.path.join(HERE, 'prompts'), exist_ok=True)
    for name, d in WHO.items():
        with open(os.path.join(HERE, 'prompts', name + '.txt'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(prompt(name, d))
        with open(os.path.join(HERE, 'prompts', name + '.refs'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(d['refs']) + '\n')
        print('prompt', name)


if __name__ == '__main__':
    main()
