#!/usr/bin/env python3
# Собрать финал заново: вырезать ЧИСТУЮ эмблему (круг) из v2_cream, поставить на ровный кремовый холст + свой текст Didot.
import os
from PIL import Image, ImageDraw, ImageFont

src = os.path.expanduser("~/poodle/logo/final2/v2_cream.png")
im = Image.open(src).convert("RGB")
W,H = im.size  # 1024x1024

# Круг-эмблема примерно: центр (512, 400), радиус ~340 (по обзору: верх ~60, низ ~740)
# Вырежем квадрат вокруг круга с запасом
cx, cy, r = 512, 400, 350
pad = 20
box = (cx-r-pad, cy-r-pad, cx+r+pad, cy+r+pad)
emblem = im.crop(box)
ew, eh = emblem.size

# Новый холст: тёплый кремовый/слоновая кость (как внутри круга)
BG = (245, 240, 230)
GOLD = (150, 118, 64)
OUT_W, OUT_H = 1200, 1500
canvas = Image.new("RGB", (OUT_W, OUT_H), BG)

# Вставить эмблему по центру сверху
target_d = 820
emblem2 = emblem.resize((target_d, target_d), Image.LANCZOS)
ex = (OUT_W - target_d)//2
ey = 120
canvas.paste(emblem2, (ex, ey))

draw = ImageDraw.Draw(canvas)
text = "ИЗ ДИНАСТИИ ЗВЁЗД"
def font(s): return ImageFont.truetype("/System/Library/Fonts/Supplemental/Didot.ttc", s)

# подобрать размер
target_w = int(OUT_W*0.82)
size = 90
for s in range(140, 50, -2):
    f = font(s)
    track = int(s*0.16)
    widths = [draw.textbbox((0,0),ch,font=f)[2]-draw.textbbox((0,0),ch,font=f)[0] for ch in text]
    full = sum(widths)+track*(len(text)-1)
    if full <= target_w:
        size=s; break
f = font(size); track=int(size*0.16)
widths = [draw.textbbox((0,0),ch,font=f)[2]-draw.textbbox((0,0),ch,font=f)[0] for ch in text]
full = sum(widths)+track*(len(text)-1)
x = (OUT_W-full)//2
y = ey + target_d + 70
for i,ch in enumerate(text):
    draw.text((x,y),ch,font=f,fill=GOLD)
    x += widths[i]+track

# тонкая разделительная звёздочка-черта под текстом
ly = y + size + 50
draw.line([(OUT_W//2-160, ly),(OUT_W//2-30, ly)], fill=GOLD, width=2)
draw.line([(OUT_W//2+30, ly),(OUT_W//2+160, ly)], fill=GOLD, width=2)
# маленькая звезда в центре
sx, sy = OUT_W//2, ly
draw.line([(sx,sy-10),(sx,sy+10)], fill=GOLD, width=2)
draw.line([(sx-10,sy),(sx+10,sy)], fill=GOLD, width=2)
# подзаголовок
sub = "Питомник той-пуделей"
sf = ImageFont.truetype("/System/Library/Fonts/Supplemental/Didot.ttc", 38)
sb = draw.textbbox((0,0),sub,font=sf); sw=sb[2]-sb[0]
draw.text(((OUT_W-sw)//2, ly+35), sub, font=sf, fill=GOLD)

out = os.path.expanduser("~/poodle/logo/final2/FINAL_v1.png")
canvas.save(out)
print("SAVED", out, "textsize", size)
