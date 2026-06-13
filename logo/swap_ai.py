#!/usr/bin/env python3
# Заменить '+' в разделителе на 'AI'. Сохранить боковые линии.
import os
from PIL import Image, ImageDraw, ImageFont

src = os.path.expanduser("~/poodle/logo/final2/FINAL_new_text.png")
im = Image.open(src).convert("RGB")
W,H = im.size
px = im.load()
BG = px[15,15]
GOLD = (150, 118, 64)
draw = ImageDraw.Draw(im)

# Зона '+' по центру разделителя. Центр ~ (W//2, 1015). Замажем узкий прямоугольник МЕЖДУ линиями.
cx = W//2
# Найдём вертикальный уровень разделителя: примерно y 1000-1035
# Замазываем только центральный зазор (линии заканчиваются ~ cx-70 и начинаются ~ cx+70)
gap_l, gap_r = cx-72, cx+72
y_top, y_bot = 990, 1045
draw.rectangle([gap_l, y_top, gap_r, y_bot], fill=BG)

# Вписать 'AI' по центру зазора, в тон золоту, шрифт Baskerville
FONT = "/System/Library/Fonts/Supplemental/Baskerville.ttc"
f = ImageFont.truetype(FONT, 46)
txt = "AI"
b = draw.textbbox((0,0), txt, font=f)
tw, th = b[2]-b[0], b[3]-b[1]
tx = cx - tw//2 - b[0]
ty = (y_top+y_bot)//2 - th//2 - b[1]
draw.text((tx, ty), txt, font=f, fill=GOLD)

out = os.path.expanduser("~/poodle/logo/final2/FINAL_AI.png")
im.save(out)
print("SAVED", out)
