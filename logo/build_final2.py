#!/usr/bin/env python3
# Финал v2: вырезать круг по КРУГЛОЙ маске (без золотого квадрата), кириллический шрифт Baskerville.
import os
from PIL import Image, ImageDraw, ImageFont

src = os.path.expanduser("~/poodle/logo/final2/v2_cream.png")
im = Image.open(src).convert("RGB")
W,H = im.size

# Круг: центр и радиус (внешняя обводка). По обзору низ ~740, верх ~62, центр x~512.
cx, cy = 512, 401
r_out = 345          # чуть внутрь внешней обводки, чтобы взять весь круг
# Берём кремовый цвет ИЗНУТРИ круга как фон холста (не угловой золотой!)
inside = im.load()
BG = inside[cx, cy-200]   # точка внутри круга сверху = кремовый
GOLD = (140, 110, 60)

# Вырезаем круг по маске на прозрачность, потом кладём на кремовый холст
emblem = im.crop((cx-r_out, cy-r_out, cx+r_out, cy+r_out)).convert("RGBA")
d = 2*r_out
mask = Image.new("L", (d, d), 0)
ImageDraw.Draw(mask).ellipse((0,0,d,d), fill=255)
emblem.putalpha(mask)

OUT_W, OUT_H = 1200, 1520
canvas = Image.new("RGB", (OUT_W, OUT_H), BG)
target_d = 800
em2 = emblem.resize((target_d, target_d), Image.LANCZOS)
ex = (OUT_W-target_d)//2; ey = 130
canvas.paste(em2, (ex, ey), em2)

draw = ImageDraw.Draw(canvas)
FONT = "/System/Library/Fonts/Supplemental/Baskerville.ttc"
def font(s): return ImageFont.truetype(FONT, s)

text = "ИЗ ДИНАСТИИ ЗВЁЗД"
target_w = int(OUT_W*0.80)
size=90
for s in range(150,50,-2):
    f=font(s); track=int(s*0.20)
    ws=[draw.textbbox((0,0),c,font=f)[2]-draw.textbbox((0,0),c,font=f)[0] for c in text]
    if sum(ws)+track*(len(text)-1)<=target_w: size=s; break
f=font(size); track=int(size*0.20)
ws=[draw.textbbox((0,0),c,font=f)[2]-draw.textbbox((0,0),c,font=f)[0] for c in text]
full=sum(ws)+track*(len(text)-1)
x=(OUT_W-full)//2; y=ey+target_d+80
for i,c in enumerate(text):
    draw.text((x,y),c,font=f,fill=GOLD); x+=ws[i]+track

# разделитель: линия — звезда — линия
ly=y+size+55
draw.line([(OUT_W//2-180,ly),(OUT_W//2-40,ly)],fill=GOLD,width=2)
draw.line([(OUT_W//2+40,ly),(OUT_W//2+180,ly)],fill=GOLD,width=2)
sx,sy=OUT_W//2,ly
for dx,dy in [(0,-12),(0,12),(-12,0),(12,0)]:
    draw.line([(sx,sy),(sx+dx,sy+dy)],fill=GOLD,width=2)

sub="ПИТОМНИК ТОЙ-ПУДЕЛЕЙ"
sf=font(40); sb=draw.textbbox((0,0),sub,font=sf); 
st=int(40*0.25)
sws=[draw.textbbox((0,0),c,font=sf)[2]-draw.textbbox((0,0),c,font=sf)[0] for c in sub]
sfull=sum(sws)+st*(len(sub)-1); sxx=(OUT_W-sfull)//2; syy=ly+38
for i,c in enumerate(sub):
    draw.text((sxx,syy),c,font=sf,fill=GOLD); sxx+=sws[i]+st

out=os.path.expanduser("~/poodle/logo/final2/FINAL_v2.png")
canvas.save(out); print("SAVED",out,"size",size)
