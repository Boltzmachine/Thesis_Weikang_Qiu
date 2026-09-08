from draw import *
OR,BL,TE="#FDAA4C","#4688F1","#12796F"
def box(c,x,y,w,h,st,f="#FFFFFF",r=3,dash=None,lw=1.3): c.rect(x,y,w,h,f,st,lw,r,dash)
def down(c,x,y1,y2,col,lab=None,lx=None):
    c.line(x,y1,x,y2,col,1.4,arrow=True)
    if lab: c.txt((lx or x+6),(y1+y2)/2+2.5,lab,7.2,col,"start" if lx is None else "middle",True)

# ---------------- PART 1 ----------------
def part1(c):
    B="#4472C4"
    box(c,4,4,116,60,"#C9D2DD","#FFFFFF")
    for p in ((22,18),(40,13),(31,30),(52,20)): c.circ(*p,2.6,"#FFFFFF","#8A93A0",1)
    c.ell(31,20,17,12,"#FDAA4C22","#B87423",1,"2 2",-10)
    c.ell(46,22,13,10,"#4688F122","#2B5FB0",1,"2 2",0)
    c.txt(88,20,"high-order",6.4,"#6B7280","middle"); c.txt(88,29,"structure",6.4,"#6B7280","middle")
    c.txt(62,45,"HyBRiD",8.6,B,"middle",True); c.txt(62,57,"discover what no atlas records",6.6,"#6B7280","middle")
    box(c,134,4,116,60,"#C9D2DD","#FFFFFF")
    for i in range(3):
        for j in range(2): c.rect(144+i*8,12+j*8,6,6,"#E7EDF6","#8A93A0",0.7)
    c.circ(200,20,13,"#FFFFFF","#8A93A0",1); c.line(200,8,200,32,"#C8243C",1,"2 2")
    c.circ(194,20,2.4,BL,"#2B5FB0",0.8); c.circ(206,20,2.4,BL,"#2B5FB0",0.8)
    c.txt(192,42,"Neuro-attn · FA-EEG",7.6,B,"middle",True)
    c.txt(192,57,"build in what is already known",6.6,"#6B7280","middle")
    c.line(62,66,90,78,B,1.3); c.line(192,66,164,78,B,1.3)
    box(c,4,80,246,30,B,"#EDF2FA",3)
    c.txt(127,99,"models that respect brain organisation",7.8,B,"middle",True)
    down(c,127,112,136,"#6B4FA8")
    c.txt(133,126,"SWA · the prior travels back out",7,"#6B4FA8","start",True)
    box(c,4,138,246,26,"#6B4FA8","#F4F1FA",3,"3 2")
    c.txt(127,155,"…improves a model with no brain in it",7.4,"#6B4FA8","middle",True)

# ---------------- PART 2 ----------------
def part2(c):
    G="#1F8A44"
    box(c,66,2,122,24,"#C9D2DD","#FFFFFF")
    c.ell(84,14,7,8,"#FFE9D2","#B87423",1)
    c.txt(148,17,"brain-signal encoder",6.8,"#6B7280","middle")
    c.txt(148,10,"(from Part 1)",5.8,"#8A93A0","middle")
    down(c,127,28,50,G); c.txt(133,42,"Brain Instruction Tuning",7.2,G,"start",True)
    box(c,4,54,150,52,G,"#EDF6F0",3,lw=1.5)
    for i,(k,v) in enumerate((("obj","dog"),("attr","fluffy"),("rel","on grass"))):
        c.txt(12,68+i*13,k,7,G,b=True); c.txt(44,68+i*13,v,7,"#6B7280")
    c.txt(79,50,"the target space",6.2,"#8A93A0","middle")
    c.line(196,80,160,80,G,1.3,arrow=True)
    box(c,198,68,52,24,G,"#FFFFFF",3)
    c.txt(224,79,"PRISM",7.6,G,"middle",True); c.txt(224,88,"which space?",5.8,"#6B7280","middle")
    down(c,79,108,128,G); c.txt(85,120,"D-Edit",7.2,G,"start",True)
    box(c,4,130,150,32,"#C2650B","#FBF3EA",3)
    c.rect(12,136,34,20,"#FFFFFF","#8A93A0",0.9); c.line(29,136,29,156,"#8A93A0",0.8); c.line(29,146,46,146,"#8A93A0",0.8)
    c.txt(102,143,"per-item",6.8,"#C2650B","middle",True); c.txt(102,153,"controllable generation",6.8,"#C2650B","middle")

# ---------------- PART 3 ----------------
def part3(c):
    R="#C8243C"; A="#B87423"
    c.txt(127,1,"(intent is represented — now make it act)",6,"#8A93A0","middle")
    box(c,4,6,246,42,"#C9D2DD","#FFFFFF")
    c.poly([(14,30),(18,20),(22,36),(26,22),(30,32),(34,26),(38,28)],A,1.2)
    c.txt(26,44,"EEG",5.8,"#6B7280","middle")
    c.line(42,28,52,28,"#8A93A0",1,arrow=True)
    box(c,54,19,34,18,A,"#FFF3E8",2); c.txt(71,31,"mind",6.6,A,"middle",True)
    c.line(90,28,100,28,"#8A93A0",1,arrow=True)
    c.rect(102,18,22,18,"#EDF1F5","#8A93A0",1); c.rect(130,18,22,18,"#EDF1F5","#8A93A0",1)
    c.line(124,27,130,27,R,1.1,"2 2",arrow=True)
    c.txt(127,44,"predict next frame",5.8,"#6B7280","middle")
    c.txt(200,24,"Mind World Models",7,A,"middle",True); c.txt(200,35,"label-free supervision",6.2,"#6B7280","middle")
    down(c,127,50,72,R); c.txt(133,63,"a goal, not a trajectory",7.2,R,"start",True)
    box(c,4,74,246,32,R,"#FBEDEF",3)
    for i,x in enumerate((16,28,40,52)):
        c.circ(x,90,3,("#FDAA4C" if i<2 else ("#4688F1" if i==2 else "#FFFFFF")),"#8A93A0",0.9)
    c.circ(64,90,4.5,"none",TE,1.4)
    c.txt(160,87,"PHIL · learned cost-to-go",7.2,R,"middle",True)
    c.txt(160,98,"turns the goal into a path",6.4,"#6B7280","middle")
    down(c,127,108,130,R); c.txt(133,121,"a plan",7.2,R,"start",True)
    box(c,4,134,246,32,R,"#FBEDEF",3)
    for i in range(3):
        c.rect(14+i*20,140,16,12,"#EDF1F5","#8A93A0",0.9); c.rect(14+i*20,154,16,4,"#4688F1","none",0)
    c.rect(14,152,56,2,"#1F8A44","none",0)
    c.txt(160,147,"SD-VLA · real-time execution",7.2,R,"middle",True)
    c.txt(160,158,"static cached, dynamic recomputed",6.4,"#6B7280","middle")
COLS={"col1":part1,"col2":part2,"col3":part3}
