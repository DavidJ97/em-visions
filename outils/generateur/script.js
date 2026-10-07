(function(){
const D=document,H=D.documentElement,$=(s,r)=>(r||D).querySelector(s),$$=(s,r)=>[...(r||D).querySelectorAll(s)];
const T=%TR%,RL=%RL%,WEEK=%WEEK%,PD=%PD%;
const RM=matchMedia('(prefers-reduced-motion:reduce)').matches,NC=navigator.connection,LITE=!!(NC&&(NC.saveData||/2g|3g/.test(NC.effectiveType||'')));
const hx=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const AR='<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h16M13 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
const toastEl=$('#toast');let tt;function toast(m){toastEl.textContent=m;toastEl.classList.add('on');clearTimeout(tt);tt=setTimeout(()=>toastEl.classList.remove('on'),2800)}

// thème clair ou sombre (clair par défaut)
function setTheme(t,save){H.dataset.theme=t;$$('.tog').forEach(b=>{b.setAttribute('aria-pressed',t==='dark');b.setAttribute('aria-label',t==='dark'?T.light:T.dark)});
 const m=$('meta[name=theme-color]');if(m)m.content=t==='dark'?'#0a0a0a':'#f6f6f3';if(save){try{localStorage.setItem('em-theme',t)}catch(e){}}}
setTheme(H.dataset.theme==='dark'?'dark':'light');$$('.tog').forEach(b=>b.onclick=()=>setTheme(H.dataset.theme==='dark'?'light':'dark',true));

// menu du cellulaire
const menu=$('#menu'),bg=$('.burger'),gal=$('#gal');
function lock(){H.classList.toggle('dlg',!menu.hidden||!gal.hidden)}
function setMenu(o,quiet){menu.hidden=!o;bg.setAttribute('aria-expanded',o);lock();if(quiet)return;(o?$('.menu-x'):bg).focus()}
bg.onclick=()=>setMenu(true);$('.menu-x').onclick=()=>setMenu(false);
menu.addEventListener('click',e=>{if(e.target.closest('a[href^="#"]'))setMenu(false,true)});

// la section à l'écran est soulignée dans le menu ; le lien FR | EN garde la même section
const secs=$$('main section[id]');
function current(id,alt){$$('.nav a,.menu nav a').forEach(a=>{a.getAttribute('href')==='#'+id?a.setAttribute('aria-current','page'):a.removeAttribute('aria-current')});
 $$('a[data-other]').forEach(a=>a.setAttribute('href',a.dataset.other+'#'+alt))}
if('IntersectionObserver' in window){const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)current(e.target.id,e.target.dataset.alt)}),{rootMargin:'-42% 0px -54% 0px'});secs.forEach(s=>io.observe(s))}

// vidéo de l'accueil : jouée seulement si l'appareil et la connexion s'y prêtent, avec un bouton pause
const hv=$('.hero-m video'),pp=$('.hero-m .pp');
if(hv&&!RM&&!LITE){hv.src=hv.dataset.src;hv.play().catch(()=>{});pp.hidden=false;
 pp.onclick=()=>{const p=!hv.paused;p?hv.pause():hv.play().catch(()=>{});pp.setAttribute('aria-pressed',p);pp.setAttribute('aria-label',p?T.play:T.pause)}}

// heures : la case d'aujourd'hui (heure de Montréal)
try{const DN=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(new Date().toLocaleDateString('en-US',{weekday:'short',timeZone:'America/Toronto'}));
 $$('.hgrid li[data-d="'+DN+'"]').forEach(e=>e.classList.add('now'));const w=WEEK[DN],td=$('#today');if(td)td.textContent=w?T.today+w[0]+T.to+w[1]:T.todayClosed}catch(e){}

// réalisations : le reste de la liste
const more=$('#more');if(more)more.onclick=()=>{const hid=$$('.works li[hidden]');hid.forEach(li=>li.hidden=false);more.remove();if(hid[0])hid[0].querySelector('button').focus()};

