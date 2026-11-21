"""Interface d'administration du site : https://emvisions.ca/admin/
Sveltia CMS (logiciel libre, licence MIT), successeur moderne de Netlify/Decap CMS : il modifie les fichiers du dossier
contenu/ directement dans le dépôt GitHub. Chaque « Enregistrer » crée un commit ; Netlify reconstruit alors le site.
Sveltia est servi depuis le site lui-même (out/admin/sveltia-<version>/), habillé aux couleurs du site (theme.css).
Connexion : GitHub (via Netlify) ou jeton d'accès personnel GitHub."""
import os, json
CMS = 'sveltia-0.262.1'
REPO = 'DavidJ97/em-visions'
BRANCH = os.environ.get('ADMIN_BRANCH', 'version-2')

def _s(name, label, hint=None, req=True, **k):
    f = {'name': name, 'label': label, 'widget': 'string', 'required': req, **k}
    if hint: f['hint'] = hint
    return f
def _t(name, label, hint=None, req=True):
    return _s(name, label, hint, req, widget='text')
def _hidden(name):
    return {'name': name, 'label': name, 'widget': 'hidden'}
def _fr_en(name, label, long=False, hint=None):
    w = _t if long else _s
    return [w(name + '_fr', label + ' (français)', hint), w(name + '_en', label + ' (anglais)', 'Laissé vide : le texte français est affiché sur la page anglaise.', req=False)]

HEURE = {'pattern': ['^([01][0-9]|2[0-3]):[0-5][0-9]$', 'Format 24 h, par exemple 09:00 ou 17:30']}
def _jour(k, label):
    return {'name': k, 'label': label, 'widget': 'object', 'collapsed': False, 'summary': '{{fields.de}} – {{fields.a}}', 'fields': [
        {'name': 'ouvert', 'label': 'Ouvert', 'widget': 'boolean', 'default': False, 'required': False},
        _s('de', 'Ouverture', 'Ex. : 09:00', req=False, **HEURE), _s('a', 'Fermeture', 'Ex. : 17:00', req=False, **HEURE)]}

