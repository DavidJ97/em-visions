import numpy as np, cv2
from scipy.ndimage import median_filter
def hsvsplit(im):
    hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV); return hsv[...,0].astype(int),hsv[...,1].astype(int),hsv[...,2].astype(int)
def classmask(im,cls):
    H,S,V=hsvsplit(im)
    return {'w':(V>140)&(S<80),'b':(H>100)&(H<135)&(S>120)&(V>110),'k':V<110,'k2':V<150,
            'g':(V<200)&(V>40),'wt':(V>190)&(S<70)}[cls]
def clean(m,minarea=5):
    n,lab,st,_=cv2.connectedComponentsWithStats(m.astype(np.uint8),connectivity=8)
    keep=np.zeros(n,bool); keep[1:]=st[1:,4]>=minarea
    return keep[lab]
def runs(v):
    r=[];i=0;n=len(v)
    while i<n:
        if v[i]:
            j=i
            while j<n and v[j]: j+=1
            r.append([i,j]); i=j
        else: i+=1
    return r
def split_bands(prof,n):
    b=runs(prof>0)
    while len(b)>n:
        gaps=[b[i+1][0]-b[i][1] for i in range(len(b)-1)]; k=int(np.argmin(gaps)); b[k]=[b[k][0],b[k+1][1]]; del b[k+1]
    while len(b)<n:
        k=int(np.argmax([e-s for s,e in b])); s,e=b[k]; lo=s+(e-s)//5; hi=e-(e-s)//5
        c=lo+int(np.argmin(prof[lo:hi])); b[k]=[s,c]; b.insert(k+1,[c+1,e])
    return b
def lines(im,region,cls,n,split='v',minarea=5,exclude=()):
    x0,y0,x1,y1=region; mm=classmask(im,cls).copy()
    for a,b,c,d in exclude: mm[b:d,a:c]=False
    m=clean(mm[y0:y1,x0:x1],minarea)
    if split=='v' and n>1: return lines_acc(m,x0,y0,n),m
    prof=m.sum(1) if split=='v' else m.sum(0)
    out=[]
    for s,e in split_bands(prof,n):
        sub=m[s:e,:] if split=='v' else m[:,s:e]
        ys,xs=np.nonzero(sub)
        if split=='v': out.append([int(x0+xs.min()),int(y0+s+ys.min()),int(x0+xs.max()+1),int(y0+s+ys.max()+1)])
        else: out.append([int(x0+s+xs.min()),int(y0+ys.min()),int(x0+s+xs.max()+1),int(y0+ys.max()+1)])
    return out,m
# ---------- hole tracing
def _inner(vals,maxstart,gapmax=5):
    i=0;n=len(vals)
    while i<min(n,maxstart):
        if vals[i]:
            j=i;gap=0;last=i
            while j<n and gap<=gapmax:
                if vals[j]: last=j;gap=0
                else: gap+=1
                j+=1
            if last-i>=3: return last
            i=j
        else: i+=1
    return None
def radial(im,guide,c,xmin=-1e9,xmax=1e9,wall=(150,860),N=3000,depth=90):
    h,w=im.shape[:2]; H,S,V=hsvsplit(im); W1=(V>165)&(S<65); W2=(V>105)&(S<80)
    gm=np.zeros((h,w),np.uint8); cv2.fillPoly(gm,[np.array(guide,np.int32)],1)
    cx,cy=c; R=np.full(N,np.nan)
    for k in range(N):
        t=2*np.pi*k/N; dx,dy=np.cos(t),np.sin(t)
        rs=np.arange(900,0,-1); xs=(cx+rs*dx).round().astype(int); ys=(cy+rs*dy).round().astype(int)
        ok=(xs>=0)&(xs<w)&(ys>=0)&(ys<h); rs,xs,ys=rs[ok],xs[ok],ys[ok]
        ing=gm[ys,xs]>0
        if not ing.any(): continue
        f=np.argmax(ing); rs,xs,ys=rs[f:],xs[f:],ys[f:]
        rw=1e9
        if dx>0: rw=(xmax-cx)/dx
        if dx<0: rw=(xmin-cx)/dx
        ins=(xs<xmax)&(xs>xmin)
        idx=_inner(W1[ys,xs]&ins,depth)
        if idx is None: idx=_inner(W2[ys,xs]&ins,depth)
        if idx is not None: R[k]=min(rs[idx],rw)
        elif rs[0]>=rw-2: R[k]=rw
    g=~np.isnan(R); ii=np.arange(N); R=np.interp(ii,ii[g],R[g],period=N)
    big=median_filter(R,size=61,mode='wrap'); R=np.where(np.abs(R-big)>20,big,R)
    t=2*np.pi*ii/N; P=np.stack([cx+R*np.cos(t),cy+R*np.sin(t)],1)
    out=[]
    for (x,y),tt in zip(P,t):
        dx,dy=np.cos(tt),np.sin(tt)
        if dx>0 and xmax<1e8:
            r=(xmax-cx)/dx; yy=cy+r*dy
            if wall[0]<yy<wall[1]: x,y=xmax,yy
        out.append((min(max(x,xmin),xmax),y))
    return np.array(out)