// catalogue : la catégorie choisie montre ses produits ; le produit choisi remplit le grand panneau
const catB=$$('.cat-nav button[data-cat]'),prodB=$$('.prods button');
function pick(id,scroll){const p=PD[id];if(!p)return;prodB.forEach(b=>b.setAttribute('aria-pressed',b.dataset.p===id));
 $('#pan-img').src=T.img+id+'.webp';$('#pan-img').alt=p.n;$('#pan-cat').textContent=p.c;$('#pan-name').textContent=p.n;$('#pan-col').textContent=p.col;$('#pan-side').textContent=p.side;
 $('#pan-try').href=T.tool+'?p='+id;$('#pan-sw').innerHTML=p.sw.map(c=>'<li><i style="background:'+c[1]+'"></i>'+hx(c[0])+'</li>').join('');
 if(scroll){const r=$('#pan').getBoundingClientRect();if(r.top<70||r.top>innerHeight*.45)scrollTo({top:r.top+scrollY-96,behavior:RM?'auto':'smooth'})}}
function setCat(c,keep){catB.forEach(b=>b.setAttribute('aria-pressed',b.dataset.cat===c));let first=null;
 $$('.prods li').forEach(li=>{const on=c==='all'||li.dataset.cat===c;li.hidden=!on;if(on&&!first)first=li.querySelector('button').dataset.p});if(!keep&&first)pick(first)}
catB.forEach(b=>b.onclick=()=>setCat(b.dataset.cat));prodB.forEach(b=>b.onclick=()=>pick(b.dataset.p,true));
const allp=$('#allp');if(allp)allp.onclick=()=>{setCat('all',true);allp.hidden=true};
if(prodB[0])pick(prodB[0].dataset.p);

// fiche d'un projet
let gi=-1,gp=0,galF=null,media=[];
function show(j){gp=(j+media.length)%media.length;const m=media[gp],box=$('.gal-m .mm',gal);
 box.innerHTML=m.v?'<video src="'+m.v+'" poster="'+m.b+'" controls muted loop playsinline'+(RM?'':' autoplay')+'></video>':'<img src="'+m.b+'" alt="'+hx(m.a)+'">';
 $$('.gal-t button',gal).forEach((b,k)=>b.setAttribute('aria-current',k===gp))}
function project(i){gi=(i+RL.length)%RL.length;const p=RL[gi];media=(p.v&&!LITE?[{v:p.v,b:p.m,s:p.t,a:p.a}]:[]).concat(p.ph);const n=media.length;
 gal.setAttribute('aria-label',p.n);
 $('.gal-b',gal).innerHTML='<figure class="gal-m"><div class="mm"></div>'+(n>1?'<button type="button" class="pv" data-g="pp" aria-label="'+hx(T.prevPhoto)+'">'+AR+'</button><button type="button" class="nx" data-g="pn" aria-label="'+hx(T.nextPhoto)+'">'+AR+'</button>':'')+'</figure>'
  +'<div class="gal-i"><small>'+String(gi+1).padStart(2,'0')+' / '+RL.length+'</small><h2>'+hx(p.n)+'</h2><p>'+hx(p.k)+'</p>'
  +(n>1?'<div class="gal-t">'+media.map((f,k)=>'<button type="button" data-g="t'+k+'"'+(f.v?' class="vd"':'')+' aria-label="'+hx((f.v?T.video:T.photo)+(k+1))+'"><img src="'+f.s+'" alt="" loading="lazy"></button>').join('')+'</div>':'')
  +'<a class="btn" href="#contact" data-g="quote">'+hx(T.similarBtn)+AR+'</a>'
  +'<div class="gal-n"><button type="button" data-g="prev">'+AR+hx(T.prevProject)+'</button><button type="button" data-g="next">'+hx(T.nextProject)+AR+'</button></div></div>';
 show(0);gal.scrollTop=0}
