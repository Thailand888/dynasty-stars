#!/usr/bin/env python3
# КОНЕЧНЫЙ ФИНАЛ: объёмная эмблема G2_champ + текст бренда (Baskerville), разделитель с AI.
import os
from PIL import Image, ImageDraw, ImageFont

src = os.path.expanduser("~/poodle/logo/gold3d/G2_champ.png")
im = Image.open(src).convert("RGB")
W,H = im.size  # 1024
px = im.load()

# Фон холста — кремовый из угла эмблемы (внутри круга, чистая зона сверху)
BG = px[512, 230]
GOLD = (150, 120, 66)
GOLD_SOFT = (165, 138, 86)

# Возьмём эмблему с запасом (сохраняем мягкую тень вокруг круга). Круг центр 512,512 r~355.
# Обрежем квадрат 1024 как есть (тень уже на кремовом) — но подровняем фон по краям под BG не будем, он и так кремовый.
emblem = im  # весь квадрат, фон кремовый с тенью — смотрится живо

OUT_W, OUT_H = 1080, 1480
canvas = Image.new("RGB",(OUT_W,OUT_H),BG)
# вписать эмблему
target = 880
em2 = emblem.resize((target,target), Image.LANCZOS)
ex=(OUT_W-target)//2; ey=70
canvas.paste(em2,(ex,ey))

draw = ImageDraw.Draw(canvas)
FONT="/System/Library/Fonts/Supplemental/Baskerville.ttc"
def font(s): return ImageFont.truetype(FONT,s)

def draw_tracked(text, y, size, track_ratio, color):
    f=font(size); track=int(size*track_ratio)
    ws=[draw.textbbox((0,0),c,font=f)[2]-draw.textbbox((0,0),c,font=f)[0] for c in text]
    full=sum(ws)+track*(len(text)-1)
    x=(OUT_W-full)//2
    for i,c in enumerate(text):
        draw.text((x,y),c,font=f,fill=color); x+=ws[i]+track
    return full

# Заголовок
title="Питомник «Из Династии Звёзд»"
ty=ey+target+30
# подобрать размер под ширину
ts=70
for s in range(80,30,-2):
    f=font(s); track=int(s*0.04)
    ws=[draw.textbbox((0,0),c,font=f)[2]-draw.textbbox((0,0),c,font=f)[0] for c in title]
    if sum(ws)+track*(len(title)-1)<=int(OUT_W*0.92): ts=s; break
draw_tracked(title, ty, ts, 0.04, GOLD)

# Разделитель: линия — AI — линия
ly=ty+ts+55
cx=OUT_W//2
draw.line([(cx-180,ly),(cx-55,ly)],fill=GOLD_SOFT,width=2)
draw.line([(cx+55,ly),(cx+180,ly)],fill=GOLD_SOFT,width=2)
af=font(40)
ab=draw.textbbox((0,0),"AI",font=af); aw=ab[2]-ab[0]; ah=ab[3]-ab[1]
draw.text((cx-aw//2-ab[0], ly-ah//2-ab[1]), "AI", font=af, fill=GOLD)

# Слоган
slogan="здесь рождаются настоящие компаньоны"
sy=ly+45
draw_tracked(slogan, sy, 40, 0.02, GOLD_SOFT)

out=os.path.expanduser("~/poodle/logo/FINAL_LOGO.png")
canvas.save(out); print("SAVED",out,"title_size",ts)
