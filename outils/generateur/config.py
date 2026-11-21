"""Réglages du site EM Visions. Tout ce qui risque de changer est ici."""
import os, re
# Adresse du site (le domaine de la boutique).
SITE_URL=os.environ.get('SITE_URL','https://emvisions.ca').rstrip('/')
# Contenu modifiable depuis l'interface /admin : dossier contenu/ (coordonnées, heures, textes, services,
# réalisations). Ce fichier n'est qu'une lecture prudente : une valeur vide ou invalide retombe sur un repli sûr.
import json, datetime
def _contenu():
    """Un fichier par section de /admin : contenu/coordonnees.json, heures.json, accueil.json, a-propos.json, services.json, realisations.json"""
    for d in (os.environ.get('CONTENU'),'contenu','../../contenu'):
        if d and os.path.isfile(os.path.join(d,'accueil.json')):
            C={}
            for k,f in (('coordonnees','coordonnees'),('heures','heures'),('accueil','accueil'),('a_propos','a-propos'),('services','services'),('realisations','realisations')):
                try: o=json.load(open(os.path.join(d,f+'.json'),encoding='utf-8'))
                except (OSError,ValueError) as x: print('contenu illisible, valeurs d’origine gardées :',f,x); o={}
                C[k]=o.get(k,[]) if k in ('services','realisations') else o
            return C,os.path.abspath(d)
    raise SystemExit('dossier contenu/ introuvable')
CONTENU,CONTENU_DIR=_contenu()
def txt(d,k,repli=''):
    v=d.get(k) if isinstance(d,dict) else None
    return v.strip() if isinstance(v,str) and v.strip() else repli
_c=CONTENU.get('coordonnees') or {}
# Courriel public (pied de page, politique de confidentialité). Vide tant que la nouvelle adresse n'existe pas.
# Les demandes de devis passent par Netlify Forms : l'adresse qui les reçoit se règle dans Netlify, pas ici.
_m=os.environ.get('CONTACT_EMAIL') or txt(_c,'courriel')
CONTACT_EMAIL=_m if re.fullmatch(r'[^@\s"<>]+@[^@\s"<>]+\.[a-zA-Z]{2,}',_m or '') else None
_t=re.sub(r'[^0-9+]','',txt(_c,'telephone'))
TELEPHONE=(txt(_c,'telephone'),_t) if len(_t)>=10 else None
_i=txt(_c,'instagram')
INSTAGRAM=_i if re.fullmatch(r'https://(www\.)?instagram\.com/[A-Za-z0-9._/-]+',_i) else 'https://www.instagram.com/visionsem/'
# date de la dernière modification (plan du site, <lastmod>) : celle de la construction
CONTENT_DATE=datetime.date.today().isoformat()
# Heures d'ouverture, jour par jour. « afficher » décoché = heures masquées partout.
_hr=CONTENU.get('heures') or {}
_J=[('lundi','Monday'),('mardi','Tuesday'),('mercredi','Wednesday'),('jeudi','Thursday'),('vendredi','Friday'),('samedi','Saturday'),('dimanche','Sunday')]
def _ok(h): return isinstance(h,str) and re.fullmatch(r'([01]\d|2[0-3]):[0-5]\d',h)
HOURS=[([D],j['de'],j['a']) for k,D in _J for j in [_hr.get(k) or {}] if j.get('ouvert') and _ok(j.get('de')) and _ok(j.get('a')) and j['de']<j['a']] if _hr.get('afficher',True) else []
HOURS=HOURS or None
HOURS_FR=[];HOURS_EN=[]
# Grille de la semaine (lundi d'abord), tirée de HOURS : (jour FR, jour EN, numéro du jour JS, ouverture, fermeture) en FR et EN.
def _h(t,en=False):
    h,m=int(t[:2]),int(t[3:])
    if en: return f"{(h-1)%12+1}{':%02d'%m if m else ''} {'am' if h<12 else 'pm'}"
    return f"{h} h{' %02d'%m if m else ''}"
_D=[('Monday','Lun','Mon',1),('Tuesday','Mar','Tue',2),('Wednesday','Mer','Wed',3),('Thursday','Jeu','Thu',4),('Friday','Ven','Fri',5),('Saturday','Sam','Sat',6),('Sunday','Dim','Sun',0)]
def _slot(d):
    for days,a,b in (HOURS or []):
        if d in days: return (a,b)
WEEK=[(fr,en,n,_slot(d)) for d,fr,en,n in _D]
WEEK_FR=[(fr,n,(_h(s[0]),_h(s[1])) if s else None) for fr,en,n,s in WEEK]
WEEK_EN={**{fr:en for fr,en,n,s in WEEK},**{_h(t):_h(t,True) for fr,en,n,s in WEEK if s for t in s},'Fermé':'Closed','Heures d’ouverture':'Opening hours'}
# Section À propos
_ap=CONTENU.get('a_propos') or {}
ABOUT_FR=txt(_ap,'texte_fr','EM Visions est un atelier de Saint-Léonard.');ABOUT_EN=txt(_ap,'texte_en',ABOUT_FR)
# Politique de confidentialité (Loi 25). Par défaut, la loi désigne la personne qui dirige l'entreprise.
PRIVACY_OFFICER='Eduardo Mazzonna'
RETENTION_YEARS=2          # durée de conservation des demandes sans suite
POLICY_DATE=('3 novembre 2026','November 3, 2026')
# Formulaire de devis : Netlify Forms (le site est hébergé chez Netlify). Netlify repère le formulaire
# au déploiement, garde les demandes (avec la pièce jointe), filtre le pourriel (Akismet) et les envoie
# par courriel. Limite de Netlify : 8 Mo par envoi, d'où le fichier limité à 7 Mo.
FORM_NAME='devis'
FILE_MAX_MB=7
# Mesure d'audience : identifiant Google Analytics 4 (« G-XXXXXXXXXX »). Vide = aucune mesure, aucun
# témoin, pas de bannière. Rempli = bannière de consentement (Loi 25) : Google Analytics ne se charge
# qu'après « Accepter », et le choix peut être changé en tout temps (lien « Témoins » du pied de page).
GA_ID=os.environ.get('GA_ID') or None
CONSENT_MONTHS=12          # le choix est redemandé après ce délai

# Deux polices pour tout le site : Sekuya (titres) et Archivo (tout le reste, en largeur normale ou étroite).
def fontface(up='',swap=True):
    d='font-display:swap;' if swap else ''
    return (f"@font-face{{font-family:'Sekuya';font-weight:400;{d}src:url({up}fonts/sekuya-latin-400-normal.woff2) format('woff2')}}"
            f"@font-face{{font-family:'Archivo';font-weight:100 900;font-stretch:62% 125%;{d}src:url({up}fonts/archivo-latin-wdth-normal.woff2) format('woff2')}}")
