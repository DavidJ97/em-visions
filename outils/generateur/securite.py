"""Ce qu'il faut pour la mise en ligne chez Netlify :
- bannière de consentement aux témoins (Loi 25) et Google Analytics, seulement si GA_ID est rempli ;
- en-têtes de sécurité (_headers), dont une politique de sécurité du contenu (CSP) calculée à partir
  des scripts réellement présents dans les pages ;
- page 404.
"""
import base64, glob, hashlib, html as H, os, re
from config import GA_ID, CONSENT_MONTHS

# ---------- témoins (cookies) et Google Analytics
TXT={'fr':{'t':'Témoins (cookies)','p':'Nous aimerions compter les visites du site avec Google Analytics. Ces témoins ne servent qu’à mesurer la fréquentation et ne sont déposés que si vous acceptez. Vous pouvez changer d’avis en tout temps.',
           'y':'Accepter','n':'Refuser','more':'En savoir plus','link':'Témoins (cookies)'},
     'en':{'t':'Cookies','p':'We would like to count visits to the site with Google Analytics. These cookies are only used to measure traffic and are only set if you accept. You can change your mind at any time.',
           'y':'Accept','n':'Decline','more':'Learn more','link':'Cookies'}}
CSS=('.consent{position:fixed;left:12px;right:12px;bottom:12px;z-index:70;max-width:560px;margin:0 auto;background:#fff;color:#000;border:1px solid #000;border-radius:6px;'
     'padding:18px 18px 16px;box-shadow:0 10px 40px #0004;font:400 16px/1.45 Archivo,Helvetica,Arial,sans-serif}.consent[hidden]{display:none}'
     '.consent h2{font:900 17px/1.1 Archivo,Helvetica,Arial,sans-serif;font-stretch:115%;text-transform:uppercase;letter-spacing:-.01em;margin:0 0 8px;padding:0;border:0}'
     '.consent p{margin:0;max-width:none}.consent a{color:#000;text-decoration:underline;text-underline-offset:3px}'
     '.consent-b{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px}'
     '.consent-b button{min-height:50px;border:1px solid #000;border-radius:6px;background:#000;color:#fff;font:500 15px Archivo,Helvetica,Arial,sans-serif;letter-spacing:.04em;text-transform:uppercase;cursor:pointer}'
     '.consent-b button:hover{background:#0a3cff;border-color:#0a3cff}.consent button:focus-visible{outline:3px solid #0a3cff;outline-offset:2px}'
     '.cklink{background:none;border:0;padding:5px 0;color:inherit;font:inherit;cursor:pointer;text-align:left}.cklink:hover{text-decoration:underline;text-underline-offset:4px}')

def banner(L,up,priv):
    """Bannière (cachée au départ) et script. Les deux boutons ont la même taille et le même poids."""
    if not GA_ID: return ''
    x=TXT[L]; e=H.escape
    return (f'<style>{CSS}</style><section class="consent" id="consent" aria-labelledby="consent-t" hidden><h2 id="consent-t">{e(x["t"])}</h2>'
            f'<p>{e(x["p"])} <a href="{priv}#temoins">{e(x["more"])}</a></p>'
            f'<div class="consent-b"><button type="button" data-c="no">{e(x["n"])}</button><button type="button" data-c="yes">{e(x["y"])}</button></div></section>'
            f'<script src="{up}js/consent.js" defer></script>')

def link(L):
    """Bouton « Témoins » pour revenir sur son choix (pied de page, politique de confidentialité)."""
    return f'<button type="button" class="cklink" data-consent-open>{H.escape(TXT[L]["link"])}</button>' if GA_ID else ''

CONSENT_JS=r"""(function(){
// Consentement aux témoins (Loi 25) : Google Analytics ne se charge qu'après « Accepter ».
// Mode consentement de Google : tout est refusé par défaut ; aucun témoin publicitaire, même après acceptation.
var ID='%ID%',K='em-consent',V=1,MAX=%MAX%;
window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}window.gtag=gtag;
gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied'});
var box=document.getElementById('consent'),loaded=false;if(!box)return;
function read(){try{var c=JSON.parse(localStorage.getItem(K));if(c&&c.v===V&&Date.now()-c.t<MAX)return c.a}catch(e){}return null}
function save(a){try{localStorage.setItem(K,JSON.stringify({v:V,t:Date.now(),a:a}))}catch(e){}}
function load(){window['ga-disable-'+ID]=false;gtag('consent','update',{analytics_storage:'granted'});if(loaded)return;loaded=true;
 gtag('js',new Date());gtag('config',ID,{cookie_expires:34190000,allow_google_signals:false,allow_ad_personalization_signals:false});
 var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+ID;document.head.appendChild(s)}
function stop(){window['ga-disable-'+ID]=true;gtag('consent','update',{analytics_storage:'denied'});
 var h=location.hostname,ds=['',h,'.'+h.replace(/^www\./,'')];
 document.cookie.split(';').forEach(function(c){var n=c.split('=')[0].trim();if(/^_ga/.test(n))ds.forEach(function(d){document.cookie=n+'=;Max-Age=0;path=/'+(d?';domain='+d:'')})})}
var opener=null;
function show(focus){box.hidden=false;if(focus)box.querySelector('[data-c="no"]').focus()}
function hide(){box.hidden=true;if(opener){opener.focus();opener=null}}
box.addEventListener('click',function(e){var b=e.target.closest('[data-c]');if(!b)return;var a=b.dataset.c==='yes';save(a);hide();a?load():stop()});
box.addEventListener('keydown',function(e){if(e.key==='Escape'&&read()!==null)hide()});
document.addEventListener('click',function(e){var o=e.target.closest('[data-consent-open]');if(o){opener=o;show(true)}});
var a=read();if(a===true)load();else if(a===null)show(false);
})();
"""

