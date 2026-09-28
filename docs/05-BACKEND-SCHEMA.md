# 5. Backend Schema — EM Visions

> Objectif : définir les données stockées, leurs relations et les règles d'accès. Base : Cloudflare D1 (SQLite) via Drizzle.

## Entités
| Entité | Représente |
| --- | --- |
| `site_settings` | Coordonnées, adresse, horaires, réseaux (1 ligne) |
| `page_content` | Textes éditoriaux par page et par langue |
| `media_asset` | Photo/vidéo avec variantes, alt FR/EN, provenance |
| `service` | Une des 6 prestations |
| `project` | Une réalisation (Ricova, Buono, Elevate, MA, Balloon Babe…) |
| `project_service` | Lien plusieurs-à-plusieurs projet ↔ service |
| `hero_item` | Élément du carrousel d'accueil (intro ou projet) |
| `supplier` | Fournisseur de catalogue |
| `team_member` | Membre de l'équipe |
| `inquiry` | Demande de devis reçue |
| `inquiry_attachment` | Fichier joint à une demande (R2) |
| `notification_job` | Envoi de courriel à fiabiliser |

## Tables
| Table | Champs (type) | Requis | Défauts | Index |
| --- | --- | --- | --- | --- |
| `site_settings` | id INTEGER PK, brand TEXT, address TEXT, phone TEXT, email TEXT, hours_json TEXT, maps_url TEXT, instagram TEXT, updated_at INTEGER | brand, address | id=1 | — |
| `page_content` | id PK, page_key TEXT, locale TEXT('fr','en'), field TEXT, value TEXT | toutes | — | UNIQUE(page_key, locale, field) |
| `media_asset` | id TEXT PK (uuid), kind TEXT('image','video'), src TEXT, poster TEXT NULL, width INT, height INT, alt_fr TEXT, alt_en TEXT, source TEXT, validated INT | id, kind, src | validated=0 | — |
| `service` | id TEXT PK, slug TEXT, name_fr, name_en, summary_fr, summary_en, display_order INT, media_id TEXT FK | slug, names, order | — | UNIQUE(slug), (display_order) |
| `project` | id PK, slug TEXT, title TEXT, client TEXT NULL, summary_fr, summary_en, cover_id FK, video_id FK NULL, status TEXT('draft','published'), featured_order INT NULL | slug, title, status | status='draft' | UNIQUE(slug), (status, featured_order) |
| `project_service` | project_id FK, service_id FK | les deux | — | PK(project_id, service_id) |
| `hero_item` | id PK, type TEXT('intro','project'), media_id FK NULL, project_id FK NULL, position INT, active INT | type, position | active=1 | (active, position) |
| `supplier` | id PK, name TEXT, url_fr TEXT, url_en TEXT NULL, display_order INT, active INT | name, url_fr | active=1 | (display_order) |
| `team_member` | id PK, name TEXT, role_fr, role_en, bio_fr NULL, bio_en NULL, portrait_id FK, display_order INT | name, roles | — | — |
| `inquiry` | id TEXT PK, public_ref TEXT, name TEXT(≤150), email TEXT, message TEXT(≤5000), quantity INT NULL, locale TEXT, context_type TEXT NULL, context_id TEXT NULL, product_ref TEXT NULL, idempotency_key TEXT, status TEXT, created_at INT | name, email, message, idempotency_key | status='new' | UNIQUE(public_ref), UNIQUE(idempotency_key), (status, created_at) |
| `inquiry_attachment` | id PK, inquiry_id FK, r2_key TEXT, original_name TEXT, mime TEXT, size INT, scan_status TEXT | inquiry_id, r2_key | scan_status='pending' | (inquiry_id) |
| `notification_job` | id PK, inquiry_id FK, kind TEXT('internal','ack'), status TEXT, attempts INT, last_error TEXT NULL, next_at INT | inquiry_id, kind | status='queued', attempts=0 | (status, next_at) |

## Relations
- `project` 1—N `project_service` N—1 `service` (plusieurs-à-plusieurs).
- `project`, `service`, `team_member`, `hero_item` → `media_asset` (N—1).
- `inquiry` 1—N `inquiry_attachment` ; `inquiry` 1—N `notification_job`.
- `inquiry.context_id` → `service`, `project` ou `supplier` selon `context_type` (sans clé étrangère stricte).

## Propriété des données
Pas de comptes clients : toutes les données appartiennent à EM Visions. Une demande est liée au courriel du visiteur seulement.

## Authentification
Public : aucune. Admin : Cloudflare Access (courriels autorisés) → session 12 h ; déconnexion = fin de session Access.

## Autorisations
| Entité | Public | Admin |
| --- | --- | --- |
| Contenus (settings, page_content, service, project publié, supplier, team, media validé) | Lire | Lire, créer, modifier, supprimer |
| `inquiry` | Créer uniquement (via API) | Lire, modifier statut, supprimer |
| `inquiry_attachment` | Créer (via API) | Lire (URL signée 5 min), supprimer |
| `notification_job` | — | Lire, relancer |

## Validation
- `name` 1–150 car., accents et tirets acceptés ; `email` format RFC simplifié ; `message` 1–5000 car. après trim ; `quantity` entier ≥ 1 ou vide.
- Fichier : `.jpg/.jpeg/.png/.pdf`, type réel vérifié, ≤ 10 000 000 octets, 1 fichier.
- `context_type/context_id` vérifiés côté serveur, ignorés s'ils sont inconnus.
- Codes : 201, 422 (champs), 413 (taille), 415 (format), 429 (débit), 503.

## Rétention et suppression
Demandes 24 mois puis purge ; pièces jointes 12 mois ; fichiers orphelins (envoi interrompu) purgés après 24 h ; export CSV des demandes pour l'admin ; suppression sur demande du visiteur (Loi 25).

## Migration et données initiales
- Migrations Drizzle versionnées (`drizzle/0000_*.sql`).
- Seed : settings (5825, rue Jean-Talon Est, Saint-Léonard, QC H1S 1M4 ; info@emvisions.ca ; @visionsem), 6 services, 5 projets, 6 fournisseurs, 2 membres, 5 éléments de carrousel.
