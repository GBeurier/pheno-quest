#!/usr/bin/env python3
"""Emit per-boss image-generation prompts (pixel-art, 2 sheets each: move + atk)
into _bossgen/prompts/<boss>.txt.

Each prompt is intended for sequential built-in image_gen calls. Save raw strips
to _bossgen/raw/, then run regrid.py to normalize them into 6x 248x280 sheets.
"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace(os.sep, '/')  # racine du repo (portable)
OUT = os.path.join(ROOT, '_bossgen', 'prompts'); os.makedirs(OUT, exist_ok=True)

COMMON = """Use your built-in image_gen tool (the "imagegen" skill) to GENERATE raster artwork. Do NOT use the CLI fallback (no OPENAI_API_KEY). Do NOT draw procedurally (no PIL/canvas/SVG). The artwork MUST come from your AI image generator. You will generate TWO sprite sheets for one boss character.

PIXEL-ART STYLE (both sheets): {style}

LAYOUT for EACH sheet (critical): EXACTLY 6 frames in a SINGLE horizontal row, left to right, on a uniform grid of 6 equal cells. Same cell size for all; the character at the SAME scale, standing on the SAME ground baseline near the bottom of each cell; centered in its cell. Leave a WIDE empty magenta gap between consecutive frames (each frame a clearly separated island; frames MUST NOT touch or overlap; nothing crosses from one frame into a neighbour). Character identity, outfit and colors IDENTICAL across all 6 frames; only the POSE changes (one looping animation). The character FACES LEFT.

BACKGROUND (both sheets): fill the ENTIRE image (including the gaps) with ONE perfectly FLAT solid #ff00ff magenta. NO shadows, NO floor line, NO gradient, NO grid lines, NO frame numbers, NO text{textnote}, NO watermark. Never use magenta/pink on the character.

CHARACTER (identical in every frame of BOTH sheets):
{character}

SHEET 1 = MOVE/IDLE. 6 frames, facing LEFT: frames 1-5 a subtle looping IDLE/MENACE cycle ({idle}); frame 6 a HURT pose ({hurt}). cp the result to {root}/_bossgen/raw/{boss}_move_sheet.png

SHEET 2 = ATTACK. 6 frames, facing LEFT: an attack cycle -> {atk}. cp the result to {root}/_bossgen/raw/{boss}_atk_sheet.png

Generate SHEET 1 first (one image_gen call), cp it; then SHEET 2 (one image_gen call), cp it. Do NOT run chroma-key removal, do NOT delete files. Finally print exactly:
  MOVE: {root}/_bossgen/raw/{boss}_move_sheet.png (<W>x<H>)
  ATK:  {root}/_bossgen/raw/{boss}_atk_sheet.png (<W>x<H>)
