"""Interface d'administration du site : https://emvisions.ca/admin/
Decap CMS (logiciel libre, licence MIT) modifie les fichiers du dossier contenu/ directement dans le dépôt GitHub.
Chaque « Publier » crée un commit ; Netlify reconstruit alors le site (environ une minute).
Decap est servi depuis le site lui-même (out/admin/decap-<version>/), sans CDN.
ADMIN_LOCAL=1 : essai sur ce poste avec decap-server (aucun compte GitHub nécessaire)."""
import os, json
DECAP = 'decap-3.17.3'
REPO = 'DavidJ97/em-visions'
BRANCH = os.environ.get('ADMIN_BRANCH', 'version-2')

def _s(name, label, hint=None, req=True, **k):
    f = {'name': name, 'label': label, 'widget': 'string', 'required': req, **k}
    if hint: f['hint'] = hint
    return f
def _t(name, label, hint=None, req=True):
    return _s(name, label, hint, req, widget='text')
def _hidden(name):
    return {'name': name, 'label': name, 'widget': 'hidden', 'required': False}
def _fr_en(name, label, long=False, hint=None):
    w = _t if long else _s
    return [w(name + '_fr', label + ' (français)', hint), w(name + '_en', label + ' (anglais)', 'Laissé vide : le texte français est affiché sur la page anglaise.', req=False)]

HEURE = {'pattern': ['^([01][0-9]|2[0-3]):[0-5][0-9]$', 'Format 24 h, par exemple 09:00 ou 17:30']}
def _jour(k, label):
    return {'name': k, 'label': label, 'widget': 'object', 'collapsed': False, 'fields': [
        {'name': 'ouvert', 'label': 'Ouvert', 'widget': 'boolean', 'default': False, 'required': False},
        _s('de', 'Ouverture', 'Ex. : 09:00', req=False, **HEURE), _s('a', 'Fermeture', 'Ex. : 17:00', req=False, **HEURE)]}

