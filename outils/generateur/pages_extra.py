"""Pages de texte hors de la page principale : politique de confidentialité (FR et EN)."""
import html as H, os
from config import SITE_URL, CONTACT_EMAIL, INSTAGRAM, PRIVACY_OFFICER, RETENTION_YEARS, POLICY_DATE, GA_ID, CONSENT_MONTHS, fontface
import securite
ADDR='5825, rue Jean-Talon Est, Saint-Léonard (Québec) H1S 1M4'
def _mail(L):
    if not CONTACT_EMAIL: return ''
    return (' ou par courriel à ' if L=='fr' else ' or by email at ')+f'<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>'
def _cookies(L):
    """Section « Témoins » : ce que le site garde dans le navigateur, et Google Analytics s'il est activé."""
    m=CONSENT_MONTHS
    if L=='fr':
        h='<h2 id="temoins">Témoins (cookies)</h2><p>Le site ne dépose aucun témoin publicitaire. Il garde seulement, dans votre navigateur : votre choix de thème clair ou sombre, le fait que l’écran de chargement a déjà été vu pendant la visite et, pendant une heure au plus, la maquette 3D que vous préparez pour la joindre à votre demande. Ces informations restent sur votre appareil et ne nous sont pas transmises.</p>'
        if GA_ID: h+=(f'<p>Seulement si vous l’acceptez, le site utilise Google Analytics (Google LLC, États-Unis) pour compter les visites et savoir quelles pages sont consultées. Google Analytics dépose alors deux témoins, « _ga » et « _ga_… », conservés au plus 13 mois. Aucune fonction publicitaire n’est activée et ces données ne servent pas à vous identifier.</p>'
                      f'<p>Si vous refusez, aucun de ces témoins n’est déposé. Votre choix est retenu {m} mois ; vous pouvez le changer en tout temps : {securite.link("fr")}.</p>')
        else: h+='<p>Le site n’utilise aucun outil de mesure d’audience ni aucune technologie qui vous identifie, vous localise ou dresse votre profil.</p>'
        return h
    h='<h2 id="temoins">Cookies</h2><p>The site sets no advertising cookies. It only keeps, in your browser: whether you chose the light or dark theme, whether the loading screen was already shown during your visit and, for one hour at most, the 3D mockup you are preparing so it can be attached to your request. This information stays on your device and is not sent to us.</p>'
    if GA_ID: h+=(f'<p>Only if you accept, the site uses Google Analytics (Google LLC, United States) to count visits and see which pages are viewed. Google Analytics then sets two cookies, “_ga” and “_ga_…”, kept for up to 13 months. No advertising feature is enabled and this data is not used to identify you.</p>'
                  f'<p>If you decline, none of these cookies are set. Your choice is remembered for {m} months; you can change it at any time: {securite.link("en")}.</p>')
    else: h+='<p>The site uses no audience measurement tool and no technology that identifies you, locates you or builds a profile of you.</p>'
    return h
