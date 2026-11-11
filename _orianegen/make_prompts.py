#!/usr/bin/env python3
"""Codex (image_gen) prompts for the ORIANE campaign -> prompts/<name>.txt (+ .refs).

Same contract as _javagen / _marcosskingen: ONE image_gen per codex session,
SEQUENTIAL (run.sh), raw copied to raw/<name>.png, then build.py cuts /
chroma-keys / rescales into assets/sprites/ at the sizes of existing analogues:

  oriane_sheet       4x4 hero sheet (idle/throw/run/jump/hurt/dash/duck/ko) -> oriane_<state>.png (224 cells)
  oriane_bike        4 frames, Oriane on her bike with the 8-ball helmet      -> oriane_bike.png (224 cells)
  oriane_bike_cannon same sheet + CHILI CANNON on the handlebars (ref = raw oriane_bike) -> oriane_bike.png
  tile_simu          144x88  (= tile_panel)  floating code-window platform cap
  simu_leg           96x48   (= panel_leg)   glowing data-beam leg
  bg_simu_far        960x480 (= bg_mountains) far band: giant screens / code skyline
  bg_simu_mid        2027x370 (= bg_field)   near band: wireframe crop simulation plots
  tile_sol_simu      224x296 (= tile_sol_labo) digital floor tile
  olab_p1..p3        indoor lab panels -> panorama bg_olab_a / bg_olab_b (2 halves <= 4096 px)
  tile_sol_olab      224x296 lab corridor floor
  bg_oriane_map      1920x1056 jpg, bg_oriane_chapter / bg_oriane_win 1672x941 jpg

REFS (-i): files of refs/ (resized photos + copies of existing sprites; gitignored).
Usage: python _orianegen/make_prompts.py [name ...]; bash _orianegen/run.sh [name ...]; python _orianegen/build.py [name ...]
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'raw').replace(os.sep, '/')
OUT = os.path.join(HERE, 'prompts')

HEAD = ('Use your built-in image_gen tool (the "imagegen" skill) to GENERATE raster pixel art. Do NOT use the CLI '
        'fallback (no OPENAI_API_KEY). Do NOT draw procedurally (no PIL/SVG/canvas). The artwork MUST come from your '
        'AI image generator. Generate exactly ONE image (ONE image_gen call).\n\n')

PIX = ('STYLE: retro 16-bit SNES pixel art matching a cute cartoon run-and-gun platformer. Crisp visible square pixels, '
       'bold dark outlines, limited vibrant palette, flat cel shading, chunky readable shapes. NO smooth gradients, NO '
       'anti-aliasing, NO 3D render, NO painterly/airbrushed look, NO photo-realism.\n\n')

MAGENTA = ('BACKGROUND: fill the ENTIRE image (including every gap) with ONE perfectly FLAT solid #ff00ff magenta. NO '
           'shadow, NO contact shadow, NO floor line, NO gradient, NO grid lines, NO frame numbers, NO text, NO labels, '
           'NO watermark. NEVER use magenta or pink anywhere on the subject.\n\n')

# v2 (2026-11-12): finer pixel art (Laura / Marcos level) + a colourful outfit.
HERO_PIX = ('STYLE (CRITICAL): EXACTLY the same art style and PIXEL DENSITY as the two existing heroes of the game '
            '(Laura and Marcos, attached): richly shaded, finely detailed, crisp high-resolution 16-bit pixel art with '
            'SMALL pixels, soft multi-tone cel shading on skin, hair and fabric, subtle highlights, thin dark outlines, '
            'many readable details (fabric folds, hair strands, shoe laces, buckles). NOT chunky, NOT low resolution, '
            'NO big blocky pixels, NO thick black outlines, NO flat 4-colour shading, NO 3D render, NO photo-realism.\n\n')

ORIANE = ('ORIANE (the playable heroine, a PhD student in crop modelling): a young woman in her twenties, fair skin, '
          'LONG wavy LIGHT-BROWN / chestnut hair with lighter sun-kissed ends falling well below the shoulders, soft '
          'middle parting, blue-grey eyes, a big warm open smile, friendly oval face (keep her recognizable from the '
          'photos). COLOURFUL OUTFIT: a flowy CHILI-RED boho blouse with a small GOLDEN paisley pattern (like the red '
          'patterned blouse in her photo), sleeves rolled to the elbows, a slim brown belt, bright TURQUOISE / teal '
          'trousers rolled up at the ankle, SUNNY-YELLOW sneakers with white soles, a small tan leather crossbody '
          'satchel with a tiny red chili-pepper charm.')

# v3 (2026-11-12): the v2 sheet had realistic, tall adult proportions; the game's heroes are CARTOON.
LAURA_PROPS = ('PROPORTIONS (CRITICAL, the main point of this sheet): EXACTLY the same CARTOON body proportions as LAURA '
               '(attached): a BIG HEAD (about one third of the total body height, roughly 3 heads tall in total), large '
               'expressive eyes, a small nose, a SHORT compact torso, SHORT legs, small hands and feet with slightly '
               'chunky sneakers, a cute rounded silhouette, the same overall height-to-width ratio as Laura. Oriane '
               'must look like Laura\'s sister character drawn by the same artist, standing next to her at the same '
               'scale. NOT realistic proportions, NOT a tall slim adult with long legs, NOT a small head, NOT a fashion '
               'figure. Her long hair is drawn big and voluminous like Laura\'s ponytail is.\n\n')

SCENE = ('STYLE: retro 16-bit pixel art, cozy and CUTE storybook warmth (LucasArts / SNES adventure vibe), crisp visible '
         'square pixels, bold dark outlines, limited vibrant palette, flat cel shading, soft chunky readable shapes. '
         'NO smooth gradients, NO 3D render, NO painterly/airbrushed look, NO photographic realism.\n\n'
         'FORMAT: ONE wide LANDSCAPE illustration, full-bleed, filling the ENTIRE frame edge to edge (a full-screen GAME '
         'BACKGROUND: no padding, no border, NO magenta anywhere). The very top ~8% and bottom ~8% may be cropped.\n\n')

BAND = ('FORMAT (CRITICAL): a WIDE horizontal PANORAMA STRIP for a side-scrolling PARALLAX background layer, seen '
        'straight from the SIDE (side elevation, like a stage backdrop). The scenery sits in the LOWER part of the '
        'image and runs across the FULL WIDTH, continuing straight off BOTH the left and the right edges (it will be '
        'tiled horizontally: no frame, no vignette, nothing that ends at the sides, keep the left and right edges '
        'similar in height and color). Everything ABOVE the scenery must be ONE perfectly FLAT solid #ff00ff magenta '
        '(chroma-key). NEVER use magenta or pink in the scenery itself. NO people, NO watermark.\n\n')

DIGITAL = ('SETTING: a VIRTUAL CROP-SIMULATION WORLD inside a computer: everything is made of glowing PIXELS and '
           'VOXELS, a deep navy / midnight-blue cyber palette with bright CYAN, LIME-GREEN and AMBER neon accents, '
           'thin glowing grid lines, floating code fragments. It must evoke CROP MODELLING (a soil-crop simulator): '
           'pixelated WHEAT and MAIZE plants drawn as stepped green voxel stacks, growth CURVES and line charts, '
           'soil layers shown as a striped cross-section, little water-drop and nitrogen icons, weather icons.\n\n')

LAB = ('STYLE (CRITICAL, match this game\'s other indoor backgrounds: rich, detailed, busy 16-bit interiors): retro 16-bit '
       'pixel-art, classic LucasArts "Monkey Island" / SCUMM adventure-game vibe, cozy and CUTE, crisp visible square '
       'pixels, BOLD dark outlines, limited palette, flat cel shading, chunky readable shapes, a touch of humour. NO smooth '
       'gradients, NO 3D render, NO painterly look, NO photographic realism.\n\n'
       'PLACE: the real CIRAD research-unit CORRIDOR shown in the attached PHOTOS (redraw it as pixel art, keep its real '
       'look): long hallway with a white suspended ceiling and long fluorescent strip lights on a metal rail, pale cream '
       'walls, ORANGE / salmon door frames and orange doors, small square beige-white mosaic FLOOR TILES, colourful '
       'scientific POSTERS on the walls.\n\n'
       'SHARED VERTICAL LAYOUT (IDENTICAL in every panel so they line up; a corridor wall seen FLAT FROM THE SIDE like a '
       'SCUMM room, floor-to-CEILING, about 3:2 landscape): TOP ~16% = white drop CEILING with fluorescent strip lights '
       '(keep the very top corners calm, a HUD is drawn over them); MIDDLE ~58% = the wall with the furniture described '
       'below; BOTTOM ~26% = the small square beige mosaic tile floor meeting a thin grey skirting.\n\n'
       'SEAMLESS JOIN (CRITICAL): panels butt together left-to-right. At each panel\'s far-left ~8% and far-right ~8% show '
       'ONLY PLAIN cream wall + the same ceiling and floor (nothing crossing a side edge). NO people, NO legible text '
       '(posters show only colourful charts, plant images and blocks of unreadable squiggles).\n\n')

TAIL = ('After image_gen returns, copy ONLY the PNG created by THIS Codex session to:\n  {raw}/{name}.png\n'
        'CRITICAL: do NOT select "the newest PNG" globally from ~/.codex/generated_images. Use only the generated_images '
        'subdirectory for YOUR OWN Codex session id, or otherwise verify the file was produced by your own image_gen '
        'call. If you cannot identify it unambiguously, print FAIL_UNSAFE_COPY instead.\n'
        'Do NOT run chroma-key removal, do NOT delete files. Finally print exactly:\n  RAW: {raw}/{name}.png (<W>x<H>)\n')

ASSETS = {
 # ------------------------------------------------------------------ hero
 'oriane_sheet': (['hero_idle.png', 'hero_run.png', 'oriane_smile.png', 'oriane_face.png', 'oriane_body.png'],
   HEAD + HERO_PIX.replace('the two existing heroes of the game (Laura and Marcos, attached)',
                           'LAURA, the existing heroine of the game (attached)') + LAURA_PROPS +
   'ATTACHED IMAGES: images 1-2 are sprite strips of LAURA, the existing heroine of this game (idle and run): they '
   'are THE reference for art STYLE, PIXEL DENSITY, SHADING and above all body PROPORTIONS (match them closely; do not '
   'copy her face, blonde hair, cat or clothes). Images 3-5 are PHOTOS of the real person to turn into the new hero: '
   'FACE and HAIR identity only (ignore her clothes in the photos except the red patterned blouse idea).\n\n'
   + ORIANE + '\n\n'
   'Draw her in STRICT RIGHT-FACING SIDE PROFILE in every frame: nose, chest, knees and toes point RIGHT, one visible '
   'eye, hair flowing behind her (not a frontal face pasted on a sideways body).\n\n'
   'LAYOUT (critical): ONE SQUARE sheet, EXACTLY 4 columns by 4 rows, sixteen equally sized square cells (no grid lines '
   'drawn). Each cell contains exactly ONE full-body pose, centered horizontally, the standing figure about 80% of the '
   'cell height, the SAME character size in all cells, feet on the SAME low baseline, clear empty space around every '
   'figure, nothing crossing into a neighbour cell. Same face, hair, outfit and colours in all cells.\n'
   'Exact cells, left to right:\n'
   'Row 1: idle neutral; idle slight breathing; THROW wind-up: right arm pulled back holding a small bright RED CHILI '
   'PEPPER; THROW release: arm extended forward to the RIGHT, the red chili just leaving her hand.\n'
   'Row 2: four distinct RUNNING cycle frames facing right (long right-leg stride; passing pose; long left-leg stride; '
   'opposite passing pose), hair bouncing.\n'
   'Row 3: jump rising knees bent; jump descending legs extended; HURT recoil still facing right; forward-leaning DASH '
   'to the right.\n'
   'Row 4: half crouch facing right; deep crouch facing right; knocked out lying horizontally on the ground head to the '
   'right; second settled knocked-out pose head to the right.\n\n' + MAGENTA),
 'oriane_bike': (['oriane_sheet.png', 'hero_bike.png'],
   HEAD + PIX +
   'The FIRST attached image is the sprite sheet of ORIANE, the heroine: reproduce her EXACTLY (same face, long wavy '
   'light-brown hair, black hoodie, blue jeans, white sneakers, same pixel style and size). The SECOND attached image '
   'shows how ANOTHER hero rides a bike in this game: layout / scale reference only.\n\n'
   'SUBJECT: Oriane RIDING a black city BICYCLE (black frame, a small rear rack with a red rear light, thin black '
   'wheels), in STRICT RIGHT-FACING SIDE PROFILE, leaning forward happily, pedalling. She wears a round glossy BLACK '
   'helmet painted exactly like a BILLIARD 8-BALL: shiny black dome with a white circle on its side containing a black '
   'number "8" (the only text allowed), her long hair flowing out behind under it.\n\n'
   'LAYOUT (critical): EXACTLY 4 frames in a SINGLE horizontal row, a uniform grid of 4 equal square cells, the bike '
   'and rider at the SAME scale with both wheels on the SAME baseline near the bottom of every cell, centered, a WIDE '
   'empty gap between frames (frames never touch). Only the pedals, legs and a slight bob change across the 4 frames '
   '(one smooth pedalling loop).\n\n' + MAGENTA),
 # Oriane (v2 outfit, fine pixel art) on her bike WITH the CHILI CANNON on the handlebars (her chili peppers
 #  come out of it on the bike). Refs: the v2 hero sheet (identity / style), Laura's bike sheet (style + scale),
 #  the v1 cannon bike (layout + cannon design only).
 'oriane_bike_cannon': (['oriane_sheet.png', 'hero_bike.png'],
   HEAD + HERO_PIX.replace('the two existing heroes of the game (Laura and Marcos, attached)',
                           'LAURA, the existing heroine of the game (attached)') + LAURA_PROPS +
   'ATTACHED IMAGES: image 1 is the sprite sheet of ORIANE, the heroine: reproduce her EXACTLY (same face, hair, '
   'cartoon proportions, chili-red paisley blouse, turquoise trousers, yellow sneakers, satchel, same pixel style and '
   'density). Image 2 shows LAURA riding her bike in this game: THE reference for the BIKE SIZE, the rider SCALE and '
   'the composition. Copy it closely.\n\n'
   'SCALE (CRITICAL, the main point of this sheet): Oriane on the bike must keep EXACTLY the SAME size and cartoon '
   'proportions as when she stands in image 1: the SAME big head size, the same short limbs. The bike is a SMALL, '
   'COMPACT cartoon bike sized for her, exactly like Laura\'s in image 2: SMALL wheels (each wheel about as tall as '
   'her leg from knee to sole, roughly one quarter of the total height), a short low frame. The whole group (helmet '
   'top to wheel bottom) is only about as tall as Oriane standing. NOT a big adult city bike with large wheels, NOT a '
   'small rider on a big bike.\n\n'
   'SUBJECT: Oriane RIDING her compact BLACK bike (glossy black frame, a tiny rear rack with a red rear light, small '
   'black wheels with fine spokes), in STRICT RIGHT-FACING SIDE PROFILE, leaning forward happily, pedalling. She wears '
   'a round glossy BLACK helmet painted exactly like a BILLIARD 8-BALL: shiny black dome with a white circle on its '
   'side containing a black number "8" (the only text allowed), her long wavy light-brown hair flowing out behind '
   'under it.\n\n'
   'LAYOUT (critical): EXACTLY 4 frames in a SINGLE horizontal row, a uniform grid of 4 equal square cells, the bike '
   'and rider at the SAME scale with both wheels on the SAME baseline near the bottom of every cell, centered, a WIDE '
   'empty gap between frames (frames never touch). Only the pedals, legs and a slight bob change across the 4 frames '
   '(one smooth pedalling loop).\n\n'
   'CHILI CANNON, identical in all 4 frames: a small cartoon CHILI CANNON bolted on the front of the bike, on a little '
   'metal bracket on the handlebar stem just in front of her hands. The cannon is a short stubby barrel shaped like a '
   'big glossy RED CHILI PEPPER lying horizontally, with its green stem cap and a little brass ring at the BACK (near '
   'her hands) and a dark round open MUZZLE pointing straight FORWARD to the RIGHT, perfectly horizontal, at the '
   'height of the handlebars. A couple of tiny red chili peppers peek out of a small ammo box clipped under it. Keep '
   'the cannon COMPACT: its muzzle sticks out only slightly beyond the front edge of the front wheel (scaled to the small bike). It must look '
   'like part of the bike (same outline, same palette, same light), clearly readable at small size.\n\n' + MAGENTA),
 # ------------------------------------------------------------------ level 2: simulation world
 'tile_simu': (['tile_panel.png'], HEAD + PIX + DIGITAL + MAGENTA.replace('every gap', 'around the object') +
   'The ATTACHED image is the GEOMETRY reference: a game platform tile (a tilted solar panel seen in side/3-4 '
   'perspective: a flat parallelogram leaning back toward the upper-left, front edge horizontal at the bottom).\n\n'
   'SUBJECT: redraw that EXACT SAME platform shape, angle, proportions and framing, but as a floating SOFTWARE WINDOW '
   'panel of the simulation world: a dark navy glass slab with a glowing CYAN neon border, a tiny title bar with three '
   'little dots, rows of tiny lime-green and amber CODE lines (unreadable squiggles) and a mini green growth curve on '
   'its face. Along the bottom FRONT edge a thick bright cyan glowing ledge (the edge the hero stands on). ONE single '
   'object, centered, filling about 80% of the width.\n\n'),
 'simu_leg': (['panel_leg.png'], HEAD + PIX + DIGITAL + MAGENTA.replace('every gap', 'around the object') +
   'SUBJECT: ONE single straight VERTICAL glowing DATA BEAM (a structural leg holding a floating software panel): a '
   'thin translucent-looking column of stacked cyan and lime-green PIXEL blocks with a bright core line, a few tiny '
   '0/1 bits drifting inside, perfectly vertical and centered, spanning the FULL HEIGHT of the image (top and bottom '
   'cut flat). About 1/8 of the image width. Plain, no base.\n\n'),
 'bg_simu_far': ([], HEAD + PIX + BAND + DIGITAL +
   'SCENERY: the FAR distance layer: a skyline of GIANT glowing MONITOR SCREENS and SERVER TOWERS standing like '
   'buildings, the screens showing big pixelated crop growth curves, leaf-area bar charts and a voxel maize plant, '
   'columns of falling green code, blinking LEDs, all slightly hazy and darker blue (it is far away). The scenery '
   'occupies the lower ~65% of the image; the bottom ~25% is a SOLID band of dark navy grid ground that reaches the '
   'bottom edge.\n\n'),
 'bg_simu_mid': ([], HEAD + PIX + BAND + DIGITAL +
   'SCENERY: the NEAR layer: a LOW strip of VIRTUAL EXPERIMENTAL FIELD PLOTS: neat rows of pixelated voxel WHEAT, MAIZE '
   'and LEGUME plants (an intercrop: two crops alternating), some drawn as glowing cyan WIREFRAME plants still being '
   'computed, little floating labels as unreadable squiggles, a soil cross-section with stripes below them, small '
   'glowing weather-station poles, a few corrupted glitchy pixel blocks. Keep it LOW and wide: everything fits in the '
   'bottom ~35% of the image, the rest above is flat magenta. The bottom edge is solid dark navy soil grid.\n\n'),
 'tile_sol_simu': ([], HEAD + PIX + DIGITAL +
   'SUBJECT: the seamless GROUND TILE the hero walks ON TOP of in the simulation world. TOP ~22% = the walkable '
   'SURFACE: a dark navy glass floor with a glowing CYAN grid, seen in a shallow top-down tilt, with a CLEAN STRAIGHT '
   'HORIZONTAL TOP EDGE (nothing sticking up). BOTTOM ~78% = the FRONT FACE of the ground block: a cross-section of '
   'SOIL LAYERS drawn as stacked pixel strata (dark brown, ochre, grey) with thin cyan data lines and tiny glowing '
   'roots, bold dark outline along the VERY BOTTOM. TILEABLE: repeats seamlessly left-right, uniform flat lighting, '
   'no unique feature, no text. A roughly SQUARE image, full-bleed, NO magenta, NO transparency, NO border.\n\n'),
 # ------------------------------------------------------------------ level 3: the lab corridor (photos)
 'olab_p1': (['lab2.jpg', 'lab3.jpg'], HEAD + LAB +
   'THIS PANEL (left part of the corridor): the POSTER corridor of the attached photos: three big colourful scientific '
   'POSTERS pinned on the cream wall (one black poster with a glowing rainbow heat-map circle, one white poster with '
   'orange tables and charts, one dark poster with a pixel plant anatomy diagram), an orange door frame with an open '
   'orange door, a plain fire extinguisher, a light switch.\n\n'),
 'olab_p2': (['lab1.jpg', 'olab_p1.png'], HEAD + LAB +
   'The SECOND attached image is the panel just to the LEFT of this one: match its palette, outline weight, ceiling, '
   'wall and floor EXACTLY.\n\n'
   'THIS PANEL (middle): the KITCHENETTE / coffee corner of the FIRST attached photo: a white cabinet with a rolling '
   'shutter and a round counter, a MICROWAVE covered in fridge magnets, a red electric kettle and a coffee pod '
   'machine on a small FRIDGE covered in magnets and postcards, a blue WATER COOLER bottle on a black dispenser, a '
   'wooden bar STOOL, paper bags on the floor, a string of small warm fairy lights on the wall, a big number 4 on '
   'the wall.\n\n'),
 'olab_p3': (['lab4.jpg', 'lab5.jpg', 'olab_p1.png'], HEAD + LAB +
   'The THIRD attached image is another panel of the SAME corridor: match its palette, outline weight, ceiling, wall '
   'and floor EXACTLY.\n\n'
   'THIS PANEL (right part): from the first photo, a tall dark BROWN metal CABINET with a glass sliding door full of '
   'books and a cream rolling shutter, with an Indonesian wayang puppet, a lime-green watering can, a small potted '
   'plant and a toy white vintage 2CV car standing on top; from the second photo, seen through a wide open office '
   'doorway: a light wooden DESK with potted plants (an amaryllis, a pothos in a jar), a black monitor, a PURPLE '
   'office chair and shelves of blue and red binders.\n\n'),
 'tile_sol_olab': (['lab2.jpg', 'olab_p1.png'], HEAD + PIX +
   'SUBJECT: the seamless FLOOR TILE of that same corridor (the second attached image is the matching background: '
   'use EXACTLY its floor colours): small square beige / off-white MOSAIC floor tiles with grey grout. TOP ~22% = the '
   'walkable SURFACE (mosaic seen in a shallow top-down tilt, CLEAN STRAIGHT HORIZONTAL TOP EDGE). BOTTOM ~78% = the '
   'solid FRONT FACE (a grey skirting over a darker beige tiled front, bold dark outline along the VERY BOTTOM). '
   'TILEABLE left-right, uniform flat lighting, no unique feature, no text. Roughly SQUARE, full-bleed, NO magenta, NO '
   'transparency, NO border.\n\n'),
 # ------------------------------------------------------------------ screens
 'bg_oriane_map': (['lab2.jpg', 'intercrop.png'], HEAD + SCENE +
   'SCENE: a cute TOP-DOWN WORLD MAP (bird\'s-eye view, like a classic 16-bit overworld map) of Oriane\'s PhD journey '
   'around Montpellier (south of France). A winding sandy DIRT PATH goes from the LOWER-LEFT, through the CENTER, to the '
   'UPPER-RIGHT. Along it, three clear empty round flat CLEARINGS (where level markers will be drawn, keep them plain '
   'and uncluttered): one at about 20% from the left / 72% from the top beside a small old APARTMENT building with a '
   'red-tiled roof and a bicycle parked in front; one at about 49% from the left / 57% from the top inside a strange '
   'square zone where the landscape turns into glowing blue PIXEL GRID with giant voxel maize plants and a computer '
   'screen (the virtual crop simulation); one at about 79% from the left / 44% from the top in front of a long white '
   'research INSTITUTE building with orange doors and experimental INTERCROP fields (alternating stripes of wheat '
   'and peas). Olive trees, oleander bushes, vineyards and garrigue everywhere else, a strip of blue Mediterranean '
   'sea in the top-left corner. NO text, NO labels, NO signs, NO numbers.\n\n'),
 'bg_oriane_chapter': (['lab5.jpg'], HEAD + SCENE +
   'SCENE: a cosy place to write a thesis chapter: a research office desk (light wooden desk like the attached photo) '
   'seen from the side, a laptop showing a green crop growth curve from a simulation, a big jar of PEANUT BUTTER with '
   'a spoon in it, a small bowl of bright red CHILI peppers, potted plants (a pothos in a jar, an amaryllis), a '
   'purple office chair, a black bicycle helmet painted like a billiard 8-ball resting on a pile of papers, a window '
   'with the afternoon Mediterranean sun. Calm, warm, inviting. NO people, NO text, NO legible writing (the only '
   'allowed mark is the white circle with an "8" on the helmet).\n\n'),
 'bg_oriane_win': (['intercrop.png'], HEAD + SCENE +
   'SCENE: a joyful PhD CELEBRATION in experimental INTERCROP fields (stripes of golden wheat alternating with green '
   'peas) at golden hour: many black graduation CAPS (mortarboards with golden tassels) thrown high up into the air, '
   'golden CONFETTI, a few flying red CHILI peppers and sparkles raining down, a thick bound thesis book, a jar of '
   'peanut butter and a black 8-ball bicycle helmet resting on a wooden bench in the lower center, olive trees and a '
   'warm golden sky with a big friendly sun. Keep the UPPER THIRD calm (soft sky, few sparkles) for a title overlay. '
   'NO people, NO faces, NO text, NO letters.\n\n'),
}

if __name__ == '__main__':
    only = set(sys.argv[1:])
    os.makedirs(OUT, exist_ok=True)
    for name, (refs, body) in ASSETS.items():
        if only and name not in only:
            continue
        p = os.path.join(OUT, name + '.txt')
        open(p, 'w', encoding='utf-8').write(body + TAIL.format(raw=RAW, name=name))
        with open(os.path.join(OUT, name + '.refs'), 'wb') as f:   # LF only (read by bash)
            f.write(('\n'.join(refs) + '\n').encode('utf-8'))
        print('wrote', p, 'refs:', ', '.join(refs) or '-')
