# EM Visions : inventaire des six pages et spécification UX/UI et full stack

**Référence :** les six PNG du dossier `maquettes-em-visions/images/`, examinés le 26 septembre 2026.

## 0. Comment lire ce document

Les fichiers montrent les premiers écrans de six pages de bureau en français et en thème sombre. Ils constituent une direction visuelle. Les sections situées plus bas, les versions mobiles et plusieurs états interactifs ne sont pas encore dessinés.

Chaque élément est identifié avec l’un de ces statuts :

- **V : visible** dans la maquette actuelle.
- **P : proposition d’intégration** ou complément à dessiner pour rendre le parcours complet.
- **T : exigence technique proposée**, invisible dans une image fixe.

Les dimensions indiquées sont des repères estimés à partir d’images d’environ **1 586 × 992 px**, et non des mesures extraites d’un fichier Figma. Les noms de composants décrivent une architecture proposée, indépendante du framework. Aucun serveur, formulaire ou carrousel fonctionnel n’est livré par ces PNG.

## 1. Structure globale et parcours

### 1.1 Les pages et leurs destinations

| Page | Route française proposée | Route anglaise proposée | Fonction dans le parcours |
| --- | --- | --- | --- |
| Accueil | `/fr` | `/en` | Comprendre l’offre, voir l’atelier et des exemples, commencer une demande. |
| Services | `/fr/services` | `/en/services` | Identifier la prestation adaptée au projet. |
| Réalisations | `/fr/realisations` | `/en/work` | Examiner le travail réalisé et ouvrir un projet. |
| Catalogue | `/fr/catalogue` | `/en/catalog` | Accéder aux catalogues des fournisseurs et choisir un support. |
| À propos | `/fr/a-propos` | `/en/about` | Comprendre qui réalise les projets et comment travaille l’équipe. |
| Contact | `/fr/contact` | `/en/contact` | Déposer une demande et trouver la boutique. |

**Gabarits complémentaires P :** détail de réalisation, confirmation du formulaire, page introuvable et politique de confidentialité. Ils ne deviennent pas nécessairement des entrées de navigation. Le lieu et la carte sont intégrés à Contact, avec une ancre `#nous-trouver`.

### 1.2 Emboîtement des composants

| Parent | Enfants | Responsabilité |
| --- | --- | --- |
| `SiteLayout` | `SkipLink`, `SiteHeader`, `main`, `SiteFooter` | Cadre partagé par toutes les pages. |
| `SiteHeader` | `BrandLogo`, `MainNavigation`, `LanguageSwitcher`, `ThemeToggle` | Navigation, langue et apparence. |
| `main` | Le composant correspondant à la route | Un seul contenu principal et un H1 propre à la page. |
| Chaque page | `EditorialHeading`, compositions de photos, listes, appels à l’action | Mise en scène spécifique dans la même identité. |
| `ProjectCarousel` | Photo active, aperçus, légende, commandes, compteur | Un même état pilote toute la sélection du projet. |
| `QuoteForm` | Champs, pièce jointe, erreurs, bouton, confirmation | Saisie, validation et envoi d’une demande. |
| `StoreLocation` | Adresse, photographie, carte, lien d’itinéraire | Toutes les représentations utilisent la même fiche d’établissement. |
| `TornFrame` | Photo et bord de papier | Découpe artistique réutilisable avec des variantes de forme. |
| `PaperAction` | Libellé et flèche | Un lien ou un bouton unique, sans bouton imbriqué. |

### 1.3 Grille proposée

- Grille de bureau à 12 colonnes, largeur utile plafonnée autour de 1 600 px.
- Marges ordinaires de 48 à 72 px sur grand écran; débords décoratifs possibles jusqu’aux bords.
- Espacement de base : 8, 16, 24, 32, 48 et 64 px. Gouttière indicative : 24 px sur bureau, 16 px sur mobile.
- En-tête d’environ 110 à 120 px sur les références. Le contenu conserve sa place si l’en-tête devient fixe.
- Le texte et les contrôles suivent la grille. Les déchirures, rubans et éclaboussures peuvent en sortir.
- La hauteur du contenu reste naturelle. On évite de forcer toute page dans `100vh`, surtout le formulaire et les versions traduites.
- Les superpositions se font localement dans une composition. On ne positionne pas tous les éléments de la page en coordonnées absolues.

## 2. Inventaire partagé par les six pages

### 2.1 En-tête

| ID | État | Élément et emplacement | Développement et comportement |
| --- | --- | --- | --- |
| G01 | V | Bande supérieure noire texturée, sur toute la largeur. | Composant `SiteHeader`, même hauteur et même alignement sur les six routes. |
| G02 | V | Logo calligraphique blanc « EM Visions », ovale incliné, en haut à gauche. | Réutiliser `sources/logo-original.png`, ou son véritable équivalent vectoriel s’il est disponible. Ne pas recréer le logo à partir de chaque rendu généré. |
| G03 | T | Zone cliquable du logo. | Lien vers l’accueil dans la langue active. Texte alternatif identifiant la marque et la destination. |
| G04 | V | Lien **Accueil**, premier dans la navigation centrale. | Destination `/fr` ou `/en`. |
| G05 | V | Lien **Services**, deuxième. | Destination de la page Services. |
| G06 | V | Lien **Réalisations**, troisième. | Destination du portfolio. |
| G07 | V | Lien **Catalogue**, quatrième. | Destination des fournisseurs. |
| G08 | V | Lien **À propos**, cinquième. | Destination de l’équipe. |
| G09 | V | Lien **Contact**, sixième. | Destination du formulaire et de l’adresse. |
| G10 | V | Libellé actif plus gras et trait cobalt placé dessous. | Calculé depuis la route; `aria-current="page"`. La position doit suivre le vrai lien, y compris en anglais. |
| G11 | V | **FR**, à droite de Contact, bleu dans la version française. | Lien vers la traduction française du même contenu. |
| G12 | V | Petit séparateur vertical entre FR et EN. | Élément décoratif, ignoré par les technologies d’assistance. |
| G13 | V | **EN**, à droite de FR, blanc dans l’état affiché. | Lien vers la traduction anglaise de la même page, et du même projet quand il existe. |
| G14 | V | Séparation verticale plus haute avant la commande de thème. | Décor, pas un contrôle. |
| G15 | V | Cercle à contour bleu avec lune blanche, à l’extrême droite. | `ThemeToggle`; icône SVG. Le nom accessible et l’état indiquent clairement « Mode sombre ». |
| G16 | T | Mémorisation du thème. | Priorité au choix sauvegardé, puis à la préférence du système; appliquer le thème avant le premier affichage pour éviter un flash. |
| G17 | P | Menu compact sur écran étroit. | Le remplacer avant que les liens se touchent, autour de 1 120 px comme point de départ à tester. Conserver FR/EN et le thème accessibles. |
| G18 | P | Lien « Aller au contenu » au début de l’ordre de tabulation. | Visible lorsqu’il reçoit le focus; rejoint `main`. |

Le bouton de devis principal appartient au contenu de la page. L’en-tête des six références ne comporte pas de bouton de devis supplémentaire.

### 2.2 Matière graphique et composants visuels

