# Générateur du site (version 2)

Le site est produit par `build.py`. On ne modifie pas `site/` à la main : on change le générateur, puis on reconstruit.

| Fichier | Rôle |
| --- | --- |
| `build.py` | Construit la page principale en français (`site/`) et en anglais (`site/en/`), le plan du site et `robots.txt` |
| `style.css`, `script.js` | La mise en page et les comportements de la page principale (insérés dans la page) |
| `verre.py` | Prépare l'image du logo pour l'effet de verre de l'accueil (`img/logo-verre.webp`) ; à relancer seulement si le logo change |
| `config.py` | Tout ce qui risque de changer : courriel, heures, texte À propos, adresse du site |
| `realisations.py` | La liste des projets montrés, avec leurs photos et leurs textes FR/EN |
| `i18n.py` | Traductions anglaises communes ; les textes propres à la version 2 sont dans `build.py` (`EN2`) |
| `loader.py` | L'écran de chargement |
| `produits.json` | Couleurs et zones d'impression de chaque produit du catalogue, tirées de `maquette_produits.js` |
| `maquette_page.py`, `maquette_app.js`, `maquette_produits.js` | Le modélisateur 3D |
| `pages_extra.py` | La politique de confidentialité |

## Reconstruire
```bash
mkdir -p out && cp -r ../../site/img ../../site/fonts ../../site/vid ../../site/models ../../site/vendor out/
cp ../modeles/models.json .
python3 build.py                 # écrit le site complet dans out/
rm -rf ../../site && cp -r out ../../site
```

## Réglages courants : `config.py`
| Réglage | Effet |
| --- | --- |
| `CONTACT_EMAIL` | Vide pour l'instant. Une fois rempli : le courriel apparaît dans le pied de page et la politique de confidentialité, et le formulaire de devis envoie les demandes à cette adresse (par FormSubmit). À la première demande, FormSubmit envoie un courriel de confirmation à cliquer une fois. |
| `HOURS` | Heures d'ouverture (provisoires, à confirmer) |
| `ABOUT_FR`, `ABOUT_EN` | Texte de la section À propos |

## Ajouter un projet aux réalisations
Déposer la photo dans `site/img/` en deux tailles (`rea-nom.webp`, 1080 px de large, et `rea-nom-s.webp`, 540 px), puis ajouter une ligne dans `realisations.py` et ses traductions dans le dictionnaire `EN` du même fichier.