function openGal(i){if(gal.hidden){galF=D.activeElement;gal.hidden=false;lock()}project(i);$('.gal-x',gal).focus({preventScroll:true})}
function closeGal(){gal.hidden=true;$('.gal-b',gal).innerHTML='';lock();galF&&galF.focus&&galF.focus({preventScroll:true})}
$$('.works button').forEach(b=>b.onclick=()=>openGal(+b.dataset.i));
gal.addEventListener('click',e=>{const t=e.target.closest('[data-g]');if(!t)return;const g=t.dataset.g;
 if(g==='close')closeGal();else if(g==='prev')project(gi-1);else if(g==='next')project(gi+1);else if(g==='pp')show(gp-1);else if(g==='pn')show(gp+1);else if(g[0]==='t')show(+g.slice(1));
 else if(g==='quote'){prefill(T.similar+RL[gi].n+'\n');closeGal()}});
addEventListener('keydown',e=>{if(e.key==='Escape'&&!menu.hidden){setMenu(false);return}if(gal.hidden)return;
 if(e.key==='Escape'){e.preventDefault();closeGal()}
 else if((e.key==='ArrowRight'||e.key==='ArrowLeft')&&!e.target.closest('video')){const d=e.key==='ArrowRight'?1:-1;gp+d<0||gp+d>=media.length?project(gi+d):show(gp+d)}
 else if(e.key==='Tab'){const f=$$('button,a[href],video',gal).filter(x=>x.offsetParent);if(!f.length)return;const a=f[0],z=f[f.length-1];if(e.shiftKey&&D.activeElement===a){e.preventDefault();z.focus()}else if(!e.shiftKey&&D.activeElement===z){e.preventDefault();a.focus()}}});

// formulaire de devis
const form=$('#devis'),ok=$('#ok'),ko=$('#ko');
const F=n=>form.querySelector('[name="'+n+'"]'),ERR=n=>form.querySelector('[data-err="'+n+'"]');
function prefill(s){const pj=F('projet');if(!pj.value.trim()){pj.value=s;pj.dispatchEvent(new Event('input',{bubbles:true}))}
 setTimeout(()=>{pj.focus({preventScroll:true});try{pj.setSelectionRange(pj.value.length,pj.value.length)}catch(_){}},700)}
D.addEventListener('click',e=>{if(e.target.closest('[data-prix]')){const n=$('#pan-name');prefill(T.priceReq+(n&&e.target.closest('.pan')?n.textContent:''))}const sv=e.target.closest('[data-svc]');if(sv)prefill(T.service+sv.dataset.svc+'\n')});
const steps=$$('.steps li');function step(k){steps.forEach((li,i)=>li.classList.toggle('on',i===k))}
form.addEventListener('focusin',e=>{const n=e.target.name;if(n)step(['qte','echeance','fichier'].includes(n)?1:0)});
const SENT=new URLSearchParams(location.search).has('envoye');if(SENT)history.replaceState(null,'',location.pathname+location.hash);
addEventListener('pageshow',e=>{if(e.persisted)$('[type=submit]',form).disabled=false});
const MSG={nom:T.eName,courriel:T.eMail,projet:T.eProj},N=['nom','courriel','projet'];
function chk(n,showIt){const el=F(n),v=el.value.trim();let bad=false;
 if(n==='nom')bad=!v;if(n==='courriel')bad=!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);if(n==='projet')bad=!v;
 if(showIt){el.closest('.f').classList.toggle('bad',bad);ERR(n).textContent=bad?MSG[n]:'';el.setAttribute('aria-invalid',bad)}return !bad}
N.forEach(n=>{const el=F(n);el.addEventListener('blur',()=>{if(el.value)chk(n,true)});el.addEventListener('input',()=>{if(el.closest('.f').classList.contains('bad'))chk(n,true)})});
const fl=F('fichier'),fname=$('[data-fl]',form),fhint=$('[data-fh]',form),ft=[fname.textContent,fhint.textContent];
function chkFile(){const e=ERR('fichier'),f=fl.files[0];e.textContent='';if(!f){fname.textContent=ft[0];fhint.textContent=ft[1];return true}
 if(!/\.(jpe?g|png|pdf)$/i.test(f.name)){fl.value='';chkFile();e.textContent=T.eFmt;return false}
 if(f.size>10000000){fl.value='';chkFile();e.textContent=T.eSize;return false}
 fname.textContent=f.name.length>40?f.name.slice(0,37)+'…':f.name;fhint.textContent=(f.size/1e6).toFixed(1).replace('.',T.dec)+T.mbChange;return true}
