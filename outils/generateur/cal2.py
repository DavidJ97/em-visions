import json, os, re, subprocess, sys, numpy as np, cv2
from playwright.sync_api import sync_playwright
from lib import classmask, clean
EL=json.load(open('elements.json'))
ONLY=[x for x in os.environ.get('ONLY','').split(',') if x]
PAGESEL=[x for x in os.environ.get('PAGES','').split(',') if x]
IT=int(os.environ.get('IT','5'))
C=json.load(open('cal2.json')) if os.path.exists('cal2.json') else {}
els=[e for e in EL if (not ONLY or e['id'] in ONLY or str(e['group']) in ONLY) and (not PAGESEL or e['page'] in PAGESEL)]
BG={'w':'#000','b':'#000','wt':'#0a3cff','k':'#ececec','k2':'#ececec','g':'#ececec'}
def spec_mode(e):
    V=json.load(open('var2.json')) if os.path.exists('var2.json') else {}
    s=dict(e['spec']); s.update(V.get(e['id'],{})); s.update(V.get('group:'+e['page']+':'+str(e['group']),{})); return s.get('mode','ls')
def measure(pg,e):
    pg.evaluate("""([id,bg,page])=>{if(location.hash!=='#'+page){location.hash=page}document.querySelectorAll('.t.show').forEach(x=>x.classList.remove('show'));
      document.getElementById(id).classList.add('show');document.documentElement.style.setProperty('--calbg',bg)}""",[e['id'],BG[e['cls']],e['page']])
    pg.wait_for_timeout(30)
    buf=pg.screenshot(); im=cv2.imdecode(np.frombuffer(buf,np.uint8),1)
    hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV); Hh,S,Vv=[hsv[...,i].astype(int) for i in range(3)]
    m={'w':Vv>70,'b':Vv>70,'wt':(S<120)&(Vv>150),'k':Vv<180,'k2':Vv<200,'g':Vv<225}[e['cls']]
    m=clean(m,3)
    ys,xs=np.nonzero(m)
    if len(xs)==0: return None
    return xs.min(),ys.min(),xs.max()+1,ys.max()+1
def cur(e):
    h=open('out/cal.html').read()
    m=re.search(rf'id="{re.escape(e["id"])}"[^>]*? data-cls="\w+" style="--x:([\d.-]+);--y:([\d.-]+);--fs:([\d.-]+);--sx:([\d.-]+);--ls:([\d.-]+)',h)
    return list(map(float,m.groups()))
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1586,'height':992})
    for it in range(IT):
        subprocess.run(['python3','build2.py','cal'],check=True,capture_output=True)
        pg.goto('file:///home/claude/work/v2/out/cal.html'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
        err=[]
        for e in els:
            x,y,fs,sx,ls=cur(e); X0,Y0,X1,Y1=e['box']; tw,th=X1-X0,Y1-Y0
            r=measure(pg,e)
            if r is None: print('none',e['id']); continue
            bx0,by0,bx1,by1=r; iw,ih=bx1-bx0,by1-by0
            if os.environ.get('DBG'): print(e['id'],(x,y,fs,sx,ls),r,e['box'])
            err.append((max(abs(bx0-X0),abs(by0-Y0),abs(bx1-X1),abs(by1-Y1)),e['id']))
            c=C.setdefault(e['id'],{}); mode=spec_mode(e); n=max(len(e['text'])-1,1)
            if it<2:
                k=th/max(ih,1); fs2=fs*k
                if mode=='sx': c['sx']=sx*tw/max(iw*k,1)
                else: c['ls']=ls*k+(tw-iw*k)/n
                c['fs']=fs2; c['x']=x+(X0-bx0); c['y']=y+(Y0-by0)
            else:
                c['x']=x+(X0-bx0); c['y']=y+(Y0-by0)
                if mode=='sx': c['sx']=sx*tw/max(iw,1)
                else: c['ls']=ls+(tw-iw)/n
            if 'ls' in c: c['ls']=float(np.clip(c['ls'],-0.12*c['fs'],0.45*c['fs']))
            if 'sx' in c: c['sx']=float(np.clip(c['sx'],0.55,1.7))
        json.dump(C,open('cal2.json','w'),indent=0)
        err.sort(reverse=True); print('it',it,'maxerr',err[:6],flush=True)
    b.close()
