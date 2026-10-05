# Générateur du site

`site/index.html`, `site/en/index.html`, `site/robots.txt` et `site/sitemap.xml` sont produits par `build2.py`. On ne les modifie pas à la main : on change le générateur, puis on reconstruit.

## Reconstruire
```bash
pip install numpy pillow opencv-python scipy playwright brotli && playwright install chromium
mkdir -p out && cp -r ../../site/img ../../site/fonts ../../site/vid out/
python3 build2.py            # écrit out/index.html, out/en/index.html, out/robots.txt, out/sitemap.xml
cp out/index.html ../../site/ && cp out/en/index.html ../../site/en/ && cp out/robots.txt out/sitemap.xml ../../site/
cp out/confidentialite/index.html ../../site/confidentialite/ && cp out/en/privacy/index.html ../../site/en/privacy/
```

## Réglages courants : `config.py`
| Réglage | Effet |
| --- | --- |
| `CONTACT_EMAIL` | Vide pour l'instant. Une fois rempli : le courriel apparaît dans le pied de page et la politique de confidentialité, et le formulaire de devis envoie les demandes à cette adresse (par FormSubmit). À la première demande, FormSubmit envoie un courriel de confirmation à cliquer une fois. |
| `HOURS`, `HOURS_FR`, `HOURS_EN` | Heures d'ouverture (provisoires, à confirmer) |
| `ABOUT_FR`, `ABOUT_EN` | Texte de la section À propos |
| `PRIVACY_OFFICER`, `RETENTION_YEARS` | Politique de confidentialité |
| `SITE_URL` | Adresse du site |

## Changer l'adresse du site (passage au vrai domaine)
L'adresse sert à l'adresse canonique, à l'aperçu de partage, aux données d'entreprise et au sitemap. Un seul réglage :
```bash
SITE_URL=https://exemple.ca python3 build2.py
```
ou modifier la valeur par défaut de `SITE_URL` dans `build2.py`.

## Fichiers
| Fichier | Rôle |
| --- | --- |
| `build2.py` | Page d'ordinateur, styles, script, en-tête de référencement |
| `mobile.py` | Mise en page du téléphone, liens des fournisseurs (`SUP_URL`) |
| `i18n.py` | Traductions anglaises |
| `config.py` | Réglages (courriel, heures, textes, adresse du site) |
| `pages_extra.py` | Politique de confidentialité, en français et en anglais |
| `en_page.py` | Écrit la version anglaise statique (`site/en/`) |
| `elements.json`, `meta.json`, `cal2.json`, `var2.json` | Positions et textes relevés sur les maquettes |
