#!/usr/bin/env python3
# Замазать битый AI-текст и наложить чистый "ИЗ ДИНАСТИИ ЗВЁЗД" шрифтом Didot.
import os
from PIL import Image, ImageDraw, ImageFont

src = os.path.expanduser("~/poodle/logo/final2/v2_cream.png")
im = Image.open(src).convert("RGB")
W,H = im.size  # 1024x1024
px = im.load()

# 1) Замазать нижнюю текстовую зону чистым фоном (берём цвет из угла — белый/кремовый).
bg = px[20,20]  # верхний левый угол = фон
draw = ImageDraw.Draw(im)
draw.rectangle([0, 755, W, H], fill=bg)

# 2) Наложить свой текст. Цвет — тёплое золото-коричневый как у обводки.
gold = (138, 109, 62)
text = "ИЗ ДИНАСТИИ ЗВЁЗД"

# Подобрать размер Didot под ширину ~78% полотна
def load_font(size):
    return ImageFont.truetype("/System/Library/Fonts/Supplemental/Didot.ttc", size)

target_w = int(W*0.80)
size = 96
for s in range(120, 40, -2):
    f = load_font(s)
    # межбуквенный интервал руками
    bbox = draw.textbbox((0,0), text, font=f)
    w = bbox[2]-bbox[0]
    # добавим трекинг ~ 0.12*size на каждый пробел между символами
    track = int(s*0.18)
    w_tracked = w + track*(len(text)-1)
    if w_tracked <= target_w:
        size = s; break

f = load_font(size)
track = int(size*0.18)

# отрисовать с трекингом, по центру, под кругом (~y=820)
# сначала измерим полную ширину с трекингом
widths = []
for ch in text:
    b = draw.textbbox((0,0), ch, font=f)
    widths.append(b[2]-b[0])
full_w = sum(widths) + track*(len(text)-1)
x = (W - full_w)//2
y = 840
asc, desc = f.getmetrics()
for i,ch in enumerate(text):
    draw.text((x, y), ch, font=f, fill=gold)
    x += widths[i] + track

out = os.path.expanduser("~/poodle/logo/final2/FINAL_white_fixed.png")
im.save(out)
print("SAVED", out, "size", size, "fullw", full_w)
