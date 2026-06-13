#!/usr/bin/env python3
# Добавить ТОЛЬКО кружок 'AI' надстрочно после слова ЗВЁЗД. Исходник не трогаем больше ничем.
import os
from PIL import Image, ImageDraw, ImageFont

src = os.path.expanduser("~/poodle/logo/source_logo.jpg")
im = Image.open(src).convert("RGB")
W,H = im.size  # 1010x1280
px = im.load()

# Цвет золота титула — возьмём из тёмной точки буквы. Сэмплируем область буквы Д (~x900,y895).
# Найдём самый "золотой/тёмный" пиксель в зоне.
def sample_text_color():
    best=None
    for yy in range(865,930):
        for xx in range(870,915):
            r,g,b=px[xx,yy]
            # текст темнее фона
            if r<180 and g<150:
                if best is None or (r+g+b)<sum(best):
                    best=(r,g,b)
    return best or (150,120,66)
GOLD = sample_text_color()
BG = px[980, 895]  # фон справа от текста

draw = ImageDraw.Draw(im)

# Кружок AI — надстрочно справа-сверху от Д
cx, cy, R = 948, 876, 27   # центр и радиус
draw.ellipse([cx-R, cy-R, cx+R, cy+R], outline=GOLD, width=3)

# 'AI' внутри
FONT="/System/Library/Fonts/Supplemental/Baskerville.ttc"
f=ImageFont.truetype(FONT, 26)
b=draw.textbbox((0,0),"AI",font=f); tw=b[2]-b[0]; th=b[3]-b[1]
draw.text((cx-tw//2-b[0], cy-th//2-b[1]), "AI", font=f, fill=GOLD)

out=os.path.expanduser("~/poodle/logo/LOGO_AI_BADGE.png")
im.save(out)
print("SAVED", out, "GOLD", GOLD, "BG", BG)
