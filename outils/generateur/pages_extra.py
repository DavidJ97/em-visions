"""Pages de texte hors de la page principale : politique de confidentialité (FR et EN)."""
import html as H, os
from config import SITE_URL, CONTACT_EMAIL, INSTAGRAM, PRIVACY_OFFICER, RETENTION_YEARS, POLICY_DATE, FORM_SERVICE
ADDR='5825, rue Jean-Talon Est, Saint-Léonard (Québec) H1S 1M4'
def _mail(L):
    if not CONTACT_EMAIL: return ''
    return (' ou par courriel à ' if L=='fr' else ' or by email at ')+f'<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>'
def body(L):
    yrs={'fr':{1:'un an',2:'deux ans',3:'trois ans'},'en':{1:'one year',2:'two years',3:'three years'}}[L].get(RETENTION_YEARS,str(RETENTION_YEARS))
    if L=='fr': return f'''
<p class="date">Dernière mise à jour : {POLICY_DATE[0]}</p>
<p class="lead">EM Visions (EM Custom Design), {ADDR}, exploite ce site. Cette page explique simplement quels renseignements personnels nous recueillons et ce que nous en faisons.</p>
<h2>Ce que nous recueillons</h2>
<p>Seulement ce que vous écrivez dans le formulaire de demande de devis : votre nom, votre courriel, la description de votre projet, la quantité souhaitée et, si vous en joignez un, votre fichier (logo ou visuel).</p>
<p>Le site n’utilise ni témoins (cookies) publicitaires, ni outil de mesure d’audience, ni technologie qui vous identifie, vous localise ou dresse votre profil. Il retient seulement, dans votre navigateur, votre choix de thème clair ou sombre ; cette information ne nous est pas transmise.</p>
<p>Comme pour tout site web, l’hébergeur du site reçoit automatiquement des données techniques (adresse IP, type d’appareil et de navigateur) nécessaires à l’affichage des pages. Nous ne nous en servons pas pour vous identifier.</p>
<h2>Pourquoi nous les recueillons</h2>
<p>Uniquement pour répondre à votre demande, préparer un devis et, si vous devenez client, réaliser votre commande. Nous ne vendons ni ne louons vos renseignements, et nous ne vous envoyons pas de publicité sans votre accord.</p>
<p>Rien ne vous oblige à utiliser le formulaire : vous pouvez aussi passer à l’atelier. Sans vos coordonnées, nous ne pouvons simplement pas vous répondre à distance.</p>
<h2>Qui y a accès</h2>
<p>Les membres de l’équipe d’EM Visions qui traitent les demandes de devis, et personne d’autre.</p>
<p>Le formulaire est acheminé jusqu’à notre boîte de courriel par un fournisseur de services ({FORM_SERVICE}). Ce fournisseur et notre fournisseur de courriel peuvent traiter et conserver ces renseignements à l’extérieur du Québec.</p>
<h2>Combien de temps nous les gardons</h2>
<p>Une demande qui ne mène pas à une commande est supprimée au plus tard {yrs} après notre dernier échange. Si vous devenez client, nous gardons ce qui est nécessaire à la facturation pendant la durée exigée par la loi.</p>
<h2>Comment nous les protégeons</h2>
<p>Les échanges avec le site sont chiffrés (HTTPS) et l’accès aux demandes est limité aux personnes qui en ont besoin. Si un incident présentait un risque sérieux pour vous, nous vous en aviserions, ainsi que la Commission d’accès à l’information.</p>
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
<p>The site uses no advertising cookies, no audience measurement tool and no technology that identifies you, locates you or builds a profile of you. It only remembers, in your browser, whether you chose the light or dark theme; that information is not sent to us.</p>
<p>As with any website, the site host automatically receives technical data (IP address, device and browser type) needed to display the pages. We do not use it to identify you.</p>
<h2>Why we collect it</h2>
<p>Only to answer your request, prepare a quote and, if you become a client, carry out your order. We do not sell or rent your information, and we do not send you advertising without your agreement.</p>
<p>You are never required to use the form: you can also drop by the workshop. Without your contact details, we simply cannot reply to you remotely.</p>
<h2>Who has access</h2>
<p>The members of the EM Visions team who handle quote requests, and no one else.</p>
<p>The form is delivered to our mailbox by a service provider ({FORM_SERVICE}). That provider and our email provider may process and store this information outside Québec.</p>
<h2>How long we keep it</h2>
<p>A request that does not lead to an order is deleted no later than {yrs} after our last exchange. If you become a client, we keep what is needed for invoicing for the period required by law.</p>
<h2>How we protect it</h2>
<p>Exchanges with the site are encrypted (HTTPS) and access to requests is limited to the people who need it. If an incident posed a serious risk to you, we would notify you and the Commission d’accès à l’information.</p>
<h2>Your rights</h2>
<p>You may ask to see the information we hold about you, to have it corrected or deleted, or withdraw your consent to being contacted by us. Write to the person in charge below: we reply within 30 days.</p>
<p>If our answer does not satisfy you, you may contact the <a href="https://www.cai.gouv.qc.ca/" target="_blank" rel="noopener">Commission d’accès à l’information du Québec</a>.</p>
<h2>Person in charge</h2>
<p>{H.escape(PRIVACY_OFFICER)}, person in charge of the protection of personal information at EM Visions.<br>By mail or in person: {ADDR}{_mail(L)}.</p>
<h2>Changes</h2>
<p>If this policy changes, the new version is published on this page with its update date.</p>'''
T={'fr':{'title':'Politique de confidentialité','desc':'Quels renseignements personnels le site EM Visions recueille, pourquoi, pendant combien de temps, et comment exercer vos droits.','back':'Retour au site','path':'/confidentialite/','other':('EN','../en/privacy/'),'home':'../','up':'../'},
   'en':{'title':'Privacy policy','desc':'What personal information the EM Visions website collects, why, for how long, and how to exercise your rights.','back':'Back to the site','path':'/en/privacy/','other':('FR','../../confidentialite/'),'home':'../','up':'../../'}}