| ID | État | Élément | Construction prévue |
| --- | --- | --- | --- |
| G19 | V | Fond noir légèrement granuleux. | Couche de fond partagée, texture optimisée et peu contrastée derrière les paragraphes. |
| G20 | V | Rayures, plis, marques d’usure et diagonales sombres. | Calques de décor, sans fonction ni texte alternatif. |
| G21 | V | Éclaboussures cobalt autour des compositions. | Petits assets transparents; ne doivent pas réduire la lecture des textes. |
| G22 | V | Bords irréguliers de papier blanc. | Masques alpha ou SVG distincts de la photographie. Plusieurs variantes pour conserver des découpes originales. |
| G23 | V | Morceaux de ruban adhésif gris translucide. | Décor au-dessus des cadres, sans interception des clics. |
| G24 | V | Petites croix et repères d’impression. | SVG décoratifs à traits fins; dimensions stables. |
| G25 | V | Bandes verticales rappelant la pellicule, petits numéros et marques. | Décor photographique sur les compositions concernées. Les faux numéros ne deviennent pas des informations de navigation. |
| G26 | V | Grands titres blancs, très gras et condensés. | Texte HTML sélectionnable. La police exacte n’est pas identifiable avec certitude à partir des PNG; son fichier et sa licence restent à choisir. |
| G27 | V | Carré cobalt à la fin de certains titres. | Ponctuation graphique indépendante, alignée sur la ligne de base et masquée aux lecteurs d’écran. |
| G28 | V | Petit trait horizontal cobalt sous le titre ou l’introduction. | Accent décoratif aligné sur le bord gauche du texte. |
| G29 | V | Paragraphes blancs ou gris clair, plus aérés. | Largeur de lecture maîtrisée; corps indicatif 18 à 22 px sur bureau, 16 à 18 px sur mobile. |
| G30 | V | Boutons sur morceau de papier blanc déchiré. | Surface décorative derrière le libellé. Le masque ne doit pas découper le texte ni le focus. |
| G31 | V | Disque noir à droite du bouton et flèche blanche. | Enfants décoratifs du même lien, pas deux actions séparées. |
| G32 | T | Ordre des calques. | Fond, photographies, papier, décor, puis texte et commandes; chaque composition possède son propre contexte d’empilement. |
| G33 | T | Décors non interactifs. | `pointer-events: none`, `aria-hidden="true"`; images décoratives avec alternative vide. |

**Palette :** noir, blanc et cobalt pour l’interface. Les couleurs réelles des photos restent présentes : enseigne magenta, bandes jaunes Ricova, impression rose du chandail. Le traitement en gris demandé s’applique aux personnes Vince et Eduardo, avec conservation du bleu voulu. On ne filtre pas automatiquement toutes les photos en bleu.

**Typographie indicative :** titres de 88 à 144 px sur grands écrans, 44 à 72 px sur petits écrans, avec réglage propre à chaque titre; navigation de 14 à 16 px. La taille reste fluide et les retours à la ligne sont adaptés à la langue. Ces valeurs sont des points de départ d’intégration, pas des mesures contractuelles des images.

### 2.3 Pied de page partagé, à dessiner

| ID | État | Élément | Placement et fonctionnement |
| --- | --- | --- | --- |
| G34 | P | Transition de papier déchiré. | Fin du contenu; prépare le pied de page sans recouvrir un bouton. |
| G35 | P | Petit logo officiel. | Début du pied de page, lien accueil. |
| G36 | P | Rappel des six destinations principales. | Liste de liens structurée; mêmes données que la navigation principale. |
| G37 | P | Adresse et lien « Itinéraire ». | Fiche d’établissement commune à Contact. |
| G38 | P | Téléphone, courriel et heures, une fois confirmés. | Liens `tel:` et `mailto:`; horaires structurés. Aucune valeur fictive pour remplir la maquette. |
| G39 | P | Politique de confidentialité. | Page dédiée accessible depuis le formulaire et le pied de page. |
| G40 | P | Nom de l’entreprise et année. | Informations éditoriales validées; année gérée automatiquement si souhaité. |
| G41 | P | Réseaux sociaux vérifiés, si retenus. | N’afficher que les liens réellement fournis par l’entreprise. |

Le pied de page n’est visible dans aucun des six PNG. Il faut donc le maquetter avant de considérer la totalité du défilement comme définie.

## 3. Page Accueil

### 3.1 Composition

La colonne éditoriale occupe environ le tiers gauche. La devanture est la grande image centrale. Deux aperçus verticaux occupent le bord droit. Les commandes du carrousel se trouvent sous ces aperçus. Les cadres déchirés font se rencontrer texte et photos sans placer le texte principal sur le bâtiment.

### 3.2 Inventaire visible

| ID | Élément | Position et contenu | Composant, action ou donnée |
| --- | --- | --- | --- |
| A01 | En-tête commun. | Haut de page; Accueil actif. | G01 à G18. |
| A02 | H1. | Haut et milieu gauche : **FAITES / BONNE / IMPRESSION.** | `EditorialHeading`; traduction prévue « Make a good impression ». |
| A03 | Carré bleu terminal. | À droite de la dernière ligne du titre. | G27. |
| A04 | Trait bleu. | Sous le H1, aligné à gauche. | G28. |
| A05 | Texte d’introduction. | Sous le trait : « Vêtements et objets personnalisés pour donner forme à vos idées. » | Contenu localisé; pas intégré au fichier photographique. |
| A06 | Lien principal de devis. | Sous l’introduction, dans la partie basse gauche : **Demander un devis**. | `PaperAction` vers `/fr/contact#devis`; provenance Accueil. |
| A07 | Support du lien. | Papier blanc irrégulier sous le texte. | Décor indépendant. |
| A08 | Disque et flèche. | Extrémité droite de A06. | Même cible cliquable que le libellé. |
| A09 | Photographie principale. | Centre, du dessous de l’en-tête jusqu’au bas du visuel. | `StorefrontMedia`, référence `sources/devanture.png`. |
| A10 | Détails réels de la devanture. | Façade, fenêtres, balcons, enseigne magenta, vitrine, lampadaire, trottoir et rue. | Contenu de la photo. Préserver l’architecture, le nom et la couleur de l’enseigne. |
| A11 | Cadre de la devanture. | Contour blanc déchiré autour de A09. | `TornFrame`; forme propre à ce cadrage. |
| A12 | Premier aperçu de projet. | Bande verticale immédiatement à droite de la devanture. | Photo Ricova, vêtement sombre et bandes réfléchissantes jaunes. |
| A13 | Deuxième aperçu de projet. | Bande verticale à l’extrême droite. | Vitrine Buono avec inscription Pop Up Shop et illustration. |
| A14 | Séparations des aperçus. | Bandes bleues, bords noirs et blancs, détails de pellicule. | Décor superposé au rail photographique. |
| A15 | Flèche précédente. | Sous les aperçus, à gauche du compteur. | Bouton circulaire, nom accessible « Image précédente ». |
| A16 | Compteur. | Entre les deux flèches : **01 / 05** sur l’image. | Valeur calculée depuis l’index et le nombre réel d’éléments. |
| A17 | Flèche suivante. | À droite du compteur. | Bouton circulaire, nom accessible « Image suivante ». |
| A18 | Cinq segments de pagination. | Sous les flèches; premier bleu, autres blancs. | Sélecteurs de diapositives avec zones cliquables plus grandes que les traits visibles. |
| A19 | Rubans, déchirures secondaires, éclaboussures et croix. | Pourtour des photos, angles et bas de la composition. | G19 à G25 et G33. |

