(function(){
const D=document,H=D.documentElement,$=(s,r)=>(r||D).querySelector(s),$$=(s,r)=>[...(r||D).querySelectorAll(s)];
const T=%TR%,RL=%RL%;
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

// accueil : les vidéos ne jouent que si l'appareil et la connexion s'y prêtent ; un bouton met tout en pause
const hero=$('.hero'),figs=$$('.strip figure'),pp=$('.pp');let stopped=false,redraw=()=>{};
const shown=()=>figs.filter(f=>f.offsetParent);
function feed(){if(RM||LITE)return;shown().forEach(f=>{const v=$('video',f);if(!v.src)v.src=v.dataset.src;if(!stopped)v.play().catch(()=>{})});pp.hidden=false}
feed();
pp.onclick=()=>{stopped=!stopped;figs.forEach(f=>{const v=$('video',f);if(v.src)stopped?v.pause():v.play().catch(()=>{})});
 pp.setAttribute('aria-pressed',stopped);pp.setAttribute('aria-label',stopped?T.play:T.pause);redraw()};

// logo de verre : l'image de l'accueil est redessinée dans un canvas, déformée à travers la forme du logo qui pivote lentement.
// Sans WebGL, le logo blanc posé sur l'image reste en place.
(function(){
 const cv=$('.gl');let gl;try{gl=cv.getContext('webgl',{alpha:false,antialias:false,powerPreference:'low-power'})}catch(e){}
 if(!gl)return;
 const VS='attribute vec2 p;varying vec2 v;void main(){v=vec2(p.x*.5+.5,.5-p.y*.5);gl_Position=vec4(p,0.,1.);}';
 const FS=`#ifdef GL_FRAGMENT_PRECISION_HIGH
precision highp float;
#else
precision mediump float;
#endif
varying vec2 v;uniform sampler2D uM,uT0,uT1,uT2;uniform vec2 uR,uC,uS0,uS1,uS2;uniform float uN,uL,uA,uB;
vec3 pic(vec2 u){u=clamp(u,0.,.9999);float f=u.x*uN,i=floor(f);vec2 z=i<.5?uS0:i<1.5?uS1:uS2;
 float rs=uR.x/uN/uR.y,rm=z.x/z.y;vec2 s=rs>rm?vec2(1.,rm/rs):vec2(rs/rm,1.);vec2 t=(vec2(f-i,u.y)-.5)*s+.5;
 return i<.5?texture2D(uT0,t).rgb:i<1.5?texture2D(uT1,t).rgb:texture2D(uT2,t).rgb;}
void main(){
 vec2 px=(v-uC)*uR/uL;float ca=cos(uA),sa=sin(uA),cb=cos(uB),sb=sin(uB);
 vec3 X=vec3(ca,0.,-sa),Y=vec3(sa*sb,cb,ca*sb),Z=vec3(sa*cb,-sb,ca*cb),o=vec3(0.,0.,2.6),d=normalize(vec3(px,0.)-o);
 vec3 h=o-d*dot(o,Z)/dot(d,Z);vec2 mu=vec2(dot(h,X),dot(h,Y)*2.)+.5;
 vec3 m=vec3(0.);vec2 g=vec2(0.);
 if(mu.x>0.&&mu.x<1.&&mu.y>0.&&mu.y<1.){m=texture2D(uM,mu).rgb;float e=1.6/1024.;
  g=vec2(texture2D(uM,mu+vec2(e,0.)).g-texture2D(uM,mu-vec2(e,0.)).g,texture2D(uM,mu+vec2(0.,e*2.)).g-texture2D(uM,mu-vec2(0.,e*2.)).g);}
 vec3 n=normalize(X*(-g.x*2.6)+Y*(-g.y*2.6)+Z);
 vec2 off=(n.xy*.085-px*.16*m.g-vec2(0.,.012))*uL/uR;
 vec3 base=pic(v)*(1.-.42*m.b*(1.-m.r));
 vec3 c=vec3(pic(v+off*.92).r,pic(v+off).g,pic(v+off*1.08).b);
 float rim=clamp(length(g)*1.9,0.,1.),sp=pow(max(dot(n,normalize(vec3(-.45,-.62,.64))),0.),26.);
 c=c*1.14+.1+rim*.3+sp*.8*rim+vec3(.02,.04,.09)*m.g;
 gl_FragColor=vec4(mix(base,c,m.r),1.);}`;
 const sh=(t,s)=>{const o=gl.createShader(t);gl.shaderSource(o,s);gl.compileShader(o);return gl.getShaderParameter(o,gl.COMPILE_STATUS)?o:null};
 const a=sh(gl.VERTEX_SHADER,VS),b=sh(gl.FRAGMENT_SHADER,FS);if(!a||!b)return;
 const pr=gl.createProgram();gl.attachShader(pr,a);gl.attachShader(pr,b);gl.linkProgram(pr);if(!gl.getProgramParameter(pr,gl.LINK_STATUS))return;gl.useProgram(pr);
 gl.bindBuffer(gl.ARRAY_BUFFER,gl.createBuffer());gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),gl.STATIC_DRAW);
 const pl=gl.getAttribLocation(pr,'p');gl.enableVertexAttribArray(pl);gl.vertexAttribPointer(pl,2,gl.FLOAT,false,0,0);
 const U=n=>gl.getUniformLocation(pr,n),G=gl.TEXTURE_2D;
 function tex(u){gl.activeTexture(gl.TEXTURE0+u);gl.bindTexture(G,gl.createTexture());gl.texParameteri(G,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);gl.texParameteri(G,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
  gl.texParameteri(G,gl.TEXTURE_MIN_FILTER,gl.LINEAR);gl.texParameteri(G,gl.TEXTURE_MAG_FILTER,gl.LINEAR);gl.texImage2D(G,0,gl.RGBA,1,1,0,gl.RGBA,gl.UNSIGNED_BYTE,new Uint8Array([0,0,0,255]))}
 for(let i=0;i<4;i++)tex(i);gl.uniform1i(U('uM'),3);[0,1,2].forEach(i=>gl.uniform1i(U('uT'+i),i));
 const uS=[0,1,2].map(i=>U('uS'+i)),uR=U('uR'),uC=U('uC'),uN=U('uN'),uL=U('uL'),uA=U('uA'),uB=U('uB'),cur=[null,null,null];
 let W=0,Hh=0,maskOk=false,lost=false,time=0,last=0,raf=0,inView=true,mx=0,my=0,tx=0,ty=0;
 const mk=new Image();mk.onload=()=>{gl.activeTexture(gl.TEXTURE3);gl.texImage2D(G,0,gl.RGB,gl.RGB,gl.UNSIGNED_BYTE,mk);gl.generateMipmap(G);gl.texParameteri(G,gl.TEXTURE_MIN_FILTER,gl.LINEAR_MIPMAP_LINEAR);maskOk=true;redraw()};mk.src=cv.dataset.m;
 function size(){const w=hero.clientWidth,h=hero.clientHeight,r=Math.min(devicePixelRatio||1,2,Math.sqrt(2.4e6/(w*h)));W=Math.round(w*r);Hh=Math.round(h*r);
  if(cv.width!==W||cv.height!==Hh){cv.width=W;cv.height=Hh;gl.viewport(0,0,W,Hh)}
  const tall=w<h*.8;gl.uniform2f(uR,W,Hh);gl.uniform2f(uC,.5,tall?.31:.44);gl.uniform1f(uL,tall?W*1.05:Math.min(W*.9,Hh*1.08,1020*r))}
 function draw(){if(lost||!maskOk)return;const fs=shown().slice(0,3);if(!fs.length)return;let ok=true;
  fs.forEach((f,i)=>{const vd=$('video',f),im=$('img',f),s=vd.readyState>=2&&vd.videoWidth?vd:im.complete&&im.naturalWidth?im:null;if(!s){if(!cur[i])ok=false;return}
   if(s!==cur[i]||(s===vd&&!vd.paused)){gl.activeTexture(gl.TEXTURE0+i);try{gl.texImage2D(G,0,gl.RGB,gl.RGB,gl.UNSIGNED_BYTE,s)}catch(e){return}cur[i]=s;gl.uniform2f(uS[i],s.videoWidth||s.naturalWidth,s.videoHeight||s.naturalHeight)}});
  if(!ok)return;
  mx+=(tx-mx)*.06;my+=(ty-my)*.06;gl.uniform1f(uN,fs.length);
  gl.uniform1f(uA,RM?.3:.46*Math.sin(time*.5)+mx*.5);gl.uniform1f(uB,RM?.08:.17*Math.sin(time*.33+1.3)-my*.3);
  gl.drawArrays(gl.TRIANGLES,0,3);hero.classList.add('on')}
 function loop(t){raf=0;if(last)time+=Math.min(.05,(t-last)/1000);last=t;draw();play()}
 function play(){if(!raf&&!RM&&!stopped&&inView&&!D.hidden)raf=requestAnimationFrame(loop);else if(!raf)last=0}
 redraw=()=>{size();feed();draw();last=0;play()};
 figs.forEach(f=>{$('img',f).addEventListener('load',redraw);$('video',f).addEventListener('loadeddata',redraw)});
 addEventListener('resize',redraw);D.addEventListener('visibilitychange',redraw);
 if('IntersectionObserver' in window)new IntersectionObserver(es=>{inView=es[0].isIntersecting;last=0;play()}).observe(hero);
 if(matchMedia('(hover:hover)').matches)hero.addEventListener('pointermove',e=>{tx=e.clientX/innerWidth-.5;ty=e.clientY/innerHeight-.5});
 cv.addEventListener('webglcontextlost',e=>{e.preventDefault();lost=true;hero.classList.remove('on')});
 redraw();
})();

// heures : la ligne d'aujourd'hui (heure de Montréal)
try{const DN=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(new Date().toLocaleDateString('en-US',{weekday:'short',timeZone:'America/Toronto'}));$$('.hours li[data-d="'+DN+'"]').forEach(e=>e.classList.add('now'))}catch(e){}

// réalisations : le reste de la liste
const more=$('#more');if(more)more.onclick=()=>{const hid=$$('.works li[hidden]');hid.forEach(li=>li.hidden=false);more.remove();if(hid[0])hid[0].querySelector('button').focus()};

// catalogue : filtre par catégorie
const catB=$$('.filt button');catB.forEach(b=>b.onclick=()=>{const c=b.dataset.cat;catB.forEach(x=>x.setAttribute('aria-pressed',x===b));$$('.prods li').forEach(li=>li.hidden=c!=='all'&&li.dataset.cat!==c)});

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
  +'<a class="btn" href="#contact" data-g="quote">'+hx(T.similarBtn)+'</a>'
  +'<div class="gal-n"><button type="button" class="cap" data-g="prev">← '+hx(T.prevProject)+'</button><button type="button" class="cap" data-g="next">'+hx(T.nextProject)+' →</button></div></div>';
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
D.addEventListener('click',e=>{if(e.target.closest('[data-prix]'))prefill(T.priceReq)});
const step=()=>{};

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