def body(L):
    yrs={'fr':{1:'un an',2:'deux ans',3:'trois ans'},'en':{1:'one year',2:'two years',3:'three years'}}[L].get(RETENTION_YEARS,str(RETENTION_YEARS))
    if L=='fr': return f'''
<p class="date">Dernière mise à jour : {POLICY_DATE[0]}</p>
<p class="lead">EM Visions (EM Custom Design), {ADDR}, exploite ce site. Cette page explique simplement quels renseignements personnels nous recueillons et ce que nous en faisons.</p>
<h2>Ce que nous recueillons</h2>
<p>Seulement ce que vous écrivez dans le formulaire de demande de devis : votre nom, votre courriel, la description de votre projet, la quantité souhaitée et, si vous en joignez un, votre fichier (logo ou visuel).</p>
<p>Comme pour tout site web, l’hébergeur du site reçoit automatiquement des données techniques (adresse IP, type d’appareil et de navigateur) nécessaires à l’affichage des pages. Nous ne nous en servons pas pour vous identifier.</p>
<h2>Pourquoi nous les recueillons</h2>
<p>Uniquement pour répondre à votre demande, préparer un devis et, si vous devenez client, réaliser votre commande. Nous ne vendons ni ne louons vos renseignements, et nous ne vous envoyons pas de publicité sans votre accord.</p>
<p>Rien ne vous oblige à utiliser le formulaire : vous pouvez aussi passer à l’atelier. Sans vos coordonnées, nous ne pouvons simplement pas vous répondre à distance.</p>
<h2>Qui y a accès</h2>
<p>Les membres de l’équipe d’EM Visions qui traitent les demandes de devis, et personne d’autre.</p>
<p>Le site est hébergé par Netlify, qui reçoit aussi les demandes envoyées par le formulaire (avec le fichier joint) et nous les transmet ; le service Akismet les analyse pour écarter le pourriel. Ces fournisseurs, comme notre fournisseur de courriel, peuvent traiter et conserver ces renseignements à l’extérieur du Québec, notamment aux États-Unis.</p>
{_cookies('fr')}
<h2>Combien de temps nous les gardons</h2>
<p>Une demande qui ne mène pas à une commande est supprimée au plus tard {yrs} après notre dernier échange. Si vous devenez client, nous gardons ce qui est nécessaire à la facturation pendant la durée exigée par la loi.</p>
<h2>Comment nous les protégeons</h2>
<p>Les échanges avec le site sont chiffrés (HTTPS), les demandes sont gardées dans un espace protégé par mot de passe et l’accès est limité aux personnes qui en ont besoin. Si un incident présentait un risque sérieux pour vous, nous vous en aviserions, ainsi que la Commission d’accès à l’information.</p>
<h2>Vos droits</h2>
<p>Vous pouvez demander à consulter les renseignements que nous avons sur vous, à les faire corriger ou supprimer, ou retirer votre consentement à ce que nous communiquions avec vous. Écrivez à la personne responsable ci-dessous : nous répondons dans les 30 jours.</p>
<p>Si notre réponse ne vous convient pas, vous pouvez vous adresser à la <a href="https://www.cai.gouv.qc.ca/" target="_blank" rel="noopener">Commission d’accès à l’information du Québec</a>.</p>
<h2>Personne responsable</h2>
<p>{H.escape(PRIVACY_OFFICER)}, responsable de la protection des renseignements personnels chez EM Visions.<br>Par la poste ou en personne : {ADDR}{_mail(L)}.</p>
<h2>Modifications</h2>
<p>Si cette politique change, la nouvelle version est publiée sur cette page avec sa date de mise à jour.</p>'''
    return f'''
<p class="date">Last updated: {POLICY_DATE[1]}</p>
<p class="lead">EM Visions (EM Custom Design), {ADDR}, runs this website. This page explains in plain terms what personal information we collect and what we do with it.</p>
<h2>What we collect</h2>
<p>Only what you write in the quote request form: your name, your email, the description of your project, the quantity you need and, if you attach one, your file (logo or artwork).</p>
<p>As with any website, the site host automatically receives technical data (IP address, device and browser type) needed to display the pages. We do not use it to identify you.</p>
<h2>Why we collect it</h2>
<p>Only to answer your request, prepare a quote and, if you become a client, carry out your order. We do not sell or rent your information, and we do not send you advertising without your agreement.</p>
<p>You are never required to use the form: you can also drop by the workshop. Without your contact details, we simply cannot reply to you remotely.</p>
<h2>Who has access</h2>
<p>The members of the EM Visions team who handle quote requests, and no one else.</p>
<p>The site is hosted by Netlify, which also receives the requests sent through the form (with the attached file) and forwards them to us; the Akismet service screens them for spam. These providers, like our email provider, may process and store this information outside Québec, including in the United States.</p>
{_cookies('en')}
<h2>How long we keep it</h2>
<p>A request that does not lead to an order is deleted no later than {yrs} after our last exchange. If you become a client, we keep what is needed for invoicing for the period required by law.</p>
<h2>How we protect it</h2>
<p>Exchanges with the site are encrypted (HTTPS), requests are kept in a password-protected space and access is limited to the people who need it. If an incident posed a serious risk to you, we would notify you and the Commission d’accès à l’information.</p>
<h2>Your rights</h2>
<p>You may ask to see the information we hold about you, to have it corrected or deleted, or withdraw your consent to being contacted by us. Write to the person in charge below: we reply within 30 days.</p>
<p>If our answer does not satisfy you, you may contact the <a href="https://www.cai.gouv.qc.ca/" target="_blank" rel="noopener">Commission d’accès à l’information du Québec</a>.</p>
<h2>Person in charge</h2>
<p>{H.escape(PRIVACY_OFFICER)}, person in charge of the protection of personal information at EM Visions.<br>By mail or in person: {ADDR}{_mail(L)}.</p>
<h2>Changes</h2>
<p>If this policy changes, the new version is published on this page with its update date.</p>'''
T={'fr':{'title':'Politique de confidentialité','desc':'Quels renseignements personnels le site EM Visions recueille, pourquoi, pendant combien de temps, et comment exercer vos droits.','back':'Retour au site','path':'/confidentialite/','other':('EN','../en/privacy/'),'home':'../','up':'../'},
   'en':{'title':'Privacy policy','desc':'What personal information the EM Visions website collects, why, for how long, and how to exercise your rights.','back':'Back to the site','path':'/en/privacy/','other':('FR','../../confidentialite/'),'home':'../','up':'../../'}}