def config():
    files = [
        {'name': 'coordonnees', 'icon': 'call', 'label': 'Coordonnées', 'file': 'contenu/coordonnees.json', 'fields': [
            _s('telephone', 'Téléphone', 'Ex. : (514) 244-9810. Laissé vide : aucun numéro sur le site.', req=False),
            _s('courriel', 'Courriel public', 'Affiché dans le pied de page et la politique de confidentialité. Laissé vide : aucun courriel affiché.', req=False,
               pattern=['^$|^[^@\\s]+@[^@\\s]+\\.[a-zA-Z]{2,}$', 'Adresse courriel invalide']),
            _s('instagram', 'Lien Instagram', 'Adresse complète, ex. : https://www.instagram.com/visionsem/',
               pattern=['^https://(www\\.)?instagram\\.com/[A-Za-z0-9._/-]+$', 'Doit commencer par https://www.instagram.com/'])]},
        {'name': 'heures', 'icon': 'schedule', 'label': 'Heures d’ouverture', 'file': 'contenu/heures.json', 'fields': [
            {'name': 'afficher', 'label': 'Afficher les heures sur le site', 'widget': 'boolean', 'default': True, 'required': False}]
            + [_jour(k, l) for k, l in (('lundi', 'Lundi'), ('mardi', 'Mardi'), ('mercredi', 'Mercredi'), ('jeudi', 'Jeudi'), ('vendredi', 'Vendredi'), ('samedi', 'Samedi'), ('dimanche', 'Dimanche'))]},
        {'name': 'accueil', 'icon': 'home', 'label': 'Accueil', 'file': 'contenu/accueil.json', 'fields':
            _fr_en('titre', 'Grand titre') + _fr_en('texte', 'Phrase sous le logo') + _fr_en('lieu', 'Petite ligne (lieu)')},
        {'name': 'a-propos', 'icon': 'groups', 'label': 'À propos', 'file': 'contenu/a-propos.json', 'fields':
            _fr_en('texte', 'Présentation', long=True) + [
            {'name': 'equipe', 'label': 'Équipe', 'label_singular': 'personne', 'widget': 'list', 'required': False, 'max': 6, 'summary': '{{fields.nom}}',
             'fields': [_s('nom', 'Nom')] + _fr_en('role', 'Rôle')}]},
        {'name': 'services', 'icon': 'design_services', 'label': 'Services', 'file': 'contenu/services.json', 'fields': [
            {'name': 'services', 'label': 'Les six services', 'label_singular': 'service', 'widget': 'list', 'min': 6, 'max': 6, 'allow_add': False,
             'allow_remove': False, 'allow_reorder': False,
             'hint': 'Chaque service garde son illustration : seuls les textes changent.', 'summary': '{{fields.titre_fr}}',
             'fields': _fr_en('titre', 'Titre') + _fr_en('texte', 'Description') + [_hidden('image_fr'), _hidden('image_en')]}]},
        {'name': 'realisations', 'icon': 'photo_library', 'label': 'Réalisations', 'file': 'contenu/realisations.json', 'fields': [
            {'name': 'realisations', 'label': 'Projets', 'label_singular': 'projet', 'widget': 'list', 'collapsed': True, 'add_to_top': True, 'summary': '{{fields.client}} — {{fields.type_fr}}',
             'hint': 'Le premier projet de la liste est le premier affiché sur le site ; un nouveau projet s’ajoute en haut. Glissez les projets pour changer l’ordre.',
             'fields': [_s('client', 'Client'), _s('client_en', 'Nom en anglais', 'Seulement si le nom change en anglais.', req=False)]
                + _fr_en('type', 'Type de travail', hint='Ex. : T-shirts imprimés, Enseigne, Lettrage de vitrine')
                + [{'name': 'photos', 'label': 'Photos', 'label_singular': 'photo', 'widget': 'list', 'min': 1, 'collapsed': True, 'summary': '{{fields.fr}}',
                    'hint': 'La première photo sert de vignette dans la grille. JPG, PNG ou HEIC (iPhone) ; elle est réduite et convertie automatiquement.',
                    'fields': [{'name': 'image', 'label': 'Image', 'widget': 'image', 'choose_url': False},
                               _s('fr', 'Description de la photo (français)', 'Ce qu’on voit sur la photo, pour les personnes non voyantes et Google.'),
                               _s('en', 'Description de la photo (anglais)', req=False), _hidden('miniature')]},
                   {'name': 'video', 'label': 'Vidéo', 'widget': 'hidden'}]}]},
    ]
    c = {'backend': {'name': 'github', 'repo': REPO, 'branch': BRANCH, 'squash_merges': True,
                     'commit_messages': {'create': 'Contenu : ajout de {{slug}} (admin)', 'update': 'Contenu : {{slug}} mis à jour (admin)',
                                         'delete': 'Contenu : {{slug}} supprimé (admin)', 'uploadMedia': 'Contenu : photo {{path}} ajoutée (admin)',
                                         'deleteMedia': 'Contenu : photo {{path}} retirée (admin)'}},
         'app_title': 'EM Visions — Administration', 'logo': {'src': '/img/icon-512.png'},
         'site_url': 'https://emvisions.ca', 'display_url': 'https://emvisions.ca', 'show_preview_links': False,
         'editor': {'preview': False}, 'media_folder': 'contenu/images', 'public_folder': '/img/contenu',
         # photos réduites et converties en WebP dans le navigateur avant l'envoi (iPhone HEIC compris) : le dépôt reste léger
         'media_libraries': {'default': {'config': {'max_file_size': 30000000,
             'transformations': {'raster_image': {'format': 'webp', 'quality': 85, 'width': 2400, 'height': 2400}}}},
             'stock_assets': {'providers': []}},   # pas de banques de photos : les réalisations sont de vraies photos
         # chaque section directement dans le menu, avec son icône
         'singletons': files}
    return c