### 3.3 Fonctionnement à développer

1. **Une collection de médias ordonnée** alimente le grand visuel, les aperçus, les flèches et la pagination.
2. **Un seul état `activeIndex`** pilote le composant. Les aperçus sont les médias suivants dans cette collection.
3. **Un clic sur un aperçu** le sélectionne; le glissement tactile et les boutons proposent la même navigation.
4. **Le texte d’accueil et le devis restent fixes** pendant le changement de média.
5. **La devanture est un média d’introduction.** Pour conserver cette ouverture et les cinq réalisations demandées, la proposition est une collection de six médias : devanture, Ricova, Buono, Elevate, enseigne MA et Balloon Babe. Le compteur d’accueil devient donc `01 / 06`. Cette correction n’apparaît pas encore sur le PNG.
6. **Un libellé de projet P** apparaît sous ou à côté du média lorsqu’une réalisation est active; il peut mener à sa fiche. La devanture mène à `Contact#nous-trouver`.
7. **La commande de devis** reste une seule action principale. Elle n’envoie rien : elle ouvre le formulaire.
8. **Défilement manuel par défaut.** Une rotation automatique éventuelle demanderait une commande pause et un comportement adapté au focus et à la préférence de mouvement réduit.
9. **En absence de JavaScript**, la première photographie, la présentation et les liens principaux restent utilisables; une liste de réalisations doit permettre l’accès aux autres projets.

### 3.4 Suite de page proposée

- **A20 P : aperçu des six services**, sous le hero; intitulé, courte description, lien de détail, sans répéter le très grand titre.
- **A21 P : déroulement de la commande**, trois étapes validées avec l’équipe : préciser le projet, préparer le visuel et le support, produire et livrer selon les modalités convenues.
- **A22 P : accès à l’atelier**, photographie ou vignette de devanture, adresse et lien vers la carte.
- **A23 P : pied de page partagé.**

### 3.5 Petit écran

Ordre de lecture : titre, introduction, devis, photo principale, légende éventuelle, commandes, services, atelier, pied de page. Le rail laisse entrevoir une partie du média suivant. Les deux aperçus étroits de bureau ne doivent pas devenir des bandes illisibles. Les déchirures restent reconnaissables avec moins de décors périphériques.

## 4. Page Services

### 4.1 Composition

Grand titre dans le quart supérieur gauche. Liste de six prestations dans la moitié inférieure gauche, répartie sur deux colonnes. À droite, grand chandail Elevate en haut et enseigne MA en bas, dans deux cadres déchirés qui se chevauchent visuellement.

### 4.2 Inventaire visible

| ID | Élément | Emplacement et contenu | Développement |
| --- | --- | --- | --- |
| S01 | En-tête commun. | Services actif. | G01 à G18. |
| S02 | H1. | Gauche : **DE L’IDÉE / À LA / MATIÈRE.** | Texte HTML; retours ajustables selon largeur et langue. |
| S03 | Carré bleu et trait bleu. | Fin du H1 puis dessous. | Décor du système commun. |
| S04 | Numéro 01. | Début de la première ligne de la colonne gauche. | Chiffres bleus; numérotation de présentation. |
| S05 | Design graphique. | À droite de 01 : « Des visuels qui marquent votre identité. » | Élément de liste lié au service correspondant. |
| S06 | Numéro 02 et Impression. | Deuxième ligne gauche : « Des supports de qualité pour vos projets. » | Même structure. |
| S07 | Numéro 03 et Vêtements personnalisés. | Troisième ligne gauche : « Des textiles uniques à votre image. » | Même structure; titre sur deux lignes dans la maquette. |
| S08 | Numéro 04 et Impression 3D. | Première ligne de la seconde colonne : « Des idées qui prennent forme. » | Même structure. |
| S09 | Numéro 05 et Sites Web. | Deuxième ligne de la seconde colonne : « Des plateformes sur mesure pour propulser votre marque. » | Même structure. |
| S10 | Numéro 06 et Applications. | Troisième ligne de la seconde colonne : « Des outils performants pour vos besoins spécifiques. » | Même structure. |
| S11 | Traits séparateurs verticaux. | Entre chaque numéro et son texte. | Décor, sans ajout de séparateur dans la lecture vocale. |
| S12 | Photo Elevate. | Grande surface supérieure droite : chandail clair et impression Miami. | `sources/elevate.webp`; conserver les couleurs du produit réel. |
| S13 | Cadre supérieur. | Papier blanc irrégulier autour de S12. | Variante large de `TornFrame`. |
| S14 | Photo de l’enseigne MA. | Partie inférieure droite : enseigne ronde suspendue, briques et ciel. | `sources/3dsign.webp`; le nom du fichier ne suffit pas à confirmer la technique de fabrication. |
| S15 | Cadre inférieur et recouvrement. | Déchirure diagonale entre les deux photos. | Deux cadres indépendants dans une seule composition. |
| S16 | Appel à l’action. | Bas gauche : **Parler de mon projet**, papier blanc, cercle noir et flèche. | Lien vers Contact, sans service présélectionné si le visiteur n’en a pas choisi. |
| S17 | Texture, éclaboussures, rubans et repères. | Fond et contours des deux photos. | Décor non interactif. |

### 4.3 Détail des services à prévoir sous le premier écran

Chaque entrée de la liste peut rejoindre une section stable, telle que `#design-graphique` ou `#impression-3d`.

Chaque section contient, dans cet ordre :

1. Identifiant et numéro du service.
2. H2 portant le nom du service.
3. Description concrète de la prestation, validée par EM.
4. Liste des livrables ou supports effectivement proposés.
5. Une photographie réelle adaptée, si disponible.
6. Un ou deux projets liés, alimentés depuis le portfolio.
7. Une indication des informations utiles pour préparer le devis.
8. Un lien « Demander un devis pour ce service ».

Les tarifs, délais, quantités minimales et procédés ne sont ajoutés qu’avec des données confirmées. La photo de l’enseigne MA ne prouve pas à elle seule qu’elle a été imprimée en 3D.

### 4.4 Relations techniques

- Collection `Service`, triée par `displayOrder`.
- Relation plusieurs-à-plusieurs avec `Project`, afin qu’une réalisation puisse illustrer plusieurs services.
- Lien de devis : `/fr/contact?service=<slug>#devis`.
- Le formulaire résout le slug autorisé vers l’identifiant du service et montre la sélection de façon modifiable.
- Si le paramètre est inconnu, le formulaire redevient générique.
- Les données peuvent être chargées au rendu de la page. Un changement de section ne nécessite pas une requête réseau.
- Ordre mobile de la liste : 01, 02, 03, 04, 05, 06; aucune inversion causée par les colonnes CSS.

## 5. Page Réalisations

### 5.1 Composition

Titre et présentation à gauche; grand projet actif au centre; deux projets suivants en bandes verticales à droite; commandes au-dessous. La structure du rail reprend celle de l’accueil, mais le contenu est entièrement orienté vers les projets.

### 5.2 Inventaire visible

