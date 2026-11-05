"""Réglages du site EM Visions. Tout ce qui risque de changer est ici."""
import os
# Adresse du site (le domaine de la boutique).
SITE_URL=os.environ.get('SITE_URL','https://emvisions.ca').rstrip('/')
# Courriel qui reçoit les demandes de devis. None tant que la nouvelle adresse n'existe pas
# (info@emvisions.ca rebondit). Dès qu'il est rempli : il apparaît dans le pied de page et la
# politique de confidentialité. Les demandes elles-mêmes passent par Netlify Forms (voir plus bas) :
# l'adresse qui les reçoit se règle dans Netlify (Forms > Form notifications), pas ici.
CONTACT_EMAIL=os.environ.get('CONTACT_EMAIL') or None
INSTAGRAM='https://instagram.com/visionsem'
# Heures d'ouverture — À CONFIRMER avec EM (sûr à 90 %). Le samedi est soit midi–14 h, soit
# 10 h–14 h : on affiche midi–14 h, la plage commune aux deux. Mettre HOURS=None pour les masquer.
HOURS=[(['Monday','Tuesday','Wednesday','Thursday','Friday'],'09:00','17:00'),(['Saturday'],'12:00','14:00')]
HOURS_FR=['Lun–ven : 9 h à 17 h','Sam : 12 h à 14 h']
HOURS_EN=['Mon–Fri: 9 am to 5 pm','Sat: 12 pm to 2 pm']
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
# Texte de présentation de la section À propos (remplace le bouton « Découvrir notre équipe »).
ABOUT_FR='Ouvert depuis la pandémie, EM Visions est un atelier de Saint-Léonard qui s’occupe de design graphique, d’impression et de vêtements personnalisés. Vous arrivez avec une idée, on la mène jusqu’au produit fini. Passez nous voir, rue Jean-Talon Est.'
ABOUT_EN='Open since the pandemic, EM Visions is a Saint-Léonard workshop handling graphic design, printing and custom apparel. You come in with an idea, we take it all the way to the finished product. Come see us on Jean-Talon Street East.'
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
