#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont
D = os.path.expanduser("~/poodle/logo/ai3")
# Топ-отбор Бобби: сочные, милые, дорогие, с AI
top = [
 ("02_mascot_head_b","Пушистая мордочка в AI-кольце"),
 ("06_poodle_star_b","Созвездие-корона + лента"),
 ("14_badge_crest","Золотой щенок, бабочка, плата"),
 ("08_heart_ai_b","Пудель + AI-сердце, золото"),
 ("07_paw_ai_a","Лапка вверх + AI-кулон"),
 ("18_proud_sit","Гордый чемпион, корона звёзд"),
 ("13_3d_glossy","Монограмма-кольцо, tech"),
 ("12_galaxy_fur","Галактика в шерсти"),
]
cols, cell, pad, label_h = 4, 440, 18, 40
rows = (len(top)+cols-1)//cols
W = cols*cell + pad*(cols+1)
H = rows*(cell+label_h) + pad*(rows+1) + 60
canvas = Image.new("RGB",(W,H),(15,17,21))
draw = ImageDraw.Draw(canvas)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 22)
    big = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 34)
except:
    font = ImageFont.load_default(); big = font
draw.text((pad, 14), "ИЗ ДИНАСТИИ ЗВЁЗД  —  ТОП-8 (мультяшно-премиум + AI)", fill=(240,210,140), font=big)
for i,(fn,desc) in enumerate(top):
    r,c = divmod(i,cols)
    x = pad + c*(cell+pad); y = 60 + pad + r*(cell+label_h+pad)
    im = Image.open(os.path.join(D,fn+".png")).convert("RGB"); im.thumbnail((cell,cell))
    ox = x+(cell-im.width)//2; oy = y+(cell-im.height)//2
    canvas.paste(im,(ox,oy))
    draw.text((x+4,y+cell+6), f"{fn.split('_')[0]} · {desc}", fill=(215,220,230), font=font)
out = os.path.join(D,"_TOP8.png")
canvas.save(out); print(out, canvas.size)