| ID | Élément | Position et contenu | Développement |
| --- | --- | --- | --- |
| R01 | En-tête commun. | Réalisations actif. | G01 à G18. |
| R02 | H1. | Gauche : **LE / TRAVAIL / PARLE.** | `EditorialHeading`. |
| R03 | Carré et trait bleus. | Fin du titre et dessous. | Décor. |
| R04 | Texte court. | Sous le trait : « Des idées devenues réelles. » | Champ éditorial localisé. |
| R05 | Lien principal. | Bas gauche : **Voir le projet**. | Ouvre le projet actif, et change de destination avec lui. |
| R06 | Papier, disque et flèche de R05. | Sous le libellé et à son extrémité droite. | Un seul lien accessible. |
| R07 | Photo active Ricova. | Grande surface centrale : personne de dos, vêtement personnalisé et camion. | Référence `sources/ricova2.webp`; préserver le logo et le marquage du vêtement. |
| R08 | Cadre principal. | Grand papier déchiré autour de Ricova. | Forme spécifique, indépendante de la taille réelle du fichier source. |
| R09 | Aperçu Buono. | Première bande verticale à droite. | Référence `sources/buono.webp`. |
| R10 | Aperçu Elevate. | Deuxième bande à droite. | Référence `sources/elevate.webp`. |
| R11 | Bandes de pellicule et accents bleus. | Entre R07, R09 et R10. | Décor. |
| R12 | Flèche précédente. | Bas du rail. | Projet précédent. |
| R13 | Compteur **01 / 05**. | Entre les commandes. | Calculé à partir des projets publiés et sélectionnés pour ce carrousel. |
| R14 | Flèche suivante. | À droite du compteur. | Projet suivant. |
| R15 | Cinq traits de pagination. | Sous les commandes. | Accès direct aux cinq projets; état actif identifiable. |
| R16 | Rubans, croix, éclaboussures et plis. | Contours et fond. | Décor commun. |

### 5.3 Contenus et comportements complémentaires

- **R17 P : légende du projet actif.** Nom, catégorie et bref descriptif, placés près du rail; ne pas compter sur les logos inclus dans les photos pour identifier le travail.
- **R18 P : liste accessible de toutes les réalisations.** Sous le premier écran, liens vers les cinq projets; elle reste disponible même sans animation.
- **R19 P : catégories éventuelles.** Ajouter des filtres seulement lorsque chaque projet a une catégorisation validée et que le volume le justifie. Ils ne figurent pas sur le PNG.
- **R20 P : pied de page.**

La sélection initiale proposée est : Ricova, Buono, Elevate, enseigne MA, Balloon Babe. Les fichiers sources existent. La photographie Balloon Babe montre un visuel imprimé sur textile, pas une photographie de ballons. Les noms officiels de projets et les techniques exactes restent des champs éditoriaux à confirmer.

### 5.4 Gabarit de détail de réalisation à maquetter

Route proposée : `/fr/realisations/<slug>`.

1. En-tête partagé.
2. Lien de retour aux réalisations.
3. H1 avec nom du projet.
4. Nom du client, uniquement si sa présentation est validée.
5. Catégorie ou service associé.
6. Image principale réelle et texte alternatif.
7. Résumé du besoin.
8. Description de l’intervention d’EM, avec des faits confirmés.
9. Galerie de détails, si de véritables images supplémentaires sont disponibles.
10. Légendes des images lorsque nécessaires.
11. Liens vers les services concernés.
12. Lien « Je veux un projet semblable », qui présélectionne le contexte dans Contact.
13. Navigation vers le projet précédent et suivant.
14. Pied de page partagé.

Le projet dispose d’une URL stable. Un visiteur peut la partager ou revenir dessus directement. Si une galerie s’ouvre en plein écran, son bouton fermer, la touche Échap et le retour du focus doivent être définis.

### 5.5 État du carrousel

`activeProjectId` doit rester cohérent entre photo, légende, lien « Voir le projet », compteur et pagination. La première image est prioritaire au chargement; les suivantes se chargent progressivement. Si un projet est retiré, sa disparition met à jour la collection et le compteur. Avec un seul projet, les commandes superflues sont masquées.

## 6. Page Catalogue

### 6.1 Composition

Le titre, le texte et la liste de fournisseurs sont à gauche, sur environ 42 % de la largeur. Les casquettes occupent le grand visuel de droite. Un gros plan Ricova se superpose en bas à droite. Quatre petits carrés de couleur se trouvent sous les photos.

### 6.2 Inventaire visible

| ID | Élément | Position et contenu | Développement |
| --- | --- | --- | --- |
| C01 | En-tête commun. | Catalogue actif. | G01 à G18. |
| C02 | H1. | Haut gauche : **CHOISISSEZ / VOTRE SUPPORT.** | Texte HTML. |
| C03 | Carré bleu et trait bleu. | Fin du titre et dessous. | Décor. |
| C04 | Introduction. | « Des fournisseurs de confiance pour concrétiser vos idées. » | Texte localisé. |
| C05 | Ligne S&S Activewear. | Première entrée sous l’introduction, sur un bandeau cobalt déchiré. | Lien de fournisseur. Le bandeau représente son état visuel mis en avant. |
| C06 | « Voir le fournisseur » et flèche diagonale. | Partie droite du bandeau S&S, séparée par un trait vertical. | Une seule destination externe pour la ligne. |
| C07 | Canada Sportswear. | Deuxième entrée, fond noir, flèche à droite. | Lien externe vers son catalogue validé. |
| C08 | Fabrik. | Troisième entrée. | Même composant de lien. |
| C09 | Eside. | Quatrième entrée. | Même composant. |
| C10 | Just Like Hero. | Cinquième entrée. | Même composant. |
| C11 | Projob. | Sixième entrée. | Même composant. |
| C12 | Fins séparateurs gris. | Entre les fournisseurs et au début des lignes. | Décor de liste, pas des champs de formulaire. |
| C13 | Grand visuel de casquettes. | Partie supérieure et centrale droite; casquettes bleues et blanches marquées « em ». | Référence `sources/emcap.webp`. Le logo imprimé sur le produit reste dans sa photographie. |
| C14 | Papier déchiré et rubans du grand visuel. | Périmètre des casquettes. | `TornFrame`, variante haute. |
| C15 | Gros plan du vêtement Ricova. | Encart superposé en bas à droite. | Recadrage de la photo source, ou vrai détail haute résolution si fourni. |
| C16 | Cadre de l’encart. | Bords blancs et accent vertical bleu. | Calque distinct de C14. |
| C17 | Carré bleu. | Premier repère coloré sous l’encart. | Fonction non précisée dans le PNG. |
| C18 | Carré magenta. | Deuxième repère. | Même statut. |
| C19 | Carré jaune. | Troisième repère. | Même statut. |
| C20 | Carré noir à contour clair. | Quatrième repère. | Même statut. |
| C21 | Croix, texture et éclaboussures. | Bas de la page et contours. | Décor commun. |

### 6.3 Fonctionnement proposé

1. Chaque ligne utilise un objet `Supplier` comportant son nom, son ordre et son URL validée.
2. Au survol et au focus, le bandeau bleu et la flèche peuvent reprendre le traitement de la première ligne. Le style ne doit pas dépendre uniquement d’une souris.
3. Un seul clic ouvre le catalogue du fournisseur. Une ouverture dans un nouvel onglet doit être annoncée et accompagnée de `rel="noopener"`.
4. Les photos de casquettes et de Ricova illustrent des supports. Elles ne sont pas automatiquement attribuées au fournisseur survolé sans preuve de cette association.
5. Les quatre carrés sont traités comme des repères d’impression décoratifs dans la version de base. S’ils doivent devenir des filtres, il faudra définir les catégories, les nommer et leur associer de vraies données. Une couleur seule ne décrit pas un filtre.
6. **C22 P : aide à la sélection**, sous la liste : « Vous avez repéré un article ? Indiquez sa référence dans votre demande. »
7. **C23 P : lien de devis contextuel**, vers Contact avec le fournisseur connu; la référence d’article reste modifiable.
8. **C24 P : pied de page partagé.**