def colscan(im,x0,x1,ytop,ybot,depth=90):
    H,S,V=hsvsplit(im); W1=(V>165)&(S<65); W2=(V>105)&(S<80)
    xs=np.arange(x0,x1+1); top=[];bot=[]
    for x in xs:
        for seq,arr in ((np.arange(ytop,ybot),top),(np.arange(ybot,ytop,-1),bot)):
            i=_inner(W1[seq,x],depth)
            if i is None: i=_inner(W2[seq,x],depth)
            arr.append(seq[i] if i is not None else np.nan)
    def cl(a):
        a=np.array(a,float); g=~np.isnan(a); ii=np.arange(len(a)); a=np.interp(ii,ii[g],a[g])
        big=median_filter(a,size=41,mode='nearest'); return np.where(np.abs(a-big)>18,big,a)
    top=cl(top);bot=cl(bot)
    return np.concatenate([np.stack([xs,top],1),np.stack([xs[::-1],bot[::-1]],1)])
def _run(vals,maxstart,gapmax=5):
    i=0;n=len(vals)
    while i<min(n,maxstart):
        if vals[i]:
            j=i;gap=0;last=i
            while j<n and gap<=gapmax:
                if vals[j]: last=j;gap=0
                else: gap+=1
                j+=1
            if last-i>=3: return i,last
            i=j
        else: i+=1
    return None
def edge_profile(seqvals_list, interior_ok, depth=90, pct=45, tmax=40):
    # seqvals_list: list of (W bool array along ray outside->inside, interiorWhite bool array)
    so=[];si=[];rel=[]
    for W,Wi in seqvals_list:
        r=_run(W,depth)
        if r is None: so.append(np.nan);si.append(np.nan);rel.append(False);continue
        a,b=r; so.append(a); si.append(b)
        inside=Wi[b+1:b+7]
        rel.append(len(inside)>0 and inside.mean()<0.5 and (b-a)<tmax)
    so=np.array(so,float);si=np.array(si,float);rel=np.array(rel)
    t=si-so; n=len(t); out=si.copy()
    tr=np.where(rel,t,np.nan)
    for k in range(n):
        if not rel[k] and not np.isnan(so[k]):
            win=tr[max(0,k-60):k+60]; win=win[~np.isnan(win)]
            tt=np.percentile(win,pct) if len(win) else 14
            out[k]=so[k]+tt
    return out,so
