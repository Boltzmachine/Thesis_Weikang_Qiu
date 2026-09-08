import math
P1,P2,P3="#4472C4","#1F8A44","#C8243C"
GR,LG,INK="#8A93A0","#C9D2DD","#3C4757"
class C:
    def __init__(s): s.o=[]
    def circ(s,x,y,r,f="none",st=GR,w=1.1,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ''
        s.o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{f}" stroke="{st}" stroke-width="{w}"{d}/>')
    def ell(s,x,y,rx,ry,f="none",st=GR,w=1.1,dash=None,rot=0):
        d=f' stroke-dasharray="{dash}"' if dash else ''
        t=f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot else ''
        s.o.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{f}" stroke="{st}" stroke-width="{w}"{d}{t}/>')
    def rect(s,x,y,w_,h,f="none",st=GR,w=1.1,r=0,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ''
        rr=f' rx="{r}"' if r else ''
        s.o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w_:.1f}" height="{h:.1f}" fill="{f}" stroke="{st}" stroke-width="{w}"{rr}{d}/>')
    def line(s,x1,y1,x2,y2,st=GR,w=1.1,dash=None,arrow=False):
        d=f' stroke-dasharray="{dash}"' if dash else ''
        a=' marker-end="url(#ar)"' if arrow else ''
        s.o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{st}" stroke-width="{w}"{d}{a}/>')
    def poly(s,pts,st=GR,w=1.2,f="none"):
        p=" ".join(f"{a:.1f},{b:.1f}" for a,b in pts)
        s.o.append(f'<polyline points="{p}" fill="{f}" stroke="{st}" stroke-width="{w}"/>')
    def txt(s,x,y,t,sz=7,f=INK,anc="start",b=False):
        s.o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{sz}" fill="{f}" text-anchor="{anc}"'
                   f'{" font-weight=\"700\"" if b else ""}>{t}</text>')
    def g(s,dx,dy,fn):
        s.o.append(f'<g transform="translate({dx},{dy})">'); fn(s); s.o.append('</g>')
