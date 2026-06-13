#!/usr/bin/env python3
# Наложить новый текст на финальную эмблему питомника.
import os
from PIL import Image, ImageDraw, ImageFont

src = "/Users/thai/.hermes/image_cache/img_af706a5c3f3c.jpg"
im = Image.open(src).convert("RGB")
W,H = im.size  # 1010 x 1280
px = im.load()
BG = px[15,15]            # кремовый фон
GOLD = (150, 120, 64)     # тёплое золото-коричневый в тон обводке
DARK = (95, 78, 52)

# 1) Замазать старую текстовую зону (всё ниже эмблемы ~y=852)
draw = ImageDraw.Draw(im)
draw.rectangle([0, 852, W, H], fill=BG)

FONT = "/System/Library/Fonts/Supplemental/Baskerville.ttc"
def font(s, idx=0):
    return ImageFont.truetype(FONT, s, index=idx)

def measure(text, f, track):
    ws = [draw.textbbox((0,0),c,font=f)[2]-draw.textbbox((0,0),c,font=f)[0] for c in text]
    return ws, sum(ws)+track*(len(text)-1)

def draw_tracked(text, f, track, y, color):
    ws, full = measure(text, f, track)
    x = (W-full)//2
    for i,c in enumerate(text):
        draw.text((x,y), c, font=f, fill=color)
        x += ws[i]+track

# Заголовок: Питомник «Из Династии Звёзд»
title = "Питомник «Из Династии Звёзд»"
# подобрать размер под 86% ширины
target_w = int(W*0.88)
ts = 70
for s in range(78, 30, -1):
    f = font(s); track = int(s*0.04)
    _, full = measure(title, f, track)
    if full <= target_w: ts = s; break
ft = font(ts); ttrack = int(ts*0.04)

# Разделитель-звезда + подзаголовок
sub = "здесь рождаются настоящие компаньоны"
ss = 40
for s in range(46, 22, -1):
    f = font(s); track = int(s*0.06)
    _, full = measure(sub, f, track)
    if full <= int(W*0.90): ss = s; break
fs = font(ss); strack = int(ss*0.06)

# Вёрстка по вертикали
y_title = 905
draw_tracked(title, ft, ttrack, y_title, DARK)

ly = y_title + ts + 48
# линия — звезда — линия
draw.line([(W//2-150, ly),(W//2-34, ly)], fill=GOLD, width=2)
draw.line([(W//2+34, ly),(W//2+150, ly)], fill=GOLD, width=2)
sx,sy=W//2,ly
for dx,dy in [(0,-11),(0,11),(-11,0),(11,0)]:
    draw.line([(sx,sy),(sx+dx,sy+dy)], fill=GOLD, width=2)

y_sub = ly + 34
draw_tracked(sub, fs, strack, y_sub, GOLD)

out = os.path.expanduser("~/poodle/logo/final2/FINAL_new_text.png")
im.save(out)
print("SAVED", out, "title_size", ts, "sub_size", ss)
