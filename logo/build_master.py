#!/usr/bin/env python3
# ФИНАЛ v2: эмблема G2 + заголовок с надстрочным значком (AI) в кружке как (R)/(C). Разделитель — звезда.
import os
from PIL import Image, ImageDraw, ImageFont

src = os.path.expanduser("~/poodle/logo/gold3d/G2_champ.png")
im = Image.open(src).convert("RGB")
W,H = im.size
px = im.load()
BG = px[512, 230]
GOLD = (150, 120, 66)
GOLD_SOFT = (165, 138, 86)

OUT_W, OUT_H = 1080, 1480
canvas = Image.new("RGB",(OUT_W,OUT_H),BG)
target=880
em2 = im.resize((target,target), Image.LANCZOS)
ex=(OUT_W-target)//2; ey=70
canvas.paste(em2,(ex,ey))
draw = ImageDraw.Draw(canvas)
FONT="/System/Library/Fonts/Supplemental/Baskerville.ttc"
def font(s): return ImageFont.truetype(FONT,s)

title="Питомник «Из Династии Звёзд»"
ty=ey+target+30
# размер заголовка с запасом справа под значок
ts=66
for s in range(80,30,-2):
    f=font(s); track=int(s*0.04)
    ws=[draw.textbbox((0,0),c,font=f)[2]-draw.textbbox((0,0),c,font=f)[0] for c in title]
    if sum(ws)+track*(len(title)-1) <= int(OUT_W*0.82): ts=s; break
f=font(ts); track=int(ts*0.04)
ws=[draw.textbbox((0,0),c,font=f)[2]-draw.textbbox((0,0),c,font=f)[0] for c in title]
full=sum(ws)+track*(len(title)-1)
badge_reserve = int(ts*0.85)   # место под надстрочный кружок справа
x0=(OUT_W-full-badge_reserve)//2
x=x0
for i,c in enumerate(title):
    draw.text((x,ty),c,font=f,fill=GOLD); x+=ws[i]+track
title_right = x - track   # правый край последнего символа »
# высота заголовка
tb=draw.textbbox((0,0),title,font=f); title_top=ty; title_h=tb[3]-tb[1]

# --- Надстрочный значок: кружок с AI, верх-право от слова ---
badge_d = int(ts*0.62)            # диаметр кружка
bx = title_right + int(ts*0.12)   # отступ справа
by = ty - int(ts*0.18)            # приподнят над строкой (superscript)
# тонкий золотой кружок
draw.ellipse([bx, by, bx+badge_d, by+badge_d], outline=GOLD, width=3)
# буквы AI внутри
af = font(int(badge_d*0.5))
ab = draw.textbbox((0,0),"AI",font=af); aw=ab[2]-ab[0]; ah=ab[3]-ab[1]
draw.text((bx+badge_d/2-aw/2-ab[0], by+badge_d/2-ah/2-ab[1]), "AI", font=af, fill=GOLD)

# --- Разделитель: линия — звезда — линия ---
ly=ty+ts+58
cx=OUT_W//2
draw.line([(cx-175,ly),(cx-40,ly)],fill=GOLD_SOFT,width=2)
draw.line([(cx+40,ly),(cx+175,ly)],fill=GOLD_SOFT,width=2)
# 4-конечная лучистая звезда (полигон с тонкими лучами)
import math
def star4(cx,cy,R,r):
    pts=[]
    for k in range(8):
        ang=math.pi/2 + k*math.pi/4
        rad = R if k%2==0 else r
        pts.append((cx+rad*math.cos(ang), cy-rad*math.sin(ang)))
    return pts
draw.polygon(star4(cx,ly,18,5), fill=GOLD)

# --- Слоган ---
slogan="здесь рождаются настоящие компаньоны"
sy=ly+42
sf=font(40); st=int(40*0.02)
sws=[draw.textbbox((0,0),c,font=sf)[2]-draw.textbbox((0,0),c,font=sf)[0] for c in slogan]
sfull=sum(sws)+st*(len(slogan)-1); sx=(OUT_W-sfull)//2
for i,c in enumerate(slogan):
    draw.text((sx,sy),c,font=sf,fill=GOLD_SOFT); sx+=sws[i]+st

out=os.path.expanduser("~/poodle/logo/FINAL_LOGO.png")
canvas.save(out); print("SAVED",out,"title_size",ts,"title_right",title_right,"badge_at",bx,by)
