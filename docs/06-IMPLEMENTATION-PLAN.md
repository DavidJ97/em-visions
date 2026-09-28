# 6. Implementation Plan — EM Visions

> Objectif : une séquence de construction ordonnée avec des points de contrôle. ✅ = fait dans le prototype actuel.

## Jalon 1 — Mise en place
- ✅ Dépôt `DavidJ97/em-visions` : `docs/` (6 documents), `site/` (prototype autonome).
- ⬜ Projet Next.js (`em-visions-composants`) importé dans `app/`, `pnpm install`, `.env` (DB, BUCKET, RESEND_*).
- ⬜ Déploiement Cloudflare (prévisualisation par PR, production sur `main`).

## Jalon 2 — Données et authentification
- ⬜ Schéma Drizzle (doc 5), migration D1, bucket R2 privé.
- ⬜ Seed des contenus.
- ⬜ Cloudflare Access sur `/admin`.
- ⬜ Tests : validation Zod, idempotence, limites de fichier.

## Jalon 3 — Parcours principal
- ✅ Scènes bureau à l'identique (6 sections, calques extraits, textes calés à ±3 px).
- ✅ Page unique défilante, en-tête fixe, ancres FR/EN, section active suivie.
- ✅ Formulaire de devis avec validation client.
- ⬜ Branchement `POST /api/demandes` → D1/R2/Resend, écran MERCI avec référence réelle.

## Jalon 4 — Fonctionnalités secondaires
- ✅ Bilingue FR/EN, thème clair/sombre, responsive mobile/tablette, logo et boutons SVG.
- ✅ Carrousel + vidéos Higgsfield (Buono, MA, Balloon Babe, casquettes).
- ⬜ Vidéos Ricova et Elevate v2 ; héberger les MP4 sur R2.
- ⬜ URL réelles des fournisseurs, vraie carte, fiches projet `/realisations/<slug>`, section équipe.
- ⬜ Administration (demandes, contenus, projets).

## Jalon 5 — Qualité
- ⬜ Audit accessibilité (axe, clavier, lecteur d'écran), contraste du cobalt.
- ⬜ Performance : chargement différé des calques et vidéos, `srcset`, préchargement de l'Accueil.
- ⬜ Sécurité : CSP, limitation de débit, honeypot.
- ⬜ Tests Playwright de régression visuelle (captures comparées aux maquettes, seuil ≤ 8/255 d'écart moyen).

## Jalon 6 — Mise en ligne
- ⬜ Plan de test (formulaire bout en bout, FR/EN, 360/768/1024/1440/1920 px).
- ⬜ DNS emvisions.ca → Cloudflare ; redirections des anciennes pages (`services.html` → `/#services`, etc.).
- ⬜ Retour arrière : déploiement précédent en un clic.
- ⬜ Surveillance : alertes sur `notification_job` en échec, Cloudflare Analytics.

## Format des tâches
| Tâche | Responsable | Entrées | Sortie | Terminé quand | Dépend de |
| --- | --- | --- | --- | --- | --- |
| API demandes | Agent IA | Doc 5, form actuel | Route + tests | 201/422/413/415 OK en test | Schéma D1 |
| Vidéos manquantes | David | Prompts Gemini/Higgsfield | 2 MP4 | Validés visuellement | Crédits |
| URL fournisseurs | EM Visions | — | 6 URL | Liens cliquables testés | — |
| Traduction EN | EM Visions | `site` EN | Textes validés | Relecture signée | — |

## Avant chaque jalon suivant
Lancer le site, vérifier les critères d'acceptation du PRD, noter les problèmes non résolus dans `docs/ISSUES.md`.
