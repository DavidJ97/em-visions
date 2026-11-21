# Contrôles de qualité

Lancés automatiquement par GitHub (`.github/workflows/qualite.yml`) à chaque envoi sur la branche `version-2`.

- **html-validate** : HTML valide sur toutes les pages de `site/`.
- **stylelint + use-baseline** : le CSS n'utilise que des fonctions disponibles dans tous les navigateurs (Baseline « largement disponible ») ;
  `overscroll-behavior` et `resize` sont permis : sans eux, rien ne casse.
- **pa11y-ci** (axe + HTML_CodeSniffer) : accessibilité WCAG 2 AA sur les 7 pages, servies avec les vrais en-têtes de sécurité.

En local : `npm ci --ignore-scripts` (avec `PUPPETEER_SKIP_DOWNLOAD=1`), puis les mêmes commandes que dans le fichier de GitHub.
Pour pa11y en local, remplacer `executablePath` dans `pa11y.json` par le chemin de Chrome sur la machine.