Le périmètre actuel correspond à un répertoire de catalogues fournisseurs. Un panier, un paiement, des stocks ou des prix synchronisés nécessiteraient un autre modèle fonctionnel, absent des maquettes.

### 6.4 Mobile

Titre, texte, liste des fournisseurs, aide au choix, composition photographique puis pied de page. Les flèches restent alignées à droite dans une zone tactile suffisamment large. La photo Ricova conserve une superposition mesurée sans masquer le produit principal.

## 7. Page À propos

### 7.1 Composition

La photographie détourée occupe environ les trois cinquièmes gauches. Vince apparaît devant à gauche, tête baissée, tenant un chandail. Eduardo est derrière et à droite, vu de profil avec un bras levé. Le titre et les identités sont dans la colonne droite. Un morceau de textile apparaît dans la déchirure inférieure.

### 7.2 Inventaire visible

| ID | Élément | Placement et contenu | Développement |
| --- | --- | --- | --- |
| P01 | En-tête commun. | À propos actif. | G01 à G18. |
| P02 | Portrait Vince. | Premier plan gauche. | Référence détourée `sources/vince.png`; visage, mains et cheveux traités en noir et blanc. |
| P03 | Tuque de Vince. | Sommet du portrait. | Bleu foncé conservé comme accent local. |
| P04 | Chandail tenu par Vince. | Grande partie inférieure gauche. | Préserver le geste, les mains et l’impression visible. |
| P05 | Portrait Eduardo. | Arrière-plan du duo, vers le centre. | Référence `sources/eduardo.png`; peau en gris, cheveux foncés, proportions préservées. |
| P06 | Contours bleus. | Périmètre des silhouettes et zones de séparation. | Liseré adapté à l’alpha des détourages; intensité mesurée. |
| P07 | Fond bleu sombre de la composition. | Derrière les deux personnes. | Couche indépendante, sans modifier les visages. |
| P08 | Grand contour déchiré blanc. | Haut, côtés et dessous du duo. | `TornFrame` spécifique à cette composition. |
| P09 | Détail de textile en bas. | Dans un pan de papier replié sous Eduardo. | Image de matière séparée; source à confirmer avant publication. |
| P10 | H1. | Colonne droite : **LES GENS / DERRIÈRE / L’IMPRESSION.** | Texte HTML, carré bleu en terminaison. |
| P11 | Trait bleu. | Sous le H1. | Décor. |
| P12 | Nom Eduardo Mazzonna. | Première colonne du bloc d’identités à droite. | Champ de fiche d’équipe. |
| P13 | Rôle Eduardo. | Sous son nom : **DESIGN GRAPHIQUE**. | Champ localisé. |
| P14 | Séparateur vertical. | Entre les deux identités. | Décor. |
| P15 | Nom Vince Mariani. | Deuxième colonne du bloc d’identités. | Champ de fiche d’équipe. |
| P16 | Rôle Vince. | Sous son nom : **GESTION DE PROJETS**. | Champ localisé. |
| P17 | Lien « Découvrir notre équipe ». | En dessous des noms, à droite. | Ancre vers `#equipe`, où les fiches détaillées doivent exister. |
| P18 | Papier, disque noir et flèche du lien. | Autour de P17. | `PaperAction`. |
| P19 | Éclaboussures, croix et plis. | Pourtour des portraits et bas de page. | Décor commun. |

### 7.3 Corrections et suite de page

- **Correspondance portraits et noms :** les noms apparaissent actuellement dans l’ordre Eduardo puis Vince, alors que les personnes se lisent visuellement Vince puis Eduardo. Ajouter des légendes explicites ou réordonner le bloc pour supprimer cette ambiguïté.
- **Traitement des portraits :** appliquer le gris aux bonnes zones avant export. Un simple `filter: grayscale(1)` sur l’ensemble ferait également disparaître le bleu de la tuque et des contours.
- **P20 P : section `#equipe`.** Deux fiches, chacune avec portrait, nom, rôle, courte biographie validée et responsabilités concrètes.
- **P21 P : histoire de l’atelier.** Texte éditorial, dates et événements uniquement après confirmation.
- **P22 P : façon de travailler.** Étapes de collaboration illustrées par de vraies photos disponibles.
- **P23 P : lien vers Contact.** Invitation à présenter un projet, après les informations sur l’équipe.
- **P24 P : pied de page.**

### 7.4 Technique et mobile

La collection `TeamMember` alimente les noms, rôles et biographies. Les versions originales et traitées des portraits restent distinctes. Les photos de l’équipe peuvent être liées aux bios sans mélanger leur ordre visuel et l’ordre du document.

Sur mobile : titre, composition des portraits, légendes Vince/Eduardo, lien vers l’équipe, fiches détaillées, histoire, contact. Le recadrage doit garder les visages et le geste de Vince. Des variantes d’image sont préférables à un recadrage automatique qui couperait les mains.

## 8. Page Contact et demande de devis

### 8.1 Composition

La moitié gauche combine titre, texte, adresse, photographie de la boutique et carte. Le grand panneau de papier blanc occupe environ les 44 % de droite. La clarté de ce panneau distingue le formulaire du reste du site sombre.

### 8.2 Informations et localisation visibles

| ID | Élément | Placement et contenu | Développement |
| --- | --- | --- | --- |
| Q01 | En-tête commun. | Contact actif. | G01 à G18. |
| Q02 | H1. | Haut gauche : **ON EN / PARLE ?** avec carré bleu. | Titre principal de la page. |
| Q03 | Texte d’introduction. | Sous le titre : « Un projet, une idée, une question ? On est là pour en discuter. Écrivez-nous et on vous répond rapidement. » | Contenu éditorial; tout engagement de délai doit être validé. |
| Q04 | Trait bleu. | Sous l’introduction. | Décor. |
| Q05 | Icône de localisation. | À gauche de l’adresse. | SVG cobalt, décoratif puisque l’adresse est écrite à côté. |
| Q06 | Adresse sur deux lignes. | **5825, rue Jean-Talon Est / Saint-Léonard, QC H1S 1M4**. | Texte sélectionnable alimenté par `SiteSettings`. |
| Q07 | Photo de devanture. | Entre le titre et le formulaire, au-dessus de la carte. | Même bâtiment que sur l’accueil; recadrage vertical adapté. |
| Q08 | Cadre de la devanture. | Déchirures et rubans autour de Q07. | Décor. |
| Q09 | Carte. | Partie inférieure gauche. | Le plan dessiné dans le PNG est illustratif et doit être remplacé par une vraie carte. |
| Q10 | Repère et libellé EM Custom Design. | Au centre de la carte illustrative. | La carte de production utilise un lieu réellement vérifié; ne pas reprendre les rues ou le point générés. |
| Q11 | Lien « Itinéraire » et flèche diagonale. | Coin inférieur gauche de la carte. | Ouvre le service de cartographie avec la bonne destination. |
| Q12 | Cadre déchiré et rubans de la carte. | Pourtour de Q09. | Bordure décorative extérieure; ne pas recouvrir les commandes ou attributions du fournisseur de carte. |

