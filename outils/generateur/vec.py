import numpy as np, potrace
def trace(mask, x0=0, y0=0, scale=1.0, turdsize=4, alphamax=1.0, opttol=0.2):
    bm=potrace.Bitmap(~mask.astype(bool))
    pl=bm.trace(turdsize=turdsize,alphamax=alphamax,opticurve=True,opttolerance=opttol)
    f=lambda p:f"{x0+p.x*scale:.2f} {y0+p.y*scale:.2f}"
    d=[]
    for c in pl:
        d.append("M"+f(c.start_point))
        for s in c.segments:
            if s.is_corner: d.append("L"+f(s.c)+" L"+f(s.end_point))
            else: d.append("C"+f(s.c1)+" "+f(s.c2)+" "+f(s.end_point))
        d.append("Z")
    return "".join(d)
