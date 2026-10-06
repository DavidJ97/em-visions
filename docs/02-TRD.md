# 2. Technical Requirements Document (TRD) — EM Visions

> Objectif : rendre les choix techniques explicites pour que le build ne repose pas sur des suppositions.

## Plateformes
Web uniquement : navigateurs evergreen (Chrome, Safari, Firefox, Edge — 2 dernières versions), iOS Safari 16+, Android Chrome.

## Frontend et hébergement
| Élément | Choix |
| --- | --- |
| Prototype actuel | HTML/CSS/JS autonome (`site/index.html`), sans framework |
| Cible production | Next.js 16 (App Router) + React 19 — base `em-visions-composants` existante |
| Hébergement | Cloudflare Workers/Pages (via vinext + `@cloudflare/vite-plugin`) |
| Polices | Deux seulement : Sekuya (titres) et Archivo variable (tout le reste, largeur normale ou étroite) — auto-hébergées (woff2, licence OFL) |
| Médias | WebP (photos, calques), SVG (logo, boutons, icônes), MP4 H.264 muet (vidéos) |

## Backend et base de données
| Élément | Choix |
| --- | --- |
| API | Route `POST /api/demandes` (Worker) |
| Base | Cloudflare **D1** (SQLite) via Drizzle ORM |
| Fichiers joints | Cloudflare **R2**, bucket privé |
| Courriels | Resend (`RESEND_API_KEY`, `MAIL_FROM`, `QUOTE_RECIPIENT`) |
| Région | Amérique du Nord (conformité Loi 25 Québec) |

## Authentification et rôles
- Site public : aucune authentification.
- Administration : accès protégé (Cloudflare Access ou mot de passe + session), rôle unique **admin** (équipe EM).

## Services externes et API
| Fournisseur | Rôle | Limites | Propriétaire des accès |
| --- | --- | --- | --- |
| Resend | Notification interne + accusé de réception | 100/jour (gratuit) | EM Visions |
| Google Maps | Lien itinéraire (pas d'API chargée) | — | — |
| Higgsfield | Génération des vidéos en boucle | Crédits du forfait | David Jules |
| Fournisseurs (S&S, etc.) | Liens sortants vers catalogues | — | EM Visions |

## Architecture
```
Navigateur ──► index (HTML statique + calques WebP + SVG + vidéos)
    │  JS : routage par ancre, i18n FR/EN, thème, carrousel, validation
    └─► POST /api/demandes (multipart)
           ├─ validation serveur (Zod)
           ├─ fichier ─► R2 (clé générée, privé)
           ├─ Inquiry + NotificationJob ─► D1 (idempotence)
           └─ Resend ─► équipe EM (+ accusé au client)
Admin ──► /admin (protégé) ─► D1 / R2 (lecture signée)
```
Rendu « à l'identique » : chaque section = une scène 1586 × 880 px (calque décoratif WebP extrait de la maquette + textes HTML positionnés + boutons SVG), mise à l'échelle par `transform: scale()`. En dessous de 1024 px, bascule vers une mise en page en colonne (`.mobile`).

## Sécurité et confidentialité
- Données sensibles : nom, courriel, message, fichier joint.
- Fichiers : liste blanche d'extensions + vérification du type réel, 10 000 000 octets max, stockage privé, jamais publics.
- Anti-abus : limitation de débit (429), honeypot, clé d'idempotence.
- Rétention : demandes 24 mois, pièces jointes 12 mois (à valider avec EM), suppression sur demande.
- En-têtes : CSP stricte, `rel="noopener"` sur liens externes.

## Performance et fiabilité
| Cible | Valeur |
| --- | --- |
| LCP mobile | < 2,5 s |
| CLS | < 0,1 (dimensions fixes pour toutes les scènes) |
| Poids initial | < 1,5 Mo (calques chargés en différé hors Accueil) |
| Disponibilité | 99,9 % (Cloudflare) |
| Sauvegarde | Export D1 quotidien |

## Environnements et livraison
- `main` → production, `develop` → prévisualisation Cloudflare par PR.
- CI GitHub Actions : `tsc --noEmit`, lint, build, tests Playwright (captures 360/768/1440 px comparées aux maquettes).

## Décisions clés et compromis
| Décision | Raison | Alternative écartée |
| --- | --- | --- |
| Calques extraits des maquettes | Déchirures identiques à 1 px près | Masques SVG génériques (pas identiques) |
| Page unique défilante + ancres | Demande client, un seul lien | Pages séparées (rechargements) |
| Logo et boutons en SVG | Netteté, thème clair/sombre | PNG (flou, 2 versions) |
| Vidéos MP4 plutôt que GIF | 10× plus légères, fluides | GIF animés |
| D1 + R2 | Même plateforme que l'hébergement | Supabase (autre fournisseur) |
