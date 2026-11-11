/* Aventures : ordre, carte, narration et habillage, independants du moteur.
 * Les identifiants sont persistants : ne pas les renommer apres publication.
 * Les definitions de niveaux / boss / assets restent partageables. */
window.LQ_CAMPAIGNS = (() => {
  'use strict';
  const C = window.CONFIG;
  return {
    laura_phd: {
      id: 'laura_phd', title: 'La quete du riz',
      levels: C.levels.slice(), finalLevel: 'jury',
      world: Object.assign({ background: 'bg_map' }, C.world),
      screens: { chapter: 'bg_chapter', win: 'bg_win' },
      story: Object.assign({ progressLabel: 'Manuscrit', levelLabel: 'Chapitres',
        finishLabel: 'PhD', collectibleLabel: 'Publis' }, C.story, {
        chapters: Object.fromEntries(C.levels.map((key, i) => [key, C.story.chapters[i] || ''])),
      }),
      music: C.music,
    },
    // Marcos : thesard a Java (cf. docs/superpowers/specs/2026-11-02-marcos-campaign-design.md).
    marcos_these: {
      id: 'marcos_these', title: 'La these de Marcos',
      levels: ['marcos_rizieres', 'marcos_village', 'marcos_parcelle'], finalLevel: null,
      world: { background: 'bg_marcos_map', fallbackBackground: 'bg_marcos_port', nodes: [
        { key: 'marcos_rizieres', x: 190, y: 380, label: 'LES RIZIERES', boss: 'RAJA TIKUS' },
        { key: 'marcos_village',  x: 470, y: 300, label: 'LE VILLAGE',   boss: 'PAK DURIAN' },
        { key: 'marcos_parcelle', x: 760, y: 230, label: 'LA PARCELLE',  boss: 'GARUDA' },
      ] },
      screens: { chapter: 'bg_marcos_chapter', win: 'bg_marcos_win', popup: 'bg_marcos_chapter',
                 fallback: 'bg_marcos_port' },
      startVehicle: { enabled: false },
      story: {
        title: 'MARCOS', subtitle: 'La these de Marcos',
        intro: 'Marcos fait sa these sur le riz sous ombrieres, a Java.\n' +
               'Boue, rats, durians et oiseaux : rien ne lui sera epargne.\n' +
               'Sors la guitare, appelle les etudiants et decroche ton PhD !',
        hint: 'Gauche/Droite ou Q/D bouger   HAUT sauter (relache tot = petit saut)\n' +
              'ESPACE notes   X (tiens) power chord   MAJ dash   C etudiants   BAS+SAUT descend   ESC quitter',
        overworld: 'Choisis un terrain (ESPACE pour entrer)',
        chapterDone: 'CHAPITRE ECRIT !', bossWarn: 'Bats le boss pour ecrire le chapitre !',
        catEmpty: 'Les etudiants sont epuises ! (ils reviennent bientot)',
        win: 'SOUTENANCE REUSSIE !  Felicitations Docteur Marcos !',
        dead: 'MARCOS EST K.O. !', deadSub: 'ON REPREND LE CHAPITRE...',
        publi: 'PUBLICATION TROUVEE ! +100%',
        mention: 'MENTION TRES HONORABLE', feliJury: 'FELICITATIONS DU JURY',
        progressLabel: 'Manuscrit', levelLabel: 'Chapitres', finishLabel: 'PhD', collectibleLabel: 'Publis',
        medals: ['TEMPS', 'DATA', 'SAUVES'],
        chapters: {
          marcos_rizieres: 'CHAPITRE 1 : Le dispositif.\nRaja Tikus retourne dans sa boue : les ombrieres en bambou sont montees, la manip demarre !',
          marcos_village: 'CHAPITRE 2 : Le terrain.\nPak Durian est en panne seche : enquetes au village bouclees, les donnees rentrent !',
          marcos_parcelle: 'CHAPITRE 3 : Les resultats.\nGaruda s envole bredouille : le riz pousse sous les filets, la these est ecrite. Place a la soutenance !',
        },
      },
      music: C.music,
    },
    // Oriane: PhD in crop modelling (cf. docs/superpowers/specs/2026-11-10-oriane-campaign-design.md).
    oriane_these: {
      id: 'oriane_these', title: 'La these d Oriane',
      levels: ['oriane_appart', 'oriane_simu', 'oriane_labo'], finalLevel: null,
      world: { background: 'bg_oriane_map', fallbackBackground: 'bg_map', nodes: [
        { key: 'oriane_appart', x: 196, y: 378, label: 'L APPART',       boss: 'FRANCOIS' },
        { key: 'oriane_simu',   x: 440, y: 296, label: 'LA SIMULATION',  boss: 'STICS' },
        { key: 'oriane_labo',   x: 736, y: 232, label: 'LE LABO',        boss: 'WORIANE' },
      ] },
      screens: { chapter: 'bg_oriane_chapter', win: 'bg_oriane_win', popup: 'bg_oriane_chapter',
                 fallback: 'bg_chapter' },
      startVehicle: { enabled: false },
      story: {
        title: 'ORIANE', subtitle: 'La these d Oriane',
        intro: 'Oriane fait sa these sur la modelisation des cultures associees.\n' +
               'Proprio grincheux, modele STICS qui plante sans arret... et pire : ses propres doutes.\n' +
               'Sors les piments, roule le beurre de cacahuete et decroche ton PhD !',
        hint: 'Gauche/Droite ou Q/D bouger   HAUT sauter (relache tot = petit saut)\n' +
              'ESPACE piments   X (tiens) pot de beurre de cacahuete   MAJ dash   BAS+SAUT descend   ESC quitter',
        overworld: 'Choisis une etape (ESPACE pour entrer)',
        chapterDone: 'CHAPITRE ECRIT !', bossWarn: 'Bats le boss pour ecrire le chapitre !',
        win: 'SOUTENANCE REUSSIE !  Felicitations Docteure Oriane !',
        dead: 'ORIANE EST K.O. !', deadSub: 'ON REPREND LE CHAPITRE...',
        publi: 'PUBLICATION TROUVEE ! +100%',
        mention: 'MENTION TRES HONORABLE', feliJury: 'FELICITATIONS DU JURY',
        progressLabel: 'Manuscrit', levelLabel: 'Chapitres', finishLabel: 'PhD', collectibleLabel: 'Publis',
        medals: ['TEMPS', 'DATA'],
        chapters: {
          oriane_appart: 'CHAPITRE 1 : L etat de l art.\nFrancois a rendu les cles : l appart est calme, la biblio est bouclee !',
          oriane_simu: 'CHAPITRE 2 : Les simulations.\nSTICS ne plante plus : la simulation tourne jusqu au bout, les courbes sont belles !',
          oriane_labo: 'CHAPITRE 3 : La discussion.\nWoriane s evapore : plus de doutes, Oriane croit en elle. Place a la soutenance !',
        },
      },
      music: C.music,
    },
  };
})();
