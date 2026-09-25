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
    rows=[(4,"PRISM I","Choose the fMRI alignment space"),
          (45,"MindLLM","Align fMRI to language"),
          (86,"PRISM II","Reconstruct visual content from language"),
          (127,"D-Edit","Item prompts + grouped cross-attention")]
    for i,(y,title,detail) in enumerate(rows):
        box(c,4,y,246,31,G,"#EDF6F0",3)
        c.txt(127,y+12,title,8.4,G,"middle",True)
        c.txt(127,y+24,detail,6.6,"#6B7280","middle")
        if i<3: down(c,127,y+33,y+39,G)
    c.txt(127,168,"Research progression; stronger per-item generation disentanglement",5.3,"#6B7280","middle")

# ---------------- PART 3 ----------------
def part3(c):
    R="#C8243C"; P="#6B4FA8"
    c.txt(127,3,"Two research branches",7.3,R,"middle",True)
    box(c,4,15,116,140,R,"#FBEDEF",3)
    c.txt(62,36,"MWM",9,R,"middle",True)
    c.txt(62,66,"Brain signals",7,"#6B7280","middle")
    c.txt(62,78,"to action meaning",7,"#6B7280","middle")
    c.txt(62,112,"EEG latent actions",6.6,"#6B7280","middle")
    c.txt(62,124,"predict visual consequences",5.8,"#6B7280","middle")
    box(c,130,15,120,140,R,"#FFFFFF",3)
    c.txt(190,31,"Act toward",7.4,R,"middle",True)
    c.txt(190,42,"specified goals",7.4,R,"middle",True)
    box(c,137,51,106,42,P,"#F4F1FA",3)
    c.txt(190,64,"PHIL",8,P,"middle",True)
    c.txt(190,76,"Learned heuristic",6.2,"#6B7280","middle")
    c.txt(190,86,"for graph search",6.2,"#6B7280","middle")
    box(c,137,104,106,42,R,"#FBEDEF",3)
    c.txt(190,117,"DySta",8,R,"middle",True)
    c.txt(190,129,"Visual policy",6.2,"#6B7280","middle")
    c.txt(190,139,"Memory + fast inference",5.8,"#6B7280","middle")
    c.txt(127,168,"Separately evaluated; not an integrated model pipeline",5.6,"#6B7280","middle")
COLS={"col1":part1,"col2":part2,"col3":part3}