fl.addEventListener('change',chkFile);
const reveal=el=>{el.hidden=false;el.focus({preventScroll:true});$('.fcard').scrollIntoView({block:'start'})};
form.addEventListener('submit',async e=>{e.preventDefault();const r=N.map(n=>chk(n,true));if(r.includes(false)){F(N[r.indexOf(false)]).focus();return}
 const btn=$('[type=submit]',form);btn.disabled=true;toast(T.sending);
 if(form.dataset.send){F('_next').value=location.origin+location.pathname+'?envoye=1#contact';F('_replyto').value=F('courriel').value.trim();form.submit();return}
 let sent=false;try{const ac=new AbortController(),to=setTimeout(()=>ac.abort(),20000);const res=await fetch('/api/demandes',{method:'POST',body:new FormData(form),signal:ac.signal});clearTimeout(to);if(!res.ok)throw 0;sent=true;
  let ref='';try{ref=(await res.json()).reference||''}catch(_){}$('.ref',ok).textContent=ref?T.ref+ref:''}catch(_){}
 btn.disabled=false;form.hidden=true;toastEl.classList.remove('on');
 if(sent){step(2);reveal(ok)}else{const v=n=>F(n).value.trim();
  const body=[T.name+' : '+v('nom'),T.mail+' : '+v('courriel'),T.qty+' : '+(v('qte')||'—'),T.due+' : '+(v('echeance')||'—'),'',v('projet')].join('\n');
  const bm=$('.bymail',ko);if(bm&&bm.dataset.mail)bm.href='mailto:'+bm.dataset.mail+'?subject='+encodeURIComponent(T.subject+' — '+v('nom'))+'&body='+encodeURIComponent(body);reveal(ko)}});
if(SENT){form.hidden=true;ok.hidden=false;step(2)}
$('.again',ok).onclick=()=>{form.reset();chkFile();form.hidden=false;ok.hidden=true;step(0);F('nom').focus()};
$('.retry',ko).onclick=()=>{form.hidden=false;ko.hidden=true;$('[type=submit]',form).focus()};

// maquette 3D envoyée depuis le modélisateur : elle est jointe à la demande
(async()=>{try{if(!('indexedDB' in window))return;const db=await new Promise((res,rej)=>{const r=indexedDB.open('em-visions',1);r.onupgradeneeded=()=>r.result.createObjectStore('kv');r.onsuccess=()=>res(r.result);r.onerror=()=>rej()});
 const rec=await new Promise(res=>{const q=db.transaction('kv').objectStore('kv').get('maquette');q.onsuccess=()=>res(q.result);q.onerror=()=>res(null)});if(!rec||Date.now()-rec.at>36e5)return;
 const dt=new DataTransfer();dt.items.add(new File([rec.snap],rec.snapName,{type:'image/jpeg'}));fl.files=dt.files;fl.dispatchEvent(new Event('change',{bubbles:true}));
 (rec.orig||[]).slice(0,2).forEach((o,i)=>{const nm='visuel_original'+(i?'_2':'');let h=F(nm);if(!h){h=D.createElement('input');h.type='file';h.name=nm;h.hidden=true;form.appendChild(h)}const d2=new DataTransfer();d2.items.add(new File([o.blob],o.name,{type:o.type}));h.files=d2.files});
 const pj=F('projet');if(!pj.value.includes(rec.summary))pj.value=(pj.value?pj.value+'\n':'')+rec.summary+'\n';
 db.transaction('kv','readwrite').objectStore('kv').delete('maquette');toast(T.mockAdded)}catch(_){}})();
})();