**Localisation P/T :** ancre `#nous-trouver`, titre accessible de la carte, adresse utilisable même si la carte ne charge pas, lien d’itinéraire indépendant. Les coordonnées et les heures d’ouverture ne doivent jamais être déduites de l’image générée. Les paramètres de confidentialité du service de cartographie sont à intégrer au choix de fournisseur.

### 8.3 Panneau et champs visibles

| ID | Élément visible | Placement et contenu exact | Contrat de développement proposé |
| --- | --- | --- | --- |
| Q13 | Grande feuille blanche texturée. | Toute la colonne droite, bords déchirés. | Fond de `QuoteForm`; l’intérieur des champs reste sobre pour la lisibilité. |
| Q14 | Titre de formulaire. | En haut : **DEMANDE DE DEVIS.**, noir, carré bleu. | H2 sous le H1 de Contact; conteneur `id="devis"`. |
| Q15 | Étiquette Nom et astérisque. | Premier champ. | Label associé à `name`; obligatoire. |
| Q16 | Champ Nom. | Placeholder **Votre nom**. | `type="text"`, `autocomplete="name"`; accepter accents, espaces et noms composés. Limite proposée : 150 caractères. |
| Q17 | Étiquette Courriel et astérisque. | Sous Nom. | Label associé à `email`; obligatoire. |
| Q18 | Champ Courriel. | Placeholder **votre@courriel.com**. | `type="email"`, `autocomplete="email"`; validation navigateur et serveur. |
| Q19 | Étiquette Votre projet et astérisque. | Sous Courriel. | Label associé à `message`; obligatoire. |
| Q20 | Zone Votre projet. | Grand champ multiligne; « Décrivez-nous votre projet en quelques mots... » | `textarea`; contenu non vide après nettoyage des espaces; plafond proposé de 5 000 caractères. |
| Q21 | Poignée de redimensionnement. | Coin inférieur droit de la zone de texte dans le PNG. | Autoriser l’agrandissement vertical sans casser la largeur du formulaire. |
| Q22 | Étiquette Quantité approximative. | Sous le message. | Champ facultatif; ne pas rendre obligatoire pour un projet Web ou une application. |
| Q23 | Champ Quantité. | Placeholder **Ex. : 50, 100, etc.** | Entier positif lorsqu’il est rempli; vide signifie quantité non définie. Valeur minimale proposée : 1, sans inventer un minimum commercial. |
| Q24 | Étiquette Joindre un visuel. | Sous la quantité. | Champ facultatif. |
| Q25 | Zone de sélection du fichier. | Rectangle à bordure pointillée. | Input fichier associé à toute la zone cliquable; glisser-déposer comme complément. |
| Q26 | Icône trombone. | À gauche dans Q25. | SVG décoratif. |
| Q27 | Texte Choisir un fichier. | À droite du trombone. | Ouvre le sélecteur natif. |
| Q28 | Indication des formats et de la limite. | **JPG, PNG, PDF (max 10 Mo)**. | Un fichier dans le périmètre de base; `.jpg`, `.jpeg`, `.png`, `.pdf`; fixer la limite identique côté client et serveur, par exemple 10 000 000 octets. |
| Q29 | Bouton bleu de soumission. | Sous la pièce jointe, sur presque toute la largeur du panneau. | Véritable `button type="submit"`. |
| Q30 | Libellé Demander un devis et flèche. | Centrés dans Q29. | Un seul contrôle; l’icône ne porte pas le sens seule. |
| Q31 | Texte de contact lié à l’envoi. | Sous le bouton : « En soumettant ce formulaire, vous nous permettez de vous contacter concernant votre demande. » | Texte à valider et à relier à la politique de confidentialité. Ce texte ne correspond pas à une inscription marketing. |
| Q32 | Décors périphériques du panneau. | Papier, plis, traces et bleu autour des bords. | Aucun décor au-dessus des champs ou du focus clavier. |

### 8.4 Éléments de formulaire à ajouter à la maquette

1. Explication de l’astérisque : « * Champs obligatoires ».
2. Champ de contexte facultatif et modifiable : service, fournisseur ou réalisation dont provient la demande.
3. Si le visiteur vient du catalogue, champ facultatif de référence produit.
4. Nom du fichier choisi, poids et commande « Retirer ».
5. Message explicite si le fichier dépasse la limite.
6. Message explicite si le format n’est pas accepté.
7. Erreur sous chaque champ invalide, associée par `aria-describedby`.
8. Résumé d’erreurs atteignable au clavier après une soumission invalide.
9. État d’envoi : libellé « Envoi en cours… » et prévention des clics répétés.
10. État d’échec réseau ou serveur avec possibilité de réessayer et conservation de la saisie.
11. État de succès avec confirmation, référence de demande et explication de la suite.
12. Lien vers la politique de confidentialité.
13. Pied de page après le formulaire, jamais fixé par-dessus le bas des champs.

### 8.5 Validation et comportement

- La validation intervient principalement à la sortie d’un champ déjà utilisé et au moment de l’envoi; pas de message rouge avant toute interaction.
- Les champs gardent leurs vraies étiquettes visibles lorsque les placeholders disparaissent.
- Une erreur contient un texte explicatif et un traitement visuel; la couleur seule ne suffit pas.
- Le brouillon reste en mémoire pendant un changement de thème et, si possible, lors d’un changement de langue. Il n’est pas persisté durablement sans décision explicite.
- La pièce jointe reste liée à la demande; elle ne devient jamais automatiquement un média public du portfolio.
- Le formulaire affiche un succès uniquement après confirmation de son enregistrement par le serveur.
- Un problème d’envoi du courriel interne après enregistrement ne doit pas faire croire au visiteur que sa demande a disparu.
- Les paramètres de contexte dans l’URL sont vérifiés côté serveur et ne constituent pas des données fiables en eux-mêmes.

### 8.6 Mobile

Ordre proposé : titre et introduction courts, formulaire, informations pratiques, photo de boutique, carte, pied de page. Le lien vers `#nous-trouver` permet d’accéder directement à l’adresse. La quantité ouvre un clavier adapté; le courriel un clavier adapté aux adresses. Le panneau blanc prend la largeur disponible avec une marge intérieure suffisante.

## 9. Architecture des données et du serveur

### 9.1 Découpage proposé

Le site comporte une couche de présentation, un contenu éditorial administrable et un traitement serveur pour les demandes. Une architecture de petite taille suffit : pages prérendues ou rendues côté serveur, ressources photographiques optimisées, module d’administration protégé et point d’entrée serveur pour le formulaire. Le choix du framework et de l’hébergement dépendra de l’environnement réel du projet.

Les cinq pages de présentation n’ont pas besoin d’appeler une API à chaque clic. Leur contenu peut arriver avec la page. Le navigateur gère le carrousel, le thème et les interactions locales. L’enregistrement d’un devis appartient au serveur.

### 9.2 Objets de données

