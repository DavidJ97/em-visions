# 4. UI and UX Design Brief — EM Visions

> Objectif : une direction visuelle cohérente et utilisable.

## Public et ton
PME, commerces et créateurs de Montréal. Trois adjectifs : **brut**, **artisanal**, **audacieux**.
Esthétique « collage d'atelier » : papier déchiré, ruban adhésif, éclaboussures d'encre cobalt, pellicule photo.

## Références
| Référence | À emprunter | À éviter |
| --- | --- | --- |
| Affiches punk / zines | Titres massifs, collage | Illisibilité |
| Maquettes EM Visions (6 PNG) | Tout : c'est la source de vérité | — |
| emvisions.ca actuel | Photos réelles | Grille d'images sans parcours |

## Palette
| Rôle | Sombre | Clair |
| --- | --- | --- |
| Fond | `#060606` + grain | `#E9E9E6` papier + grain |
| Texte principal | `#FFFFFF` | `#141414` |
| Accent (cobalt) | `#0A3CFF` | `#0A3CFF` |
| Papier (cadres, boutons) | `#F4F4F2` | `#F4F4F2` + ombre portée |
| Erreur | `#D6002A` | `#D6002A` |
| Couleurs photo conservées | Magenta enseigne, jaune Ricova, rose Elevate | idem |

## Typographie
| Usage | Police | Taille bureau | Taille mobile |
| --- | --- | --- | --- |
| Titres H1 | Anton (épaissi 3 px) | 88–144 px | 58–128 px (17,5 vw) |
| Titres de liste, boutons papier | Oswald 700 | 22–40 px | 22–38 px |
| Navigation | Jost 400/700, capitales espacées | 14 px | 40–64 px (menu plein écran) |
| Texte courant | Kumbh Sans 300 | 20–23 px | 17–23 px |
| Formulaire | Inter 400/500/600 | 16–17 px | 16 px |
| Adresse, itinéraire | Figtree 600 | 18 px | 18 px |

## Composants
- **PaperAction** : bouton sur papier déchiré (SVG), disque noir + flèche.
- **TornFrame** : cadre photo à bords déchirés propre à chaque composition.
- **ProjectCarousel** : grand média + 2 aperçus + flèches rondes + 5 barres.
- **SupplierRow** : ligne fournisseur, bandeau cobalt déchiré au survol.
- **QuoteForm** : feuille blanche, champs bordés, zone fichier pointillée, bouton cobalt.
- **ThemeToggle** : anneau cobalt SVG + lune.
- **InkBrush** (mobile) : coup de pinceau cobalt derrière les titres.
- **Logo** : SVG vectorisé, `currentColor` (blanc/noir selon le thème).

## Règles de mise en page
- Bureau : scènes fixes 1586 × 880 px mises à l'échelle, en-tête 112 px fixe.
- Points de rupture : > 1024 px (scènes), 700–1024 px (tablette, 2 colonnes pour Services), < 700 px (mobile 1 colonne).
- Marges mobile 20 px, tablette 40 px. Espacements 8/16/24/32/48/64.
- Les décors (déchirures, rubans, encre) peuvent déborder de la grille ; le texte non.

## Notes par écran
- **Accueil** : H1 « FAITES BONNE IMPRESSION. », sous-titre, bouton devis, devanture au centre, 2 aperçus verticaux, carrousel.
- **Services** : H1 « DE L'IDÉE À LA MATIÈRE. », 6 prestations numérotées 01–06 sur 2 colonnes, chandail Elevate + enseigne MA (vidéo).
- **Réalisations** : H1 « LE TRAVAIL PARLE. », projet actif + aperçus, « Voir le projet ».
- **Catalogue** : H1 « CHOISISSEZ VOTRE SUPPORT. », 6 fournisseurs, casquettes (vidéo) + gros plan Ricova, 4 repères couleur.
- **À propos** : duo Vince / Eduardo en N&B avec liseré cobalt, H1 « LES GENS DERRIÈRE L'IMPRESSION. ».
- **Contact** : H1 « ON EN PARLE ? », adresse, devanture, carte, formulaire sur feuille blanche.

## Accessibilité
- Contraste texte ≥ 4,5:1 (vérifier le cobalt sur petits textes).
- Tout au clavier, focus visible (contour `#6F8CFF` 3 px), lien « Aller au contenu ».
- Cibles tactiles ≥ 44 × 44 px (barres du carrousel à zone élargie).
- Décors `aria-hidden`, images informatives décrites, `lang` mis à jour FR/EN.
- `prefers-reduced-motion` : vidéos et animations désactivées.

## États d'interaction
| Composant | Survol | Focus | Désactivé | Chargement | Erreur | Succès |
| --- | --- | --- | --- | --- | --- | --- |
| Bouton papier | Légère surbrillance | Contour bleu | — | — | — | — |
| Flèche ronde | Fond cobalt | Contour | Masquée si 1 média | — | — | — |
| Fournisseur | Bandeau cobalt glisse | idem survol | URL manquante → message | — | — | — |
| Champ | — | Bordure cobalt | — | — | Bordure + texte rouges | — |
| Envoyer | Plus lumineux | Contour | Pendant l'envoi | « Envoi en cours… » | Message réseau | Écran MERCI |

## Ressources nécessaires
Logo (SVG ✅), 6 calques décoratifs sombres + 6 clairs (✅), photos originales HD (❌ à fournir), vidéos Ricova et Elevate v2 (❌), polices sous licence (✅ OFL), icônes SVG (✅), vraie carte (❌).