CSS='''*{box-sizing:border-box;margin:0;padding:0}:root{--bg:#0a0a0a;--fg:#f4f4f2;--mut:#b9b9b6;--line:#2c2c2c;--blue:#4d74ff}
html[data-theme=light]{--bg:#efefec;--fg:#141414;--mut:#555;--line:#cfcfcb;--blue:#0a3cff}
body{background:var(--bg);color:var(--fg);font:400 17px/1.62 'Kumbh Sans',system-ui,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--blue);text-underline-offset:3px}a:focus-visible{outline:3px solid #6f8cff;outline-offset:3px}
header{display:flex;align-items:center;justify-content:space-between;gap:16px;max-width:760px;margin:0 auto;padding:22px 20px}
.logo{display:block;width:150px;height:70px;color:var(--fg)}.logo svg{width:100%;height:100%;display:block}
nav{display:flex;gap:22px;align-items:center;font-weight:600;font-size:15px}nav a{color:var(--fg)}
main{max-width:760px;margin:0 auto;padding:26px 20px 90px}
h1{font:400 clamp(26px,6.2vw,44px)/1.14 Sekuya,'Kumbh Sans',sans-serif;text-transform:uppercase;letter-spacing:.05em;text-wrap:balance}
h1:after{content:"";display:block;width:72px;height:5px;background:#0a3cff;margin-top:22px}
.date{color:var(--mut);font-size:14.5px;margin-top:22px}.lead{font-size:19px;line-height:1.55;margin-top:14px}
h2{font:700 20px/1.3 'Kumbh Sans',sans-serif;margin-top:40px;padding-top:22px;border-top:1px solid var(--line)}
p{margin-top:12px;max-width:66ch}'''
HEADJS='(function(){let t;try{t=localStorage.getItem("em-theme")}catch(e){}if(t!=="light"&&t!=="dark")t=matchMedia("(prefers-color-scheme: light)").matches?"light":"dark";document.documentElement.dataset.theme=t})()'
def page(L,logo_vb,logo_d):
    t=T[L]; e=H.escape; up=t['up']
    ff=''.join(f"@font-face{{font-family:'{n}';font-weight:{w};font-display:swap;src:url({up}fonts/{f}-normal.woff2) format('woff2')}}" for n,w,f in (('Sekuya',400,'sekuya-latin-400'),('Kumbh Sans',400,'kumbh-sans-latin-400'),('Kumbh Sans',600,'kumbh-sans-latin-600'),('Kumbh Sans',700,'kumbh-sans-latin-700')))
    return (f'<!doctype html><html lang="{L}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(t["title"])} — EM Visions</title>'
      f'<meta name="description" content="{e(t["desc"])}"><link rel="canonical" href="{SITE_URL}{t["path"]}">'
      f'<link rel="alternate" hreflang="fr-CA" href="{SITE_URL}/confidentialite/"><link rel="alternate" hreflang="en-CA" href="{SITE_URL}/en/privacy/">'
      f'<link rel="icon" href="{up}img/favicon.svg" type="image/svg+xml"><link rel="icon" href="{up}img/favicon-32.png" sizes="32x32" type="image/png"><meta name="theme-color" content="#0a0a0a">'
      f'<script>{HEADJS}</script><style>{ff}{CSS}</style></head><body>'
      f'<header><a class="logo" href="{t["home"]}" aria-label="EM Visions"><svg viewBox="{logo_vb}" aria-hidden="true"><path fill="currentColor" fill-rule="evenodd" d="{logo_d}"/></svg></a>'
      f'<nav><a href="{t["home"]}">← {e(t["back"])}</a><a href="{t["other"][1]}" hreflang="{t["other"][0].lower()}" lang="{t["other"][0].lower()}">{t["other"][0]}</a></nav></header>'
      f'<main><h1>{e(t["title"])}</h1>{body(L)}</main></body></html>')
def write(logo_vb,logo_d):
    for L,d in (('fr','out/confidentialite'),('en','out/en/privacy')):
        os.makedirs(d,exist_ok=True); open(d+'/index.html','w').write(page(L,logo_vb,logo_d))
