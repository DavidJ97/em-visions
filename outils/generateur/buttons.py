import numpy as np, cv2
from scipy import ndimage as ndi
from vec import trace
from lib import hsvsplit
PILLS={'accueil':(70,705,436,815),'services':(76,866,490,970),'realisations':(70,705,428,815),'a-propos':(1074,752,1496,868)}
ARROW_R='M{a} {cy}h{L}M{b} {t}l{h} {h}l-{h} {h}'
def arrow(cx,cy,s,col='#fff',sw=2.4):
    # right arrow centered at cx,cy with length s
    x0=cx-s/2;x1=cx+s/2;h=s*0.36
    return f'<path d="M{x0:.1f} {cy:.1f}H{x1:.1f}M{x1-h:.1f} {cy-h:.1f}L{x1:.1f} {cy:.1f}L{x1-h:.1f} {cy+h:.1f}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
def diag(cx,cy,s,col='#fff',sw=2.2):
    a=s/2
    return f'<path d="M{cx-a:.1f} {cy+a:.1f}L{cx+a:.1f} {cy-a:.1f}M{cx-a*0.35:.1f} {cy-a:.1f}H{cx+a:.1f}V{cy+a*0.35:.1f}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
def build(page,im,E,EL):
    h,w=im.shape[:2]; H,S,V=hsvsplit(im); out=[]
    def add_erase(m,d=3): E[:]=np.maximum(E,cv2.dilate(m.astype(np.uint8),np.ones((2*d+1,2*d+1),np.uint8)))
    # --- logo
    m=np.zeros((h,w),bool); m[10:120,70:335]=(V[10:120,70:335]>120)&(S[10:120,70:335]<90); add_erase(m,2)
    out.append(dict(kind='logo',box=[76,14,328,116]))
    # --- theme toggle ring + moon
    yy,xx=np.mgrid[:h,:w]; m=((xx-1466.5)**2+(yy-59.5)**2)<29**2; add_erase(m,1)
    out.append(dict(kind='toggle',box=[1437,30,1496,89]))
    # --- nav underline (blue under active)
    m=np.zeros((h,w),bool); m[70:86,490:1160]=((H>100)&(H<135)&(S>110))[70:86,490:1160]; add_erase(m,2)
    # --- pills
    if page in PILLS:
        x0,y0,x1,y1=PILLS[page]; sub=((V>135)&(S<80))[y0:y1,x0:x1]
        g=cv2.cvtColor(im[y0:y1,x0:x1],cv2.COLOR_BGR2GRAY)
        c=cv2.HoughCircles(cv2.GaussianBlur(g,(5,5),1),cv2.HOUGH_GRADIENT,1,80,param1=80,param2=18,minRadius=28,maxRadius=48)
        cx,cy,r=c[0][0]; cx+=x0; cy+=y0
        disc=((xx-cx)**2+(yy-cy)**2)<(r+1)**2
        pm=np.zeros((h,w),bool); pm[y0:y1,x0:x1]=sub; pm|=disc
        pm=cv2.morphologyEx(pm.astype(np.uint8),cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))>0
        pm=ndi.binary_fill_holes(pm); lab,n=ndi.label(pm); sizes=ndi.sum(pm,lab,range(1,n+1)); pm=lab==(1+int(np.argmax(sizes)))
        add_erase(pm,3)
        ys,xs=np.nonzero(pm); bx=[int(xs.min())-1,int(ys.min())-1,int(xs.max())+2,int(ys.max())+2]
        k=3; sm=cv2.resize(pm[bx[1]:bx[3],bx[0]:bx[2]].astype(np.uint8)*255,None,fx=k,fy=k,interpolation=cv2.INTER_LINEAR)>127
        d=trace(sm,bx[0],bx[1],1/k,turdsize=20,alphamax=0.9)
        out.append(dict(kind='pill',box=bx,d=d,disc=[float(cx),float(cy),float(r)]))
    # --- carousel arrows are already vector; contact extras
    if page=='contact':
        # submit button
        m=np.zeros((h,w),bool); m[810:876,950:1500]=((H>100)&(H<135)&(S>120))[810:876,950:1500]|((V>200)&(S<60))[810:876,950:1500]&False
        m=ndi.binary_fill_holes(cv2.morphologyEx(m.astype(np.uint8),cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))>0)
        ys,xs=np.nonzero(m); sb=[int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1]
        m2=np.zeros((h,w),bool); m2[sb[1]-2:sb[3]+2,sb[0]-2:sb[2]+2]=True; add_erase(m2,1)
        btn=[e for e in EL if e['page']=='contact' and e['group']=='btn'][0]
        out.append(dict(kind='submit',box=sb))
        # arrow in submit after label
        out.append(dict(kind='arrow',box=[1308,832,1332,854],line=btn['id'],col='#fff'))
        # itineraire pill (dark) + diag
        x0,y0,x1,y1=70,846,256,914; m=np.zeros((h,w),bool); m[y0:y1,x0:x1]=(V<70)[y0:y1,x0:x1]
        m=ndi.binary_fill_holes(cv2.morphologyEx(m.astype(np.uint8),cv2.MORPH_CLOSE,np.ones((7,7),np.uint8))>0)
        lab,n=ndi.label(m); sizes=ndi.sum(m,lab,range(1,n+1)); m=lab==(1+int(np.argmax(sizes)))
        add_erase(m,2); ys,xs=np.nonzero(m); bx=[int(xs.min())-1,int(ys.min())-1,int(xs.max())+2,int(ys.max())+2]
        k=3; sm=cv2.resize(m[bx[1]:bx[3],bx[0]:bx[2]].astype(np.uint8)*255,None,fx=k,fy=k)>127
        it=[e for e in EL if e['page']=='contact' and e['text']=='Itinéraire'][0]
        out.append(dict(kind='darkpill',box=bx,d=trace(sm,bx[0],bx[1],1/k,turdsize=20)))
        out.append(dict(kind='diag',box=[201,869,221,889],line=it['id'],col='#fff'))
        # location pin
        m=np.zeros((h,w),bool); m[532:596,74:124]=((H>100)&(H<135)&(S>110))[532:596,74:124]; add_erase(m,2)
        ys,xs=np.nonzero(m); out.append(dict(kind='pin',box=[int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1]))
    if page=='catalogue':
        for r,y in enumerate([530,598,664,729,795,860]):
            if r==0:
                X0,X1=606,636
            else: X0,X1=600,640
            m=np.zeros((h,w),bool); m[y-16:y+16,X0:X1]=((V>150)&(S<70))[y-16:y+16,X0:X1]; add_erase(m,2)
            ys,xs=np.nonzero(m)
            if len(xs)==0: continue
            bx=[int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1]
            out.append(dict(kind='diag' if r==0 else 'arrow',box=bx,col='#fff',row=r))
    return out