def radial2(im,guide,c,xmin=-1e9,xmax=1e9,wall=(150,860),N=3000,depth=90):
    h,w=im.shape[:2]; H,S,V=hsvsplit(im); W=(V>150)&(S<70); Wi=(V>150)&(S<90)
    gm=np.zeros((h,w),np.uint8); cv2.fillPoly(gm,[np.array(guide,np.int32)],1)
    cx,cy=c; rays=[];meta=[]
    for k in range(N):
        t=2*np.pi*k/N; dx,dy=np.cos(t),np.sin(t)
        rs=np.arange(900,0,-1); xs=(cx+rs*dx).round().astype(int); ys=(cy+rs*dy).round().astype(int)
        ok=(xs>=0)&(xs<w)&(ys>=0)&(ys<h)&(xs<xmax)&(xs>xmin); rs,xs,ys=rs[ok],xs[ok],ys[ok]
        ing=gm[ys,xs]>0
        if not ing.any(): rays.append((np.zeros(1,bool),np.zeros(1,bool))); meta.append(None); continue
        f=np.argmax(ing); rs,xs,ys=rs[f:],xs[f:],ys[f:]
        rays.append((W[ys,xs],Wi[ys,xs])); meta.append(rs)
    ins,_=edge_profile(rays,None,depth)
    R=np.full(N,np.nan)
    for k in range(N):
        if meta[k] is not None and not np.isnan(ins[k]): R[k]=meta[k][int(min(ins[k],len(meta[k])-1))]
    g=~np.isnan(R); ii=np.arange(N); R=np.interp(ii,ii[g],R[g],period=N)
    big=median_filter(R,size=41,mode='wrap'); R=np.where(np.abs(R-big)>25,big,R)
    t=2*np.pi*ii/N; out=[]
    for r,tt in zip(R,t):
        dx,dy=np.cos(tt),np.sin(tt); x,y=cx+r*dx,cy+r*dy
        if dx>0 and xmax<1e8:
            rr=(xmax-cx)/dx; yy=cy+rr*dy
            if wall[0]<yy<wall[1] or x>xmax: x,y=xmax,yy
        out.append((max(x,xmin),y))
    return np.array(out)
def colscan2(im,x0,x1,ytop,ybot,depth=90):
    H,S,V=hsvsplit(im); W=(V>150)&(S<70); Wi=(V>150)&(S<90)
    xs=np.arange(x0,x1+1)
    res=[]
    for seqf in (lambda: np.arange(ytop,ybot), lambda: np.arange(ybot,ytop,-1)):
        seq=seqf(); rays=[(W[seq,x],Wi[seq,x]) for x in xs]
        ins,_=edge_profile(rays,None,depth,tmax=26)
        a=np.array([seq[int(min(i,len(seq)-1))] if not np.isnan(i) else np.nan for i in ins],float)
        g=~np.isnan(a); ii=np.arange(len(a)); a=np.interp(ii,ii[g],a[g])
        big=median_filter(a,size=31,mode='nearest'); a=np.where(np.abs(a-big)>18,big,a); res.append(a)
    top,bot=res
    return np.concatenate([np.stack([xs,top],1),np.stack([xs[::-1],bot[::-1]],1)])

def lines_acc(m,x0,y0,n):
    k,lab,st,_=cv2.connectedComponentsWithStats(m.astype(np.uint8),connectivity=8)
    if k<=1: return []
    areas=st[1:,4]; big=[i for i in range(1,k) if st[i,4]>=0.15*areas.max()]
    hmax=float(np.median([st[i,3] for i in big]))
    body=[i for i in range(1,k) if 0.45*hmax<=st[i,3]<=1.5*hmax]
    prof=np.zeros(m.shape[0])
    for i in body: prof[st[i,1]:st[i,1]+st[i,3]]+=1
    bands=split_bands(prof,n)
    boxes=[[1e9,1e9,-1,-1] for _ in bands]
    def add(bi,i):
        x,y,w,h=st[i,:4]; b=boxes[bi]; b[0]=min(b[0],x);b[1]=min(b[1],y);b[2]=max(b[2],x+w);b[3]=max(b[3],y+h)
    bx=[[1e9,-1] for _ in bands]
    for i in body:
        x,y,w,h=st[i,:4]; bi=int(np.argmin([abs(y+h/2-(s+e)/2) for s,e in bands])); bx[bi]=[min(bx[bi][0],x),max(bx[bi][1],x+w)]
    for i in range(1,k):
        x,y,w,h=st[i,:4]; cy=y+h/2
        if i in body:
            bi=int(np.argmin([abs(cy-(s+e)/2) for s,e in bands]))
        else:
            inside=[j for j,(s,e) in enumerate(bands) if s<=cy<=e and x<bx[j][1] and x+w>bx[j][0]]
            below=[j for j,(s,e) in enumerate(bands) if s>=y+h-6 and s-(y+h)<0.35*hmax and h<0.3*hmax and x<bx[j][1] and x+w>bx[j][0]]
            if h>1.5*hmax or not (inside or below): continue
            bi=inside[0] if inside else below[0]
        add(bi,i)
    return [[int(x0+b[0]),int(y0+b[1]),int(x0+b[2]),int(y0+b[3])] for b in boxes]