| Entité | Champs utiles | Relations et utilisation |
| --- | --- | --- |
| `SiteSettings` | Nom de marque, logo clair/sombre, adresse, coordonnées validées, horaires, identifiant cartographique, liens sociaux. | Source unique du header, footer, Contact et des informations de référencement. |
| `PageContent` | Clé de page, langue, titre, introduction, libellés et métadonnées. | Sépare le contenu éditorial des composants. |
| `MediaAsset` | Identifiant, original, variantes, dimensions, type, texte alternatif FR/EN, légende, point de recadrage, provenance, statut de validation. | Photos de pages, projets et équipe. |
| `Service` | Identifiant, slug, nom FR/EN, résumé, détails, ordre, médias associés. | Services et contexte du devis. |
| `Project` | Identifiant, slug localisé, titre, client validé, description, couverture, galerie, statut, ordre de sélection. | Réalisations, détail de projet et carrousel d’accueil. |
| `ProjectService` | `projectId`, `serviceId`. | Un projet peut concerner plusieurs prestations. |
| `HeroItem` | Type introduction/projet, média ou `projectId`, position, actif. | Permet d’avoir une devanture sur Accueil sans la confondre avec une réalisation client. |
| `Supplier` | Identifiant, nom, URL FR/EN si différente, ordre, état actif, descriptif éventuel. | Lignes de Catalogue; association à un article uniquement si elle est vérifiée. |
| `TeamMember` | Nom, rôle FR/EN, biographie, portrait original et traité, ordre, actif. | À propos et fiches de l’équipe. |
| `Inquiry` | Identifiant interne, référence publique opaque, nom, courriel, message, quantité facultative, langue, contexte, date, statut. | Dossier d’une demande reçue. |
| `InquiryAttachment` | `inquiryId`, clé de stockage privée, nom d’origine, type vérifié, poids, état de vérification. | Fichier facultatif associé à une demande. |
| `NotificationJob` | `inquiryId`, type de notification, statut, tentatives, dates. | Envoi fiable des notifications après enregistrement. |

Les slugs et noms visibles ne remplacent pas les identifiants internes. Les liens entre français et anglais utilisent l’identité commune du contenu. Le choix de thème appartient à la préférence du visiteur et ne duplique pas les données de chaque page.

### 9.3 Contrat proposé pour le formulaire

**Point d’entrée :** `POST /api/demandes`.

**Charge utile :** nom, courriel, message, quantité facultative, langue, service/projet/fournisseur facultatif, référence produit facultative, pièce jointe facultative et clé d’idempotence. La provenance n’autorise aucune action supplémentaire; elle sert à comprendre la demande.

| Situation | Réponse proposée | Effet dans l’interface |
| --- | --- | --- |
| Demande enregistrée. | `201`, référence de demande et état accepté. | Confirmation, sans promettre un devis déjà calculé. |
| Erreur de saisie. | `422`, erreurs associées aux champs. | Correction ciblée; données conservées. |
| Fichier trop volumineux. | `413`. | Rappel de la limite de 10 Mo. |
| Format non accepté. | `415`. | Invitation à choisir JPG, PNG ou PDF. |
| Trop de tentatives. | `429`, délai de nouvelle tentative si disponible. | Message compréhensible et préservation de la saisie. |
| Service temporairement indisponible. | `503` ou erreur serveur générique maîtrisée. | Réessayer; aucun détail interne exposé. |

### 9.4 Cycle d’une demande

1. Le visiteur soumet le formulaire. Le navigateur vérifie les erreurs immédiatement corrigeables.
2. Le serveur vérifie à nouveau les champs, les identifiants de contexte, la taille et le type du fichier.
3. La pièce jointe éventuelle est déposée dans un stockage privé avec un nom généré. Les fichiers douteux restent indisponibles au traitement normal tant que leur vérification n’est pas terminée.
4. Le serveur enregistre la demande et un travail de notification. La base garantit l’unicité de la clé d’idempotence pour éviter deux dossiers lors d’un nouvel essai identique.
5. La réponse de réussite est envoyée au navigateur dès que l’enregistrement durable est confirmé.
6. Une notification interne est envoyée à l’adresse configurée pour l’équipe. L’adresse du visiteur peut servir de `Reply-To`, tandis que l’expéditeur utilise le domaine autorisé du site.
7. Un accusé de réception peut être envoyé au visiteur dans sa langue. Il confirme la réception et n’annonce pas un prix calculé.
8. L’équipe consulte le dossier et ses fichiers avec un accès autorisé.
9. Si une notification échoue, elle est réessayée sans recréer la demande.
10. Les fichiers orphelins d’un envoi interrompu sont nettoyés. La durée de conservation des demandes et des pièces jointes doit être définie avec l’entreprise.

La validation côté navigateur ne remplace pas celle du serveur [T2]. Pour les pièces jointes, la sélection des extensions, la vérification du contenu, les limites et le stockage privé se complètent [T3].

### 9.5 Administration nécessaire

L’administration peut être assurée par un CMS existant ou une petite interface protégée. Ses besoins sont :

- Modifier les textes français et anglais.
- Remplacer les images et leurs recadrages.
- Renseigner les textes alternatifs.
- Ajouter, trier, publier et retirer une réalisation.
- Choisir les cinq projets mis en avant.
- Relier les projets aux services.
- Modifier les fournisseurs et leurs URL.
- Mettre à jour l’équipe, l’adresse, les coordonnées et les heures validées.
- Consulter les demandes et leur statut : nouveau, en traitement, répondu, fermé.
- Accéder aux pièces jointes de façon autorisée.
- Identifier les notifications échouées et les reprendre.

Ces écrans d’administration ne sont pas représentés par les six maquettes publiques.

## 10. Médias, thèmes, traductions et états

### 10.1 Inventaire des ressources disponibles

| Ressource | Utilisation prévue | Vérification d’intégration |
| --- | --- | --- |
| `sources/logo-original.png` | En-tête et pied de page. | Réemployer le vrai fichier; conserver les proportions et la transparence. |
| `sources/devanture.png` | Accueil et Contact. | Préserver l’enseigne réelle et l’architecture. Prévoir deux recadrages. |
| `sources/ricova2.webp` | Réalisations, aperçu Accueil et détail Catalogue. | Le gros plan peut dépasser la résolution utile de la source; demander un original plus grand si nécessaire. |
| `sources/buono.webp` | Réalisations et aperçu Accueil. | Conserver les inscriptions du visuel d’origine. |
| `sources/elevate.webp` | Services et Réalisations. | Respecter le motif du chandail et ses couleurs. |
| `sources/3dsign.webp` | Services et Réalisations. | Enseigne MA; technique de production à confirmer. |
| `sources/balloon.webp` | Cinquième projet proposé. | Visuel Balloon Babe sur textile; contenu du projet à documenter. |
| `sources/emcap.webp` | Composition Catalogue. | Photos de casquettes; attribution à un fournisseur non établie. |
| `sources/vince.png` | À propos. | Contrôler gris de la peau, cheveux noirs, tuque bleue et alpha. |
| `sources/eduardo.png` | À propos. | Contrôler gris de la peau, contours bleus, cadrage et alpha. |

À produire séparément : variantes de masques déchirés, texture de fond optimisée, éclaboussures, rubans, repères, icônes SVG, véritable donnée cartographique et fichiers de police autorisés.

Les PNG de maquette ont pu réinterpréter des détails des images. La construction finale doit repartir des fichiers d’origine et des détourages approuvés. Les en-têtes, textes et boutons ne doivent pas être extraits comme images d’un screenshot de page.

### 10.2 Thème clair