def svg(el,theme_fg='var(--fg)'):
    x0,y0,x1,y1=el['box']; w_,h_=x1-x0,y1-y0; k=el['kind']
    st=f'style="left:{x0}px;top:{y0}px;width:{w_}px;height:{h_}px"'
    vb=f'viewBox="{x0} {y0} {w_} {h_}"'
    if k=='pill':
        cx,cy,r=el['disc']
        return (f'<svg class="vsvg" aria-hidden="true" {st} {vb}><path d="{el["d"]}" fill="url(#paperfill)" filter="url(#paperedge)"/>'
                f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="#0b0b0c"/>{arrow(cx,cy,r*0.8,"#fff",2.6)}</svg>')
    if k=='darkpill':
        return f'<svg class="vsvg" aria-hidden="true" {st} {vb}><path d="{el["d"]}" fill="#0b0b0c"/></svg>'
    if k=='submit':
        return f'<svg class="vsvg" aria-hidden="true" {st} {vb}><rect x="{x0}" y="{y0}" width="{w_}" height="{h_}" rx="4" fill="#0a3cff"/></svg>'
    if k in ('arrow','diag'):
        cx,cy=(x0+x1)/2,(y0+y1)/2; s=max(w_,h_)
        f=arrow if k=='arrow' else diag
        extra=f' data-line="{el["line"]}"' if el.get('line') else ''
        cls='vsvg sqd' if el.get('line') else 'vsvg'
        col=el.get('col','#fff'); col='var(--fg)' if (col=='#fff' and el.get('row') not in (None,0)) else col
        return f'<svg class="{cls}"{extra} aria-hidden="true" {st} viewBox="{x0-2} {y0-2} {w_+4} {h_+4}" overflow="visible">{f(cx,cy,s,col,2.2)}</svg>'
    if k=='pin':
        return (f'<svg class="vsvg" aria-hidden="true" {st} viewBox="0 0 24 30" preserveAspectRatio="none"><path d="M12 1.8a9 9 0 0 0-9 9c0 6.6 9 17.4 9 17.4s9-10.8 9-17.4a9 9 0 0 0-9-9z" fill="none" stroke="#0a3cff" stroke-width="3"/><circle cx="12" cy="10.6" r="3.6" fill="#0a3cff"/></svg>')
    return ''
