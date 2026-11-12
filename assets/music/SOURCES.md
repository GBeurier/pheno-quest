# Musiques d’Oriane

Ces arrangements MIDI sont joués par le synthétiseur chiptune du jeu et embarqués
dans `js/assets_data.js` : aucun téléchargement pendant la partie.

| Fichier | Niveau | Morceau | Source |
| --- | --- | --- | --- |
| `oriane_niveau1.mid` | L’appart | Daddy Yankee — Gasolina | [Midis101](https://www.midis101.com/free-midi/9352-daddy-yankee-gasolina) |
| `oriane_niveau2.mid` | La simulation | Worakls — Salzburg | [Nonstop2k](https://www.nonstop2k.com/midi-files/16533-worakls-salzburg-midi.html) |
| `oriane_niveau3.mid` | Le labo | Bad Bunny — DtMF | [MIDI DB / Hit Trax](https://www.mididb.com/bad-bunny/dtmf-midi/) |

Téléchargés le 12 novembre 2026. Gasolina est une séquence complète de reggaeton
(environ 3 min 33 s). Salzburg est un arrangement partiel mélodique d’environ
65 secondes, proposé en téléchargement « Regular / Free » par Nonstop2k.
DtMF est un **extrait de démonstration**, proposé gratuitement par MIDI DB.
Le téléchargement gratuit ne constitue pas une licence de redistribution ni de
synchronisation ; aucune licence libre n’est revendiquée ici.

Préparation des boucles (sans changer le lecteur partagé) :

- Gasolina : conservation de toute la durée et des canaux source 2, 3, 4, 8, 9,
  10, 11 et 13 (numérotation MIDI de 1 à 16). Suppression des couches de bruitages
  et doublures pour laisser respirer la mélodie. Les vélocités intègrent les volumes
  et expressions CC7/CC11 du fichier, avec un facteur global de 0,75.
  La partie rythmique XG du canal 11 est réunie avec les percussions GM du canal 10 ;
  les notes 33, 39, 79, 86 et 104 deviennent respectivement 36, 38, 46, 46 et 42.
  Les messages SysEx propres au matériel sont retirés pour rester compatibles avec
  le lecteur SMF du jeu. La première mesure silencieuse (768 ticks, environ 2,47 s)
  est retirée : la musique démarre immédiatement et dure environ 3 min 30 s.
- Salzburg : les quatre canaux mélodiques sont conservés ; vélocités pondérées à
  65 %, 80 %, 45 % et 45 % pour distinguer basse, mélodie et accompagnement.
- DtMF : fichier `AUD_FV0035.mid`, 48 ticks/noire ; conservation des ticks 384 à
  2688 (12 mesures à 113 BPM, environ 25,5 secondes). Suppression de l’introduction
  silencieuse et du marqueur de fin à 208 secondes qui aurait provoqué un long blanc.
- Les notes encore tenues à la coupe sont fermées ; les réglages d’instruments et
  les métadonnées initiales sont conservés. Le dernier départ de note de DtMF,
  à moins de 40 ms de la coupe, est retiré pour respecter la durée minimale du
  lecteur et conserver une reprise sur la mesure.

Après remplacement d’une piste : `python gen_assets_data.py`.
