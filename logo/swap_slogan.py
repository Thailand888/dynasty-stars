#!/usr/bin/env python3
# Заменить ТОЛЬКО нижнюю строку 'ПИТОМНИК ТОЙ-ПУДЕЛЕЙ' на 'здесь рождается дружба'. Остальное не трогаем.
import os
from PIL import Image, ImageDraw, ImageFont

src = os.path.expanduser("~/poodle/logo/LOGO_AI_BADGE.png")
im = Image.open(src).convert("RGB")
W,H = im.size  # 1010x1280
px = im.load()

# Зона нижней строки. По обзору текст ~ y 985-1035. Разделитель '+' выше (~955), его НЕ трогаем.
y_top, y_bot = 975, 1055
x_l, x_r = 120, 890

# Цвет нижней строки (светлое золото) — сэмпл из тёмных пикселей зоны
def sample():
    best=None
    for yy in range(y_top, y_bot):
        for xx in range(x_l, x_r):
            r,g,b=px[xx,yy]
            if r<200 and g<185 and abs(r-g)<60:
                if best is None or (r+g+b)<best[3]:
                    best=(r,g,b,r+g+b)
    return best[:3] if best else (150,120,80)
GOLD = sample()
BG = px[60, 1015]  # фон слева, вне текста

draw = ImageDraw.Draw(im)
# Замазать старую строку фоном
draw.rectangle([0, y_top, W, y_bot], fill=BG)

# Новый текст
FONT="/System/Library/Fonts/Supplemental/Baskerville.ttc"
text="здесь рождается дружба"
# подобрать размер под примерно ту же ширину (~62% полотна)
def font(s): return ImageFont.truetype(FONT, s)
target_w = int(W*0.62)
size=44
for s in range(70,28,-2):
    f=font(s); track=int(s*0.10)
    ws=[draw.textbbox((0,0),c,font=f)[2]-draw.textbbox((0,0),c,font=f)[0] for c in text]
    if sum(ws)+track*(len(text)-1)<=target_w: size=s; break
f=font(size); track=int(size*0.10)
ws=[draw.textbbox((0,0),c,font=f)[2]-draw.textbbox((0,0),c,font=f)[0] for c in text]
full=sum(ws)+track*(len(text)-1)
x=(W-full)//2
# вертикально по центру зоны
asc,desc=f.getmetrics()
y=y_top + ( (y_bot-y_top) - (asc+desc) )//2 + 4
for i,c in enumerate(text):
    draw.text((x,y),c,font=f,fill=GOLD); x+=ws[i]+track

out=os.path.expanduser("~/poodle/logo/LOGO_FINAL2.png")
im.save(out)
print("SAVED", out, "GOLD", GOLD, "BG", BG, "size", size)