# Habillage : mêmes couleurs, même police et mêmes titres que le site (Sveltia se règle par variables CSS --sui-*)
THEME = """@font-face{font-family:'Archivo';font-weight:100 900;font-stretch:62% 125%;font-display:swap;src:url(../fonts/archivo-latin-wdth-normal.woff2) format('woff2')}
html:root,html:root[data-theme]{--sui-font-family-default:'Archivo',Helvetica,Arial,sans-serif;--sui-control-font-family:'Archivo',Helvetica,Arial,sans-serif;
 --sui-base-hue:228;--sui-primary-accent-color:#0a3cff;--sui-primary-accent-color-light:#2f5bff;--sui-primary-accent-color-dark:#0029b8;
 --sui-primary-accent-color-text:#0a3cff;--sui-primary-accent-color-inverted:#fff;--sui-control-medium-border-radius:6px}
html:root,html:root[data-theme=light]{color-scheme:light;
 --sui-foreground-color-1-hsl:0 0% 0%;--sui-foreground-color-2-hsl:0 0% 12%;--sui-foreground-color-3-hsl:0 0% 28%;--sui-foreground-color-4-hsl:0 0% 37%;--sui-foreground-color-5-hsl:0 0% 55%;
 --sui-background-color-1-hsl:0 0% 100%;--sui-background-color-2-hsl:0 0% 98%;--sui-background-color-3-hsl:0 0% 95%;--sui-background-color-4-hsl:0 0% 91%;--sui-background-color-5-hsl:0 0% 84%;
 --sui-border-color-1-hsl:0 0% 46%;--sui-border-color-2-hsl:0 0% 80%;--sui-border-color-3-hsl:0 0% 85%;--sui-shadow-color:0 0% 0%}
html:root[data-theme=dark]{color-scheme:dark;--sui-primary-accent-color-text:#8aa1ff;
 --sui-foreground-color-1-hsl:0 0% 100%;--sui-foreground-color-2-hsl:0 0% 88%;--sui-foreground-color-3-hsl:0 0% 75%;--sui-foreground-color-4-hsl:0 0% 66%;--sui-foreground-color-5-hsl:0 0% 45%;
 --sui-background-color-1-hsl:0 0% 0%;--sui-background-color-2-hsl:0 0% 4%;--sui-background-color-3-hsl:0 0% 8%;--sui-background-color-4-hsl:0 0% 12%;--sui-background-color-5-hsl:0 0% 22%;
 --sui-border-color-1-hsl:0 0% 55%;--sui-border-color-2-hsl:0 0% 22%;--sui-border-color-3-hsl:0 0% 16%;--sui-shadow-color:0 0% 0%}
h1,h2,h3,[role=heading]{font-weight:900;font-stretch:115%;letter-spacing:-.01em;text-transform:uppercase}
/* boutons comme sur le site : pilule, majuscules */
.sui.button.primary,.sui.button.secondary{border-radius:999px;text-transform:uppercase;letter-spacing:.04em;font-weight:500;padding-inline:20px}
.sui.button.primary:not(:disabled){background:#0a3cff;border-color:#0a3cff;color:#fff}
/* barre du haut : noire, comme l'en-tête du site */
.toolbar-wrapper>.sui.toolbar.primary[role=toolbar]{background:#000;color:#fff;--sui-primary-foreground-color:#fff;--sui-secondary-foreground-color:#e6e6e6;
 --sui-hover-background-color:#262626;--sui-active-background-color:#333;--sui-selected-background-color:#333}
.toolbar-wrapper>.sui.toolbar.primary[role=toolbar] .sui.button:not(.primary){color:#fff}
.toolbar-wrapper>.sui.toolbar.primary[role=toolbar] .sui.button.primary{background:#0a3cff;color:#fff}
/* page de connexion : fond noir et logo chromé, comme l'accueil du site */
.sui.app-shell .main:has(> .container img.logo){background:#000;color:#fff;--sui-primary-foreground-color:#fff;--sui-secondary-foreground-color:#ccc}
.sui.app-shell .main:has(> .container img.logo) img.logo{width:min(420px,80vw);height:auto;content:url(../img/logo-chrome-768.webp)}
.sui.app-shell .main:has(> .container img.logo) h1{color:#fff;font-size:clamp(22px,3vw,32px)}
.sui.app-shell .main:has(> .container img.logo) .sui.button.secondary{background:transparent;color:#fff;border:1px solid #fff}
.sui.app-shell .main:has(> .container img.logo) .sui.button.secondary:hover{background:#fff;color:#000}
.sui.app-shell .main:has(> .container img.logo) .powered-by{color:#8a8a8a}
.sui.app-shell .main:has(> .container img.logo) .buttons{width:min(440px,92vw)}
.sui.app-shell .main:has(> .container img.logo) .buttons .sui.button{width:100%;min-height:46px;font-size:14px;white-space:normal}
"""

def write(out='out'):
    d = os.path.join(out, 'admin'); os.makedirs(d, exist_ok=True)
    if not os.path.isfile(os.path.join(d, CMS, 'sveltia-cms.js')):
        raise SystemExit(f'{d}/{CMS}/sveltia-cms.js manquant (fichiers de Sveltia CMS)')
    # YAML est un sur-ensemble de JSON : config.yml est écrit en JSON, que Sveltia lit sans souci
    open(os.path.join(d, 'config.yml'), 'w').write(json.dumps(config(), ensure_ascii=False, indent=1) + '\n')
    open(os.path.join(d, 'theme.css'), 'w').write(THEME)
    open(os.path.join(d, 'index.html'), 'w').write(
        '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="robots" content="noindex, nofollow"><title>Administration — EM Visions</title>'
        '<link rel="icon" href="../img/favicon-32.png" sizes="32x32" type="image/png"><link rel="stylesheet" href="theme.css"></head>'
        f'<body><script src="{CMS}/sveltia-cms.js"></script></body></html>\n')