- Remplacer le fond principal par un papier clair et la typographie principale par du noir.
- Garder le cobalt comme accent.
- Employer une variante officielle du logo lisible sur clair.
- Recomposer les bords de papier pour qu’ils restent visibles; ne pas simplement inverser les couleurs de toute la page.
- Conserver les couleurs réelles des photos et les portraits déjà traités.
- Recontrôler les séparateurs, états actifs, champs et focus.
- Prévoir le panneau du formulaire dans une matière distincte du fond clair.

### 10.3 Version anglaise

- Traduire navigation, textes, métadonnées, champs, aides, erreurs, boutons et messages serveur.
- Conserver noms de personnes, marques et références d’articles.
- Refaire les retours à la ligne des grands titres.
- Le sélecteur EN rejoint la traduction du contenu actuel grâce à son identifiant commun.
- Éviter qu’un changement de langue efface silencieusement un formulaire commencé.
- La notification de confirmation reprend la langue de la demande.

### 10.4 Matrice des principaux états à dessiner

| Composant | États requis |
| --- | --- |
| Navigation | Normal, survol, focus, page active, menu mobile ouvert et fermé. |
| Langue | FR actif, EN actif, traduction momentanément indisponible avec destination explicite. |
| Thème | Sombre, clair, état initial selon préférence. |
| Lien sur papier | Normal, survol, focus, activation. |
| Carrousel | Premier média, autres médias, navigation clavier, tactile, chargement d’une image, image indisponible, un seul média. |
| Catalogue | Ligne normale, survol/focus, fournisseur désactivé ou URL à remplacer. |
| Galerie projet | Vue normale et, si retenue, vue agrandie ouverte/fermée avec focus restauré. |
| Formulaire | Vide, prérempli, saisie, erreur par champ, erreur globale, envoi, réussite, échec réseau. |
| Fichier | Aucun fichier, sélectionné, retrait, trop gros, format incorrect, vérification. |
| Carte | Avant chargement, chargée, indisponible; adresse et lien d’itinéraire toujours présents. |
| Pages | Chargement initial stable, contenu introuvable, erreur temporaire. |

## 11. Qualité d’intégration et critères d’acceptation

### 11.1 Accessibilité et interaction

- Navigation et boutons utilisables au clavier, focus toujours visible.
- Hiérarchie H1/H2/H3 cohérente, landmarks et noms accessibles.
- Texte ordinaire avec contraste d’au moins 4,5:1; grands textes au moins 3:1 selon les définitions WCAG. Le bleu utilisé pour de petits libellés doit être mesuré, pas seulement jugé visuellement [T4].
- Cibles tactiles de 44 × 44 px ou plus comme objectif de confort du projet; une petite barre de pagination peut avoir une zone de clic invisible plus grande.
- Taille de texte et zoom ne provoquant ni chevauchement ni disparition d’action.
- Photos informatives décrites; décors ignorés par les lecteurs d’écran.
- Carrousel utilisable sans glissement obligatoire, avec commandes nommées et annonce raisonnable du média sélectionné [T1].
- Animation courte et discrète; variante sans déplacement marqué pour la préférence de mouvement réduit.
- Formulaire avec labels persistants, erreurs reliées aux champs et confirmation annoncée.

### 11.2 Performance et construction

- Conserver des originaux puis produire des variantes adaptées aux dimensions affichées, avec `srcset` et `sizes`.
- Indiquer largeur, hauteur ou ratio pour stabiliser la mise en page.
- Donner la priorité à l’image principale au-dessus du premier défilement; différer les médias suivants et ceux plus bas.
- Employer les détourages transparents avec un format et une compression appropriés.
- Réutiliser les textures et composants pour éviter une duplication lourde sur six pages.
- Garder des formes de déchirures propres à chaque composition; partager l’outil technique ne signifie pas imposer la même silhouette partout.
- Limiter les animations aux transformations et à l’opacité lorsque possible.
- Le changement de thème, la traduction ou le chargement d’une police ne doit pas déplacer le bouton principal hors d’atteinte.
- Vérifier à 360, 390, 768, 1 024, 1 440 et 1 920 px comme échantillons de contrôle, puis dans les zones où le contenu commence réellement à se heurter.

### 11.3 Référencement et liens

- Titres et descriptions spécifiques par page et par langue.
- URL stables, correspondances linguistiques, liens canoniques et sitemap issus des contenus publiés.
- Les fiches de réalisations sont des pages partageables et accessibles par des liens ordinaires.
- Les données d’établissement correspondent à la même fiche que l’adresse de Contact.
- Aucun horaire, avis, prix ou caractéristique commerciale inventé dans les données structurées.
- Les liens de devis gardent le contexte utile sans révéler de données personnelles dans l’URL.

### 11.4 Critères propres aux pages

| Page | Contrôle indispensable |
| --- | --- |
| Accueil | Une seule action principale de devis; devanture fidèle; compteur égal au nombre de médias; cinq projets réellement accessibles. |
| Services | Six prestations dans le bon ordre; chaque lien rejoint une section; contexte de service transféré au devis. |
| Réalisations | Image, légende, compteur et destination de « Voir le projet » correspondent toujours au même projet. |
| Catalogue | Chaque fournisseur a sa vraie URL; aucune association produit/fournisseur non vérifiée; carrés colorés sans ambiguïté de fonction. |
| À propos | Portraits attribués aux bonnes personnes; peau en gris, contour bleu; section équipe réellement atteignable. |
| Contact | Adresse et destination cartographique concordantes; fichier contrôlé; validation et confirmation vérifiées; données conservées en cas d’échec. |

## 12. Ce qu’il reste à figer pour transmettre le dossier à un intégrateur

1. Police exacte et variantes autorisées du logo.
2. Versions haute résolution des photos qui le nécessitent.
3. Origine validée du petit détail textile sur À propos.
4. Libellés définitifs et informations des cinq projets.
5. Compteur d’accueil corrigé si la devanture accompagne cinq projets.
6. Contenus de détail des six services.
7. Biographies et ordre des légendes de Vince et Eduardo.
8. URL définitives des six fournisseurs.
9. Fonction finale des quatre repères colorés de Catalogue.
10. Véritable carte, coordonnées et horaires confirmés.
11. Contenu des sections situées sous les six premiers écrans.
12. Pied de page commun.
13. Gabarit de détail d’une réalisation.
14. États de formulaire, de fichier et de confirmation.
15. Déclinaisons mobile, claire et anglaise.

Ces points précisent les éléments absents ou ambigus; ils ne remettent pas en cause la direction artistique retenue. Le site doit être intégré comme un système de textes, photos, masques, interactions et données réutilisables, avec une composition propre à chaque page.

## Références techniques

- **T1.** W3C WAI, [Carousels Tutorial](https://www.w3.org/WAI/tutorials/carousels/), consulté le 26 septembre 2026 : navigation clavier, maîtrise du mouvement et annonces accessibles.
- **T2.** W3C WAI, [Validating Input](https://www.w3.org/WAI/tutorials/forms/validation/), consulté le 26 septembre 2026 : champs requis, erreurs et validation côté serveur.
- **T3.** OWASP, [File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html), consulté le 26 septembre 2026 : validation, limitations et stockage des fichiers.
- **T4.** W3C, [Understanding SC 1.4.3: Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), consulté le 26 septembre 2026 : contraste du texte.