"""

STYLE = ("retro 16-bit SNES / arcade run-and-gun look. Crisp visible square pixels, bold dark outline, limited "
         "vibrant palette, flat cel shading, chunky readable shapes. NO smooth gradients, NO anti-aliasing, NO "
         "airbrushed/painterly look, NO 3D.")
# finer variant (same level as the Laura / Marcos heroes and the Garuda / Tikus bosses): per-boss 'style'
FINE = ("richly shaded, finely detailed, crisp high-resolution 16-bit pixel art with SMALL pixels (the same pixel "
        "density as the attached game sprites), soft multi-tone cel shading on skin, hair and fabric, subtle highlights, "
        "thin dark outlines, many readable details. NOT chunky, NO big blocky pixels, NO thick black outlines, NO flat "
        "4-colour shading, NO 3D render, NO photo-realism.")

BOSSES = {
 'proprietaire': dict(
   character="FRANCOIS, a grumpy rural LANDOWNER / property boss, not a farmer. Short stocky middle-aged man with a big round pot belly, red scowling face, small slick hair, thin moustache, expensive BORDEAUX / burgundy suit straining over the belly, white shirt, dark shoes, gold watch, bunch of keys at the belt, holding a rolled property deed or land contract. Renfrogne, greedy, territorial, comedic villain.",
   idle="squaring his shoulders, belly jutting forward, jangling keys, glaring to the left",
   hurt="recoiling backward, belly bouncing, keys and deed flying up, eyes squeezed shut, impact stars",
   atk="frame1 stand, frames2-3 wind up with the rolled land contract and keys, frame4 thrust / shove the contract hard to the LEFT, frame5 shoulder-charge LEFT with belly first, frame6 recover"),
 'agriculteur': dict(
   character="A cocky MAFIA BOSS / mob 'don' riding the SAME rusty red TRACTOR, clearly the boss vehicle. HIS FACE MUST CLEARLY RESEMBLE THE ATTACHED REFERENCE PHOTO (a real man): olive / Mediterranean skin, SHORT SALT-AND-PEPPER hair (dark on top, grey at the temples) SLICKED BACK over a high receding forehead, dark thick eyebrows, dark eyes, clean-shaven, a confident MENACING SMIRK. NO hat at all (bare slicked hair). Dressed as a 1930s gangster / mafioso: dark charcoal PINSTRIPE three-piece suit with waistcoat, crisp white dress shirt, dark blood-red silk tie, gold pinky ring and watch chain, a thin cigar clenched in his teeth. NO straw hat, NO overalls, NO plaid shirt, NO work gloves. He sits high on the tractor, leaning left, sneering. TRACTOR (keep it the boss vehicle, unchanged from a classic farm tractor): rust-red body, black exhaust chimney / smokestack, two very large dark wheels with pale hubs, chunky fenders, small steering wheel, grime. Keep the tractor visible and dominant in every frame, and keep his face recognizable as the reference man in every frame.",
   idle="tractor chugging in place, big wheels rocking slightly, smokestack puffing, the mobster smirking, puffing his cigar and shaking a fist while facing left",
   hurt="tractor jolts backward, the mobster almost falls from the seat, cigar flying from his mouth, slicked hair coming loose, sparks and impact stars",
   atk="frame1 engine idles, frames2-3 tractor revs with smoke from the chimney, frame4 tractor lunges / rams to the LEFT, frame5 wheel spin and front grill thrust left, frame6 recover"),
 'michael': dict(
   character="MICHAEL based on the provided reference photo: an older bald man with a long oval bald skull, high forehead, no hair on top, short neat grey beard / stubble around jaw and chin, pale skin, narrow nose, serious eyes, wearing a plain RED t-shirt. No lab coat, no full white beard, no black hair. Comedic stern researcher villain, but the head silhouette must resemble the reference.",
   idle="standing tall in the red t-shirt, stern glare to the left, small breathing motion, one hand holding statistical notes",
   hurt="recoiling, bald head tilted back, grey beard visible, red shirt wrinkling, notes flying, impact stars",
   atk="frame1 stern stance, frames2-3 wind up with a statistical chart / graph sheet, frame4 fling the chart hard to the LEFT, frame5 point menacingly while data sheets fly left, frame6 recover"),
 'rstudio': dict(
   character="NOT a person: the RStudio software personified as a buggy computer-machine monster. A chunky retro monitor / CRT body with stubby arms and feet, angry glitchy face, teal/cyan casing, tangled cables. On the screen or chest is a VERY LARGE, CLEAR, READABLE RStudio logo: a bold WHITE capital letter R inside a vivid bright BLUE sphere / halo / roundel. The logo is the main identity and must stay legible in every frame. Tiny red Error popups may float near it.",
   idle="standing and leaning left, the big blue RStudio logo glowing clearly, screen flickering an angry face, small error popups blinking",
   hurt="screen cracking further with a static burst, sparks",
   atk="frame1 idle with big readable blue-and-white RStudio logo, frames2-3 screen charges up flashing red, frame4 spit jagged red Error popups / stack-trace blocks to the LEFT, frame5 more errors streaming left, frame6 settle with logo still readable",
   textnote=" (the exact white letter \"R\" inside the blue RStudio logo and tiny \"Error\" popups ARE allowed, since they are the character)"),
 'cendrine': dict(
   character="CENDRINE, a severe female administrative manager. Strict tight bun, sharp glasses, stern pursed mouth, beige tailored suit / tailleur beige with skirt and jacket, sensible shoes, several folders / dossiers tucked under one arm. Comedic bureaucratic boss, rigid posture, no purple outfit.",
   idle="standing rigid and disapproving, clutching folders under her arm, glaring left over her glasses",
   hurt="recoiling, glasses knocked askew, folders and papers puffing up, impact stars",
   atk="frame1 ready with folders under arm, frames2-3 pull a dossier / form from the stack, frame4 fling official folders and papers to the LEFT, frame5 point angrily left while papers scatter, frame6 recover"),
 'jury': dict(
   character=("THE THESIS JURY (final boss): a wide sprite showing THREE clearly DIFFERENT professors seated behind one long wooden defense table, the WHOLE panel shown in EVERY frame. LEFT: an older male professor with white hair and/or white beard, glasses, dark academic suit. MIDDLE: a severe woman professor with a tight bun, formal jacket, holding papers. RIGHT: a younger male professor with glasses, neat hair, skeptical expression, laptop or notebook. They sit shoulder-to-shoulder behind the long desk with paper stacks, water glasses, and a small lamp. Burgundy academic accents but no magenta/pink. Keep the three people and the bench identical in every frame; only gestures change."),
   idle="the three seated professors shuffling papers, leaning in, exchanging skeptical looks; attention toward the left",
   hurt="all three jolting back in their chairs, papers flying up",
   atk="frame1 seated, frames2-3 all three lean forward with documents raised, frame4 they fling papers / criticism sheets to the LEFT together, frame5 papers flying left across the desk, frame6 settle",
   facenote=" (a forward-facing panel is fine; angle their attention/gestures toward the left)"),
 # ---- CAMPAGNE MARCOS (Java) ----
 'tikus': dict(
   character="RAJA TIKUS, the RAT KING of the Javanese rice paddies: a GIANT fat rice-field rat standing semi-upright on its hind legs, scruffy grey-brown fur heavily caked with wet brown MUD on legs and belly, a small dented GOLD CROWN tilted on its head, a tattered red royal cape, huge yellow buck teeth, glowing red eyes, long thick bare grey tail, sharp claws, a few rice stalks stuck in its fur. Comedic but menacing crop-pest monarch.",
   idle="hunched on its hind legs, crown wobbling, tail swishing, sniffing and gnashing its teeth toward the left, claws flexing",
   hurt="recoiling backward, crown flying up off its head, mud splattering, eyes squeezed shut, impact stars",
   atk="frame1 crouches low, frame2 DIGS / burrows head-first into a mound of brown mud (half buried, mud spraying), frame3 only a mud mound with the crown and ears poking out, frame4 ERUPTS upward out of the mud, claws raised, mud clods flying, frame5 spins and WHIPS its long tail toward the LEFT, frame6 recover on hind legs"),
 'pakdurian': dict(
   character="PAK DURIAN, a stocky middle-aged Indonesian DURIAN VENDOR riding a small step-through SCOOTER / moped that is absurdly OVERLOADED with a tall wobbly pile of spiky green DURIAN fruits tied with ropes on a rack behind him. He wears a black peci cap, a batik shirt, a towel around his neck, flip-flops, a thick moustache and a big grin. The scooter is red with a round headlight and a horn. Keep the scooter and the durian pile visible and dominant in every frame. Comedic boss vehicle.",
   idle="idling on the scooter, wheels rocking slightly, durian pile wobbling, exhaust puffing, the vendor grinning and twirling his moustache toward the left",
   hurt="the scooter jolting backward, durians bouncing off the pile, vendor's cap flying off, smoke puffing from the engine, impact stars",
   atk="frame1 vendor grabs a durian from the pile, frame2 winds up holding the spiky durian high, frame3 THROWS the durian in an arc toward the LEFT, frame4 revs the engine with a big smoke cloud from the exhaust, frame5 scooter lunges / charges LEFT with front wheel lifted, frame6 recover"),
 'garuda': dict(
   character="GARUDA, a majestic humanoid BIRD-MAN warrior inspired by Javanese mythology: an EAGLE head with a sharp curved golden-yellow beak and fierce eyes, a golden crown-like crest of feathers, a muscular human torso with brown-and-gold feathers, huge brown-and-gold feathered WINGS instead of arms (feathered wing-hands with claw fingers), wearing a red-and-gold BATIK SARONG around the waist, golden armbands, bird talons for feet. Heroic-villain look, powerful and proud (the final boss).",
   idle="standing proudly on his talons, wings half spread and slowly flapping, head turning, glaring to the left",
   hurt="recoiling backward, feathers bursting off, wings flung up, beak open in a squawk, impact stars",
   atk="frame1 wings raised high, frame2 pulls a rope fishing NET from behind with a wing, frame3 THROWS the spread rope net toward the LEFT, frame4 big WING FLAP sending sharp feathers flying left, frame5 BEAK LUNGE: whole body thrust forward-left, beak first, frame6 recover"),
 # ---- ORIANE campaign (refs -i in prompts/<boss>.refs, cf. run_batch.sh) ----
 'stics': dict(
   character="NOT a person and NOT a server: STICS, the CROP SIMULATION MODEL itself (a soil-crop model software that a PhD student keeps trying to run and that keeps CRASHING) come to life as a monster. A big SOFTWARE WINDOW standing upright on stubby legs: a grey retro desktop-application window frame (title bar with three little buttons and the STICS logo, a menu bar, a few input-parameter fields and sliders on its side), and growing OUT OF the window a giant SIMULATED CROP PLANT made of glowing green VOXELS / pixels (a tall wheat-and-maize hybrid stalk with big leaves and a golden ear like a head), with an angry pixel face on the ear; at the bottom of the window a striped SOIL cross-section (soil layers, roots, water drops) and a small growth-curve chart. The STICS LOGO copied from the ATTACHED reference image (the word stics in elegant dark-green CALLIGRAPHIC lowercase letters with a round RED DOT above the i) is LARGE and CLEAR in the title bar / centre of the window and must stay legible in every frame.",
   idle="the simulated plant swaying and growing a little, leaves flapping, the growth curve ticking up, a small progress bar running, the angry face glaring to the left",
   hurt="the window jolting backward, the plant glitching into scattered pixels, a red error icon popping up, impact stars",
   atk="frame1 COMPUTING: a big progress bar and spinning hourglass in the window, the plant glowing, leaves raised; frame2 FIRES a burst of glowing cyan data cubes / pixel seeds from the window toward the LEFT; frame3 FERTILIZES: the plant sprays green nitrogen droplets (marked N) high up into the air; frame4 OVERLOAD: the window glowing red, the plant overgrown and twisted, warning triangles; frame5 CRASH (it PLANTS = it crashes): the window filled with red ERROR / exception popups stacked on each other and a sad face, the plant WILTED and drooping, frozen, a little smoke; frame6 RESTART: the plant a small seedling again in the window, a tiny progress bar restarting",
   textnote=" (the green calligraphic word \"stics\" of the logo IS allowed, since it is the character)"),
 'woriane': dict(
   style=FINE,
   character="WORIANE, the EVIL TWIN of the heroine ORIANE, exactly like Wario is to Mario. ATTACHED: image 1 is the NEW sprite sheet of Oriane in this game (her exact look, outfit and pixel style), images 2-3 are PHOTOS of the real Oriane (face identity), image 4 is another boss of the game (GARUDA): STYLE, pixel density and BOSS SIZE reference only. Woriane MUST be INSTANTLY RECOGNIZABLE AS ORIANE: the SAME face (same oval face shape, nose, cheeks, eyebrows), the SAME long wavy LIGHT-BROWN / chestnut hair with lighter ends falling below the shoulders, the SAME body proportions and the SAME clothes CUT as image 1 (flowy boho blouse with rolled sleeves and a slim belt, trousers rolled up at the ankle, sneakers, small crossbody satchel). Only the attitude and the colours change (a dark colour-swap of Oriane's outfit): the blouse becomes deep PLUM / dark PURPLE with a small acid-GREEN paisley pattern and a jagged yellow W brooch, the trousers dark slate grey, the sneakers black with purple soles, the satchel black with a tiny dark-purple chili charm, a faint violet shadow aura. A MEAN, cocky, sly evil grin (Wario-like) with narrowed eyes and a raised eyebrow, slight dark circles under the eyes (she embodies Oriane's doubts and anxiety). NOT a goth, NOT a zombie, NOT grey skin: normal fair skin like Oriane, same hair colour. She is about 15% TALLER and more imposing than Oriane (boss size).",
   idle="standing with a cocky menacing stance, smirking, tossing a dark purple chili pepper up and down in one hand, facing left",
   hurt="recoiling, hair flying, eyes squeezed shut, purple sparks, impact stars",
   atk="frame1 WIND-UP holding a dark purple chili pepper behind her; frame2 THROWS the dark chili hard toward the LEFT; frame3 crouches and BOWLS a dark jar along the ground toward the LEFT; frame4 hugs herself, head down, summoning a dark STORM CLOUD with a question mark above her head; frame5 DASHES / lunges to the LEFT leaving a purple smear; frame6 COLLAPSED: sitting on the ground curled up hugging her knees, crying, small sad tears (she is overwhelmed by doubt)"),
}

import sys
ONLY = set(sys.argv[1:])            # noms en argument = n'ecrit que ceux-la
for boss, d in BOSSES.items():
    if ONLY and boss not in ONLY:
        continue
    body = COMMON.format(boss=boss, root=ROOT, character=d['character'], style=d.get('style', STYLE),
                         idle=d['idle'], hurt=d['hurt'], atk=d['atk'],
                         textnote=d.get('textnote', ''), facenote=d.get('facenote', ''))
    open(os.path.join(OUT, boss + '.txt'), 'w', encoding='utf-8').write(body)
    print('wrote', boss + '.txt')
