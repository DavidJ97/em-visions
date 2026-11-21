# Guides de qualité web pour l'assistant de code

Copies figées (lues avant d'être ajoutées) de deux dépôts de fiches, utilisées pour auditer le site.
On ne les installe pas avec `npx` : on garde ces copies et on les met à jour à la main, après relecture.

| Dossier | Source | Version copiée | Licence |
|---|---|---|---|
| `web-quality-skills/` | [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills) (non officiel, par Addy Osmani) : performance, Core Web Vitals, accessibilité WCAG 2.2, SEO, bonnes pratiques | commit `afa8da9` (24 août 2026) | MIT (voir LICENSE) |
| `web-design-guidelines/` | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills), fiche `web-design-guidelines` : règles d'interface | commit `5a37a63` (20 nov. 2026) ; règles figées, SHA-256 vérifié `d246b026…0234` | MIT |

Retiré à la copie : le script `web-quality-audit/scripts/analyze.sh` (inutile ici).

Ces fiches complètent celles de [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance), lues directement dans le dépôt
(si on utilise son outil en ligne de commande : figer la version et mettre `DISABLE_TELEMETRY=1`).
