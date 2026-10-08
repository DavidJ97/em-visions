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

// accueil à la Palace : la scène reste en place pendant qu'on fait défiler ; les vidéos se relaient derrière le logo de verre,
// qui fait un tour par vidéo et suit le doigt ou la souris. Les vidéos ne jouent que si l'appareil et la connexion s'y prêtent ;
// le bouton pause arrête les vidéos et le mouvement automatique.
const hero=$('.hero'),stage=$('.stage'),figs=$$('.strip figure'),pp=$('.pp'),kNum=$('.hero-k span'),kName=$('.hero-k b'),NS=figs.length;
let stopped=false,inView=true,scene=0,next=0,mixK=0,turn=0,redraw=()=>{};
const vid=j=>$('video',figs[j]),pad=j=>String(j+1).padStart(2,'0'),ease=x=>{x=Math.min(1,Math.max(0,x));return x*x*(3-2*x)};
function scenes(){const r=hero.getBoundingClientRect(),run=r.height-innerHeight,p=run>0?Math.min(1,Math.max(0,-r.top/run)):0,s=p*(NS-1),i=Math.min(NS-1,Math.floor(s)),f=s-i;
 scene=i;next=Math.min(NS-1,i+1);mixK=next>i?ease((f-.42)/.3):0;turn=i+ease((f-.12)/.8);
 const k=mixK>.5?next:scene;if(kNum.textContent!==pad(k)){kNum.textContent=pad(k);kName.textContent=figs[k].dataset.n;figs.forEach((g,j)=>g.classList.toggle('cur',j===k))}
 videos()}
function videos(){if(RM||LITE)return;pp.hidden=false;figs.forEach((g,j)=>{const v=vid(j),want=inView&&(j===scene||j===next);
 if(want&&!v.src)v.src=v.dataset.src;if(want&&!stopped){if(v.paused)v.play().catch(()=>{})}else if(v.src&&!v.paused)v.pause()})}
scenes();addEventListener('scroll',scenes,{passive:true});
if('IntersectionObserver' in window)new IntersectionObserver(es=>{inView=es[0].isIntersecting;videos();redraw()}).observe(hero);
pp.onclick=()=>{stopped=!stopped;videos();pp.setAttribute('aria-pressed',stopped);pp.setAttribute('aria-label',stopped?T.play:T.pause);redraw()};