def write_consent(out='out'):
    p=os.path.join(out,'js','consent.js')
    if not GA_ID:
        if os.path.exists(p): os.remove(p)
        return
    os.makedirs(os.path.dirname(p),exist_ok=True)
    open(p,'w').write(CONSENT_JS.replace('%ID%',GA_ID).replace('%MAX%',str(CONSENT_MONTHS*30*86400000)))

# ---------- page 404 (chemins absolus : Netlify la sert à n'importe quelle adresse)
def write_404(logo_vb,logo_d,fontface,out='out'):
    e=H.escape
    css=('*{box-sizing:border-box;margin:0;padding:0}body{min-height:100vh;display:grid;place-items:center;background:#fff;color:#000;font:400 17px/1.45 Archivo,Helvetica,Arial,sans-serif;padding:24px}'
         'main{max-width:640px;text-align:center}svg{width:180px;height:auto;display:block;margin:0 auto 34px}'
         'h1{font:900 clamp(34px,8vw,64px)/1 Archivo,Helvetica,Arial,sans-serif;font-stretch:115%;letter-spacing:-.02em;text-transform:uppercase}'
         'p{margin-top:14px;color:#5f5f5f}.b{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:28px}'
         'a{display:inline-flex;align-items:center;min-height:52px;padding:0 24px;border:1px solid #0a3cff;border-radius:6px;background:#0a3cff;color:#fff;text-decoration:none;font-weight:500;font-size:15px;letter-spacing:.04em;text-transform:uppercase}'
         'a.g{background:none;color:#000;border-color:#000}a:focus-visible{outline:3px solid #0a3cff;outline-offset:2px}')
    page=(f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">'
          f'<title>Page introuvable — EM Visions</title><link rel="icon" href="/img/favicon-32.png" sizes="32x32" type="image/png"><style>{fontface("/")}{css}</style></head><body><main>'
          f'<svg viewBox="{logo_vb}" aria-hidden="true"><path fill="currentColor" fill-rule="evenodd" d="{logo_d}"/></svg>'
          f'<h1>Page introuvable</h1><p>Cette page n’existe pas ou a changé d’adresse.</p><p lang="en">This page does not exist or has moved.</p>'
          f'<div class="b"><a href="/">Retour à l’accueil</a><a class="g" href="/en/" lang="en">English</a></div></main></body></html>')
    open(os.path.join(out,'404.html'),'w').write(page)

# ---------- en-têtes de sécurité
GA_SRC={'script':'https://www.googletagmanager.com','connect':'https://*.google-analytics.com https://*.analytics.google.com https://*.googletagmanager.com',
        'img':'https://*.google-analytics.com https://*.googletagmanager.com'}
def inline_hashes(out='out'):
    """Empreintes SHA-256 de chaque script écrit dans les pages (les données JSON-LD ne sont pas du code)."""
    hs=set()
    for f in glob.glob(os.path.join(out,'**','*.html'),recursive=True):
        for attrs,code in re.findall(r'<script(?![^>]*\bsrc=)([^>]*)>(.*?)</script>',open(f).read(),re.S):
            if 'application/ld+json' in attrs: continue
            hs.add("'sha256-"+base64.b64encode(hashlib.sha256(code.encode()).digest()).decode()+"'")
    return sorted(hs)

def csp(out='out'):
    g=GA_SRC if GA_ID else {'script':'','connect':'','img':''}
    parts=["default-src 'self'",
           " ".join(["script-src 'self' 'wasm-unsafe-eval'",*inline_hashes(out),g['script']]).strip(),
           "style-src 'self' 'unsafe-inline'",           # styles écrits dans les pages (aucun risque d'exécution)
           f"img-src 'self' data: blob: {g['img']}".strip(),
           "font-src 'self'","media-src 'self' blob:",
           f"connect-src 'self' data: blob: {g['connect']}".strip(),
           "worker-src 'self' blob:","frame-src 'none'","object-src 'none'","base-uri 'self'","form-action 'self'",
           "frame-ancestors 'none'","upgrade-insecure-requests"]
    return '; '.join(parts)

def write_headers(out='out'):
    rules=[('/*',[('Content-Security-Policy',csp(out)),('X-Content-Type-Options','nosniff'),('Referrer-Policy','strict-origin-when-cross-origin'),
                  ('Permissions-Policy','camera=(), microphone=(), geolocation=(), payment=(), usb=(), browsing-topics=()'),
                  ('X-Frame-Options','DENY'),('Cross-Origin-Opener-Policy','same-origin'),('Strict-Transport-Security','max-age=31536000')]),
           ('/fonts/*',[('Cache-Control','public, max-age=31536000, immutable')])]
    rules+=[(f'/{d}/*',[('Cache-Control','public, max-age=604800')]) for d in ('img','vid','models','vendor')]
    open(os.path.join(out,'_headers'),'w').write('# En-têtes envoyés par Netlify (généré par securite.py, ne pas modifier à la main)\n'
        +''.join(p+'\n'+''.join(f'  {k}: {v}\n' for k,v in hs) for p,hs in rules))
