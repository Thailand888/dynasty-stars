#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont
D = os.path.expanduser("~/poodle/logo/bond")
files = sorted([f for f in os.listdir(D) if f.endswith(".png") and not f.startswith("_")])
cols, cell, pad, label_h = 4, 420, 16, 36
rows = (len(files)+cols-1)//cols
W = cols*cell + pad*(cols+1)
H = rows*(cell+label_h) + pad*(rows+1) + 50
canvas = Image.new("RGB",(W,H),(15,17,21))
draw = ImageDraw.Draw(canvas)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 22)
    big = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 30)
except:
    font = ImageFont.load_default(); big = font
draw.text((pad,12), "СВЯЗЬ ЧЕЛОВЕК+СОБАКА + ТЁПЛЫЙ СВЕТ AI (GPT-5-Image)", fill=(245,200,120), font=big)
labels = {
 "b01_hand_paw":"Рука+лапа тянутся, AI-звезда",
 "b02_hand_paw_heart":"Рука+лапа = сердце с AI",
 "b03_silhouette_star":"Человек+пудель под звездой",
 "b04_embrace":"Объятие, ореол-хранитель",
 "b05_community_orbit":"Сообщество вокруг AI-света",
 "b06_glow_paw_hand":"Ладонь держит светящ. лапу",
 "b07_poodle_light":"Свет пуделя освещает лицо",
 "b08_paw_hand_star":"Минимал: рука+лапа в звезду",
}
for i,fn in enumerate(files):
    r,c = divmod(i,cols)
    x = pad + c*(cell+pad); y = 50 + pad + r*(cell+label_h+pad)
    im = Image.open(os.path.join(D,fn)).convert("RGB"); im.thumbnail((cell,cell))
    ox = x+(cell-im.width)//2; oy = y+(cell-im.height)//2
    canvas.paste(im,(ox,oy))
    key=fn.replace(".png","")
    draw.text((x+4,y+cell+6), f"{key.split('_')[0]} · {labels.get(key,'')}", fill=(215,220,230), font=font)
out = os.path.join(D,"_BOND_SHEET.png")
canvas.save(out); print(out, canvas.size)
