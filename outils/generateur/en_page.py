"""Version anglaise statique : traduit le texte et les attributs de la page française
(même règles que le script de la page) et garde l'original dans data-fr / data-fra
pour que la mise en page anglaise soit recalculée au chargement."""
import json, asyncio
from playwright.async_api import async_playwright
JS=r"""([html,EN,SLUG])=>{const doc=new DOMParser().parseFromString(html,'text/html');
 const w=doc.createTreeWalker(doc.body,NodeFilter.SHOW_TEXT);let n;const todo=[];
 while(n=w.nextNode()){const v=n.nodeValue,t=v.trim();if(!t||n.parentNode.closest('script,style'))continue;
  const pg=(n.parentNode.closest('.page,.mpage')||{id:''}).id.replace(/^[pm]-/,'');const en=EN[pg+':'+t]??EN[t];if(en===undefined)continue;todo.push([n,v,t,en])}
 todo.forEach(([n,v,t,en])=>{const p=n.parentNode,i=[...p.childNodes].indexOf(n);const m=p.dataset.fr?JSON.parse(p.dataset.fr):{};m[i]=t;p.dataset.fr=JSON.stringify(m);
  n.nodeValue=v.slice(0,v.indexOf(t))+en+v.slice(v.indexOf(t)+t.length)});
 doc.querySelectorAll('[aria-label],[placeholder],[alt]').forEach(el=>{const m={};['aria-label','placeholder','alt'].forEach(a=>{const v=el.getAttribute(a);if(v&&EN[v]!==undefined){m[a]=v;el.setAttribute(a,EN[v])}});
  if(Object.keys(m).length)el.dataset.fra=JSON.stringify(m)});
 doc.querySelectorAll('a[href^="#"]').forEach(a=>{const k=a.getAttribute('href').slice(1);if(SLUG[k])a.setAttribute('href','#'+SLUG[k])});
 doc.querySelectorAll('a[data-m3d]').forEach(a=>a.setAttribute('href','mockup/'));
 doc.querySelectorAll('a[data-privacy]').forEach(a=>a.setAttribute('href','privacy/'));
 doc.querySelectorAll('.lang-fr,.mlang-fr').forEach(a=>a.setAttribute('href','../#accueil'));doc.querySelectorAll('.lang-en,.mlang-en').forEach(a=>a.setAttribute('href','#home'));
 return '<!doctype html>'+doc.documentElement.outerHTML}"""
async def _run(html,EN,SLUG):
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(java_script_enabled=True)
        out=await pg.evaluate(JS,[html,EN,SLUG]); await b.close(); return out
def translate(html,EN,SLUG): return asyncio.run(_run(html,EN,SLUG))