def config(local=False):
    files = [
        {'name': 'coordonnees', 'label': 'Coordonnées', 'file': 'contenu/coordonnees.json', 'fields': [
            _s('telephone', 'Téléphone', 'Ex. : (514) 244-9810. Laissé vide : aucun numéro sur le site.', req=False),
            _s('courriel', 'Courriel public', 'Affiché dans le pied de page et la politique de confidentialité. Laissé vide : aucun courriel affiché.', req=False,
               pattern=['^$|^[^@\\s]+@[^@\\s]+\\.[a-zA-Z]{2,}$', 'Adresse courriel invalide']),
            _s('instagram', 'Lien Instagram', 'Adresse complète, ex. : https://www.instagram.com/visionsem/',
               pattern=['^https://(www\\.)?instagram\\.com/[A-Za-z0-9._/-]+$', 'Doit commencer par https://www.instagram.com/'])]},
        {'name': 'heures', 'label': 'Heures d’ouverture', 'file': 'contenu/heures.json', 'fields': [
            {'name': 'afficher', 'label': 'Afficher les heures sur le site', 'widget': 'boolean', 'default': True, 'required': False}]
            + [_jour(k, l) for k, l in (('lundi', 'Lundi'), ('mardi', 'Mardi'), ('mercredi', 'Mercredi'), ('jeudi', 'Jeudi'), ('vendredi', 'Vendredi'), ('samedi', 'Samedi'), ('dimanche', 'Dimanche'))]},
        {'name': 'accueil', 'label': 'Accueil', 'file': 'contenu/accueil.json', 'fields':
            _fr_en('titre', 'Grand titre') + _fr_en('texte', 'Phrase sous le logo') + _fr_en('lieu', 'Petite ligne (lieu)')},
        {'name': 'a-propos', 'label': 'À propos', 'file': 'contenu/a-propos.json', 'fields':
            _fr_en('texte', 'Présentation', long=True) + [
            {'name': 'equipe', 'label': 'Équipe', 'label_singular': 'personne', 'widget': 'list', 'required': False, 'max': 6, 'summary': '{{fields.nom}}',
             'fields': [_s('nom', 'Nom')] + _fr_en('role', 'Rôle')}]},
        {'name': 'services', 'label': 'Services', 'file': 'contenu/services.json', 'fields': [
            {'name': 'services', 'label': 'Les six services', 'label_singular': 'service', 'widget': 'list', 'min': 6, 'max': 6, 'allow_add': False,
             'allow_remove': False, 'allow_reorder': False,
             'hint': 'Chaque service garde son illustration : seuls les textes changent.', 'summary': '{{fields.titre_fr}}',
             'fields': _fr_en('titre', 'Titre') + _fr_en('texte', 'Description') + [_hidden('image_fr'), _hidden('image_en')]}]},
        {'name': 'realisations', 'label': 'Réalisations', 'file': 'contenu/realisations.json', 'fields': [
            {'name': 'realisations', 'label': 'Projets', 'label_singular': 'projet', 'widget': 'list', 'summary': '{{fields.client}} — {{fields.type_fr}}',
             'hint': 'Le premier projet de la liste est le premier affiché. Glissez les projets pour changer l’ordre.',
             'fields': [_s('client', 'Client'), _s('client_en', 'Nom en anglais', 'Seulement si le nom change en anglais.', req=False)]
                + _fr_en('type', 'Type de travail', hint='Ex. : T-shirts imprimés, Enseigne, Lettrage de vitrine')
                + [{'name': 'photos', 'label': 'Photos', 'label_singular': 'photo', 'widget': 'list', 'min': 1, 'summary': '{{fields.fr}}',
                    'hint': 'La première photo sert de vignette dans la grille. JPG ou PNG ; elle est réduite et convertie automatiquement.',
                    'fields': [{'name': 'image', 'label': 'Image', 'widget': 'image', 'choose_url': False, 'media_library': {'config': {'multiple': False}}},
                               _s('fr', 'Description de la photo (français)', 'Ce qu’on voit sur la photo, pour les personnes non voyantes et Google.'),
                               _s('en', 'Description de la photo (anglais)', req=False), _hidden('miniature')]},
                   {'name': 'video', 'label': 'Vidéo', 'widget': 'hidden', 'required': False}]}]},
    ]
    c = {'backend': {'name': 'github', 'repo': REPO, 'branch': BRANCH, 'squash_merges': True,
                     'commit_messages': {'create': 'Contenu : ajout de {{slug}} (admin)', 'update': 'Contenu : {{slug}} mis à jour (admin)',
                                         'delete': 'Contenu : {{slug}} supprimé (admin)', 'uploadMedia': 'Contenu : photo {{path}} ajoutée (admin)',
                                         'deleteMedia': 'Contenu : photo {{path}} retirée (admin)'}},
         'locale': 'fr', 'site_url': 'https://emvisions.ca', 'display_url': 'https://emvisions.ca', 'logo_url': '/img/icon-512.png',
         'show_preview_links': False, 'media_folder': 'contenu/images', 'public_folder': '/img/contenu',
         'slug': {'encoding': 'ascii', 'clean_accents': True},
         'collections': [{'name': 'site', 'label': 'Site', 'editor': {'preview': False}, 'delete': False, 'files': files}]}
    if local: c['local_backend'] = True
    return c

def write(out='out'):
    d = os.path.join(out, 'admin'); os.makedirs(d, exist_ok=True)
    if not os.path.isfile(os.path.join(d, DECAP, 'decap-cms.js')):
        raise SystemExit(f'{d}/{DECAP}/decap-cms.js manquant (fichiers de Decap CMS)')
    # YAML est un sur-ensemble de JSON : config.yml est écrit en JSON, que Decap lit sans souci
    open(os.path.join(d, 'config.yml'), 'w').write(json.dumps(config(os.environ.get('ADMIN_LOCAL') == '1'), ensure_ascii=False, indent=1) + '\n')
    open(os.path.join(d, 'index.html'), 'w').write(
        '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="robots" content="noindex, nofollow"><title>Administration — EM Visions</title>'
        '<link rel="icon" href="../img/favicon-32.png" sizes="32x32" type="image/png"></head>'
        f'<body><script src="{DECAP}/decap-cms.js"></script></body></html>\n')