CSS='''*{box-sizing:border-box;margin:0;padding:0}:root{--bg:#fff;--fg:#000;--mut:#5f5f5f;--line:#d9d9d9;--blue:#0a3cff}
html[data-theme=dark]{--bg:#000;--fg:#fff;--mut:#a8a8a8;--line:#333;--blue:#8aa1ff}
body{background:var(--bg);color:var(--fg);font:400 17px/1.6 Archivo,Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--blue);text-underline-offset:3px}a:focus-visible,button:focus-visible{outline:3px solid var(--blue);outline-offset:3px}
header{display:flex;align-items:center;justify-content:space-between;gap:16px;max-width:760px;margin:0 auto;padding:22px 20px;border-bottom:1px solid var(--fg)}
.logo{display:block;width:130px;height:62px;color:var(--fg)}.logo svg{width:100%;height:100%;display:block}
nav{display:flex;gap:22px;align-items:center;font-weight:500;font-size:14.5px;letter-spacing:.03em;text-transform:uppercase}nav a{color:var(--fg);text-decoration:none}nav a:hover{text-decoration:underline}
main{max-width:760px;margin:0 auto;padding:34px 20px 90px}
h1,h2{font-style:italic;font-weight:900;font-stretch:115%;letter-spacing:-.02em;text-transform:uppercase;text-wrap:balance}
h1{font-size:clamp(30px,6.4vw,52px);line-height:1}
.date{color:var(--mut);font-size:14.5px;margin-top:22px}.lead{font-size:19px;line-height:1.55;margin-top:14px}
h2{font-size:20px;line-height:1.2;margin-top:40px;padding-top:22px;border-top:1px solid var(--line)}
p{margin-top:12px;max-width:66ch}.cklink{color:var(--blue);text-decoration:underline;text-underline-offset:3px}'''
HEADJS='(function(){let t;try{t=localStorage.getItem("em-theme")}catch(e){}if(t!=="light"&&t!=="dark")t="light";document.documentElement.dataset.theme=t})()'
def page(L,logo_vb,logo_d):
    t=T[L]; e=H.escape; up=t['up']
    ff=fontface(up)
    return (f'<!doctype html><html lang="{L}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(t["title"])} — EM Visions</title>'
      f'<meta name="description" content="{e(t["desc"])}"><link rel="canonical" href="{SITE_URL}{t["path"]}">'
      f'<link rel="alternate" hreflang="fr-CA" href="{SITE_URL}/confidentialite/"><link rel="alternate" hreflang="en-CA" href="{SITE_URL}/en/privacy/">'
      f'<link rel="icon" href="{up}img/favicon.svg" type="image/svg+xml"><link rel="icon" href="{up}img/favicon-32.png" sizes="32x32" type="image/png"><meta name="theme-color" content="#ffffff">'
      f'<script>{HEADJS}</script><style>{ff}{CSS}</style></head><body>'
      f'<header><a class="logo" href="{t["home"]}" aria-label="EM Visions"><svg viewBox="{logo_vb}" aria-hidden="true"><path fill="currentColor" fill-rule="evenodd" d="{logo_d}"/></svg></a>'
      f'<nav><a href="{t["home"]}">← {e(t["back"])}</a><a href="{t["other"][1]}" hreflang="{t["other"][0].lower()}" lang="{t["other"][0].lower()}">{t["other"][0]}</a></nav></header>'
      f'<main><h1>{e(t["title"])}</h1>{body(L)}</main>{securite.banner(L,up,"")}</body></html>')
def write(logo_vb,logo_d):
    for L,d in (('fr','out/confidentialite'),('en','out/en/privacy')):
        os.makedirs(d,exist_ok=True); open(d+'/index.html','w').write(page(L,logo_vb,logo_d))