// le logo de verre : l'image de fond est redessinée dans un canvas et déformée à travers un logo épais, en vrai 3D.
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
varying vec2 v;uniform sampler2D uM,uT0,uT1;uniform vec2 uR,uC,uS0,uS1;uniform float uL,uA,uB,uK;
const float TH=.055;
vec2 cov(vec2 u,vec2 z){float rs=uR.x/uR.y,rm=z.x/z.y;vec2 s=rs>rm?vec2(1.,rm/rs):vec2(rs/rm,1.);return (u-.5)*s+.5;}
vec3 pic(vec2 u){u=clamp(u,.001,.999);vec3 a=texture2D(uT0,cov(u,uS0)).rgb;return uK>0.?mix(a,texture2D(uT1,cov(u,uS1)).rgb,uK):a;}
vec3 mk(vec2 q){vec2 u=vec2(q.x,q.y*2.)+.5;return (u.x<0.||u.x>1.||u.y<0.||u.y>1.)?vec3(0.):texture2D(uM,u).rgb;}
void main(){
 vec2 px=(v-uC)*uR/uL;float ca=cos(uA),sa=sin(uA),cb=cos(uB),sb=sin(uB);
 vec3 X=vec3(ca,0.,-sa),Y=vec3(sa*sb,cb,ca*sb),Z=vec3(sa*cb,-sb,ca*cb),o=vec3(0.,0.,2.6),d=normalize(vec3(px,0.)-o);
 vec3 ol=vec3(dot(o,X),dot(o,Y),dot(o,Z)),dl=vec3(dot(d,X),dot(d,Y),dot(d,Z));
 if(abs(dl.x)<1e-4)dl.x=1e-4;if(abs(dl.y)<1e-4)dl.y=1e-4;if(abs(dl.z)<1e-4)dl.z=1e-4;
 float sh=mk((ol-dl*ol.z/dl.z).xy).b;
 vec3 base=pic(v)*(1.-.4*sh);
 vec3 t0=(vec3(-.5,-.25,-TH*.5)-ol)/dl,t1=(vec3(.5,.25,TH*.5)-ol)/dl,tl=min(t0,t1),th=max(t0,t1);
 float tn=max(max(tl.x,tl.y),tl.z),tf=min(min(th.x,th.y),th.z);
 if(tn>=tf){gl_FragColor=vec4(base,1.);return;}
 vec3 hp=ol+dl*tl.z;float af=mk(hp.xy).r,as=0.;vec3 sp=hp;
 if(af<.5){for(int i=0;i<16;i++){vec3 p=ol+dl*mix(max(tn,tl.z),tf,(float(i)+.5)/16.);float m=mk(p.xy).r;if(m>as){as=m;sp=p;}if(m>.5)break;}}
 bool face=af>=as;if(!face)hp=sp;
 float e=1.6/1024.;vec3 mh=mk(hp.xy),nl;float rim;
 if(face){vec2 g=vec2(mk(hp.xy+vec2(e,0.)).g-mk(hp.xy-vec2(e,0.)).g,mk(hp.xy+vec2(0.,e)).g-mk(hp.xy-vec2(0.,e)).g);
  nl=normalize(vec3(-g*2.6,-sign(dl.z)));rim=clamp(length(g)*1.9,0.,1.);}
 else{vec2 g=vec2(mk(hp.xy+vec2(e*4.,0.)).b-mk(hp.xy-vec2(e*4.,0.)).b,mk(hp.xy+vec2(0.,e*4.)).b-mk(hp.xy-vec2(0.,e*4.)).b);
  nl=normalize(vec3(-g+vec2(1e-5),0.));rim=.75;}
 vec3 n=normalize(X*nl.x+Y*nl.y+Z*nl.z);
 vec2 off=(n.xy*(face?.085:.2)-px*.16*mh.g-vec2(0.,.012))*uL/uR;
 vec3 c=vec3(pic(v+off*.92).r,pic(v+off).g,pic(v+off*1.08).b);
 float spc=pow(max(dot(n,normalize(vec3(-.45,-.62,.64))),0.),26.);
 c=face?c*1.14+.1+rim*.3+spc*.8*rim+vec3(.02,.04,.09)*mh.g:c*.82+.16+spc*.9+vec3(.03,.05,.1);
 float a=face?af:smoothstep(.35,.65,as);
 gl_FragColor=vec4(mix(base,c,a),1.);}`;
 const sh=(t,s)=>{const o=gl.createShader(t);gl.shaderSource(o,s);gl.compileShader(o);return gl.getShaderParameter(o,gl.COMPILE_STATUS)?o:null};
 const a=sh(gl.VERTEX_SHADER,VS),b=sh(gl.FRAGMENT_SHADER,FS);if(!a||!b)return;
 const pr=gl.createProgram();gl.attachShader(pr,a);gl.attachShader(pr,b);gl.linkProgram(pr);if(!gl.getProgramParameter(pr,gl.LINK_STATUS))return;gl.useProgram(pr);
 gl.bindBuffer(gl.ARRAY_BUFFER,gl.createBuffer());gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),gl.STATIC_DRAW);
 const pl=gl.getAttribLocation(pr,'p');gl.enableVertexAttribArray(pl);gl.vertexAttribPointer(pl,2,gl.FLOAT,false,0,0);
 const U=n=>gl.getUniformLocation(pr,n),G=gl.TEXTURE_2D;
 function tex(u){gl.activeTexture(gl.TEXTURE0+u);gl.bindTexture(G,gl.createTexture());gl.texParameteri(G,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);gl.texParameteri(G,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
  gl.texParameteri(G,gl.TEXTURE_MIN_FILTER,gl.LINEAR);gl.texParameteri(G,gl.TEXTURE_MAG_FILTER,gl.LINEAR);gl.texImage2D(G,0,gl.RGBA,1,1,0,gl.RGBA,gl.UNSIGNED_BYTE,new Uint8Array([0,0,0,255]))}
 [0,1,3].forEach(tex);gl.uniform1i(U('uM'),3);gl.uniform1i(U('uT0'),0);gl.uniform1i(U('uT1'),1);
 const uS=[U('uS0'),U('uS1')],uR=U('uR'),uC=U('uC'),uL=U('uL'),uA=U('uA'),uB=U('uB'),uK=U('uK'),cur=[null,null];
 let W=0,Hh=0,tall=false,base=1,maskOk=false,lost=false,time=0,last=0,raf=0,mx=0,my=0,tx=0,ty=0,key='';
 const mk=new Image();mk.onload=()=>{gl.activeTexture(gl.TEXTURE3);gl.texImage2D(G,0,gl.RGB,gl.RGB,gl.UNSIGNED_BYTE,mk);gl.generateMipmap(G);gl.texParameteri(G,gl.TEXTURE_MIN_FILTER,gl.LINEAR_MIPMAP_LINEAR);maskOk=true;redraw()};mk.src=cv.dataset.m;
 function size(){const w=stage.clientWidth,h=stage.clientHeight,r=Math.min(devicePixelRatio||1,2,Math.sqrt(2.4e6/(w*h)));W=Math.round(w*r);Hh=Math.round(h*r);tall=w<h*.8;
  if(cv.width!==W||cv.height!==Hh){cv.width=W;cv.height=Hh;gl.viewport(0,0,W,Hh)}gl.uniform2f(uR,W,Hh);base=tall?W*1.05:Math.min(W*.9,Hh*1.08,1020*r);key=''}
 const media=j=>{const g=figs[j],v=$('video',g),im=$('img',g);return v.readyState>=2&&v.videoWidth?v:im.complete&&im.naturalWidth?im:null};
 function upload(u,j){const s=media(j);if(!s)return!!cur[u];const v=s.tagName==='VIDEO';
  if(s!==cur[u]||(v&&!s.paused)){gl.activeTexture(gl.TEXTURE0+u);try{gl.texImage2D(G,0,gl.RGB,gl.RGB,gl.UNSIGNED_BYTE,s)}catch(e){return!!cur[u]}cur[u]=s;gl.uniform2f(uS[u],s.videoWidth||s.naturalWidth,s.videoHeight||s.naturalHeight);return 2}return 1}
 function draw(){if(lost||!maskOk)return;
  const live=!RM,s0=upload(0,scene),s1=next!==scene?upload(1,next):1;if(!s0)return;
  mx+=(tx-mx)*.08;my+=(ty-my)*.08;
  const wob=live&&!stopped?.07*Math.sin(time*.8):0,A=live?turn*Math.PI*2+mx*.9:0,B=live?wob-my*.55+.04:.06;
  const k=[A.toFixed(4),B.toFixed(4),mixK.toFixed(3),mx.toFixed(3),my.toFixed(3),W,Hh].join();if(k===key&&s0!==2&&s1!==2)return;key=k;
  gl.uniform1f(uA,A);gl.uniform1f(uB,B);gl.uniform1f(uK,next!==scene?mixK:0);
  gl.uniform2f(uC,.5+(live?mx*.08:0),(tall?.31:.44)+(live?my*.06:0));gl.uniform1f(uL,base);
  gl.drawArrays(gl.TRIANGLES,0,3);hero.classList.add('on')}
 function loop(t){raf=0;if(last&&!stopped)time+=Math.min(.05,(t-last)/1000);last=t;draw();play()}
 function play(){if(!raf&&inView&&!D.hidden)raf=requestAnimationFrame(loop);else if(!raf)last=0}
 redraw=()=>{size();draw();play()};
 figs.forEach(f=>{$('img',f).addEventListener('load',redraw);$('video',f).addEventListener('loadeddata',redraw)});
 addEventListener('resize',redraw);D.addEventListener('visibilitychange',redraw);addEventListener('scroll',play,{passive:true});
 if(!RM){const at=(x,y)=>{tx=x/innerWidth-.5;ty=y/innerHeight-.5;play()},home=()=>{tx=ty=0;play()};
  stage.addEventListener('pointermove',e=>{if(e.pointerType==='mouse')at(e.clientX,e.clientY)});stage.addEventListener('pointerleave',home);
  stage.addEventListener('touchstart',e=>at(e.touches[0].clientX,e.touches[0].clientY),{passive:true});
  stage.addEventListener('touchmove',e=>at(e.touches[0].clientX,e.touches[0].clientY),{passive:true});stage.addEventListener('touchend',home)}
 cv.addEventListener('webglcontextlost',e=>{e.preventDefault();lost=true;hero.classList.remove('on')});
 redraw();
})();

// heures : la ligne d'aujourd'hui (heure de Montréal)
try{const DN=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(new Date().toLocaleDateString('en-US',{weekday:'short',timeZone:'America/Toronto'}));$$('.hours li[data-d="'+DN+'"]').forEach(e=>e.classList.add('now'))}catch(e){}

// réalisations : le reste de la liste
const more=$('#more');if(more)more.onclick=()=>{const hid=$$('.works li[hidden]');hid.forEach(li=>li.hidden=false);more.remove();if(hid[0])hid[0].querySelector('button').focus()};

// catalogue : filtre par catégorie
const catB=$$('.filt button');catB.forEach(b=>b.onclick=()=>{const c=b.dataset.cat;catB.forEach(x=>x.setAttribute('aria-pressed',x===b));$$('.prods li').forEach(li=>li.hidden=c!=='all'&&li.dataset.cat!==c);
 const n=$$('.prods li').filter(li=>!li.hidden).length,w=$('.count [data-one]');$('#pc').textContent=n;w.textContent=n===1?w.dataset.one:w.dataset.many});

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
