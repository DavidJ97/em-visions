# 1. Product Requirements Document (PRD) — EM Visions

> Objectif : définir ce que le site doit faire et comment on mesure son succès.

## Produit et idée en une phrase
**EM Visions** — le site vitrine bilingue d'un atelier d'impression et de personnalisation de Saint-Léonard (Montréal) qui transforme la visite en **demande de devis**.

## Utilisateurs cibles
| Segment | Besoin |
| --- | --- |
| PME et commerces locaux (restos, boutiques, pop-up) | Enseignes, vitrines, textiles de marque, rapidement et localement |
| Entreprises avec équipes terrain (ex. Ricova) | Vêtements de travail personnalisés en quantité |
| Créateurs, marques émergentes, événements | Merch (t-shirts, casquettes), design graphique, petites séries |
| Clients numériques | Sites Web et applications sur mesure |

## Problème et solution de contournement actuelle
- Le site actuel (emvisions.ca) montre des images sans parcours clair ni vraie mise en avant des services.
- Les clients écrivent sur Instagram / par courriel, sans structure : il manque quantité, visuel, contexte → allers-retours.

## Objectif et mesure du succès
| Objectif | Signal mesurable (90 jours après lancement) |
| --- | --- |
| Générer des demandes qualifiées | ≥ 15 demandes de devis/mois via le formulaire |
| Demandes complètes | ≥ 70 % avec quantité ou visuel joint |
| Crédibilité | Temps moyen sur Réalisations ≥ 45 s |
| Accessibilité / perf | Lighthouse ≥ 90 (perf, a11y) sur mobile |

## Fonctionnalités clés
| # | Fonctionnalité | Bénéfice | Priorité |
| --- | --- | --- | --- |
| F1 | Page unique défilante : Accueil, Services, Réalisations, Catalogue, À propos, Contact | Parcours fluide, un seul lien à partager | P0 |
| F2 | Formulaire de devis (nom, courriel, projet, quantité, visuel ≤ 10 Mo) | Demandes complètes | P0 |
| F3 | Carrousel de réalisations (photos + vidéos en boucle) | Preuve du savoir-faire | P0 |
| F4 | Bilingue FR/EN avec URL propres (`#services`, `#en/work`) | Clientèle anglophone | P0 |
| F5 | Responsive ordinateur / tablette / mobile | 60 %+ du trafic est mobile | P0 |
| F6 | Thème clair / sombre (mémorisé) | Confort, identité | P1 |
| F7 | Répertoire des 6 fournisseurs (S&S, Canada Sportswear, Fabrik, Eside, Just Like Hero, Projob) | Choisir un support | P1 |
| F8 | Carte + itinéraire vers la boutique | Visites en personne | P1 |
| F9 | Administration (demandes, contenus, projets) | Autonomie de l'équipe | P2 |

## Hors périmètre v1
Panier et paiement en ligne, prix/stock synchronisés avec les fournisseurs, compte client, blog, chat en direct.

## User stories
- En tant que **gérant de commerce**, je veux **voir des exemples d'enseignes et de vitrines**, afin de **juger la qualité avant de demander un prix**.
- En tant que **responsable d'équipe terrain**, je veux **indiquer une quantité et joindre mon logo**, afin de **recevoir un devis sans aller-retour**.
- En tant que **visiteur anglophone**, je veux **passer à l'anglais sur la même section**, afin de **ne pas perdre ma place**.
- En tant que **visiteur mobile**, je veux **faire défiler le site d'un pouce**, afin de **tout parcourir en 1 minute**.
- En tant que **client potentiel**, je veux **ouvrir l'itinéraire**, afin de **me rendre à la boutique**.
- En tant que **membre de l'équipe EM**, je veux **consulter et classer les demandes**, afin de **répondre vite**.

## Critères d'acceptation
- **Étant donné** le formulaire vide, **quand** je clique « Demander un devis », **alors** chaque champ obligatoire affiche une erreur explicite et le focus va au premier champ invalide.
- **Étant donné** un fichier > 10 Mo ou hors JPG/PNG/PDF, **quand** je le sélectionne, **alors** il est refusé avec un message clair.
- **Étant donné** que je suis sur `#catalogue`, **quand** je clique EN, **alors** j'arrive sur `#en/catalog`, tous les textes sont traduits et la position est conservée.
- **Étant donné** un écran de 360 px, **quand** je parcours le site, **alors** aucun défilement horizontal n'apparaît.
- **Étant donné** que je fais défiler, **quand** une section passe à l'écran, **alors** le menu la souligne et l'URL se met à jour.
- **Étant donné** « réduire les animations » activé, **alors** les vidéos sont remplacées par des photos fixes.

## Questions ouvertes
1. URL définitives des 6 fournisseurs.
2. ~~Police officielle des titres~~ — réglé : Sekuya pour les titres, Archivo pour tout le reste.
3. Validation de la traduction anglaise par EM.
4. Adresse de réception des devis et délai de réponse annoncé.
5. Remplacement des photos générées par les photos originales haute résolution.
6. Hébergement final des vidéos (actuellement servies par Higgsfield).
