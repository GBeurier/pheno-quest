"""raw/<name>.png -> assets/sprites/<name>.jpg (cover-crop to the screen size).
Usage: python _wingen/build.py [name ...]  then  python gen_assets_data.py
"""
import os
import sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'assets', 'sprites')
SCREENS = {'bg_oriane_win': (1672, 941), 'bg_marcos_win': (1672, 941)}


def build(name):
    W, H = SCREENS[name]
    im = Image.open(os.path.join(HERE, 'raw', name + '.png')).convert('RGB')
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    dst = os.path.join(OUT, name + '.jpg')
    im.crop((x, y, x + W, y + H)).save(dst, quality=92)
    print('OK', dst)


if __name__ == '__main__':
    for n in sys.argv[1:] or list(SCREENS):
        if os.path.exists(os.path.join(HERE, 'raw', n + '.png')):
            build(n)
        else:
            print('skip (no raw)', n)
