#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont
D = os.path.expanduser("~/poodle/logo/final")
files = sorted([f for f in os.listdir(D) if f.endswith(".png") and not f.startswith("_")])
cols, cell, pad, label_h = 4, 420, 16, 36
rows = (len(files)+cols-1)//cols
W = cols*cell + pad*(cols+1)
H = rows*(cell+label_h) + pad*(rows+1) + 50
canvas = Image.new("RGB",(W,H),(12,12,14))
draw = ImageDraw.Draw(canvas)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 22)
    big = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 30)
except:
    font = ImageFont.load_default(); big = font
draw.text((pad,12), "FINAL — варианты фаворита (рука+лапа+созвездие)", fill=(220,180,110), font=big)
labels = {
 "F1_black_gold":"Чёрный фон, золото",
 "F2_teal_gold":"Бирюза/петроль + золото",
 "F3_cream_gold":"Кремовый, тиснение",
 "F4_mono_gold":"Моно-золото / фольга",
 "F5_stronger_dog":"Усиленный пудель",
 "F6_ai_links":"AI-связи (линии звёзд)",
 "F7_icon_only":"Иконка без текста",
 "F8_horizontal":"Горизонталь / шапка",
}
for i,fn in enumerate(files):
    r,c = divmod(i,cols)
    x = pad + c*(cell+pad); y = 50 + pad + r*(cell+label_h+pad)
    im = Image.open(os.path.join(D,fn)).convert("RGB"); im.thumbnail((cell,cell))
    ox = x+(cell-im.width)//2; oy = y+(cell-im.height)//2
    canvas.paste(im,(ox,oy))
    key=fn.replace(".png","")
    draw.text((x+4,y+cell+6), f"{key.split('_')[0]} · {labels.get(key,'')}", fill=(210,210,215), font=font)
out = os.path.join(D,"_FINAL_SHEET.png")
canvas.save(out); print(out, canvas.size)
