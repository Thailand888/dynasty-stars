#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont
D = os.path.expanduser("~/poodle/logo/final2")
files = sorted([f for f in os.listdir(D) if f.endswith(".png") and not f.startswith("_")])
cols, cell, pad, label_h = 3, 540, 18, 40
rows = (len(files)+cols-1)//cols
W = cols*cell + pad*(cols+1)
H = rows*(cell+label_h) + pad*(rows+1) + 50
canvas = Image.new("RGB",(W,H),(30,30,32))
draw = ImageDraw.Draw(canvas)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 24)
    big = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 30)
except:
    font = ImageFont.load_default(); big = font
draw.text((pad,12), "FINAL2 — проверка текста и чистоты линий", fill=(230,230,235), font=big)
for i,fn in enumerate(files):
    r,c = divmod(i,cols)
    x = pad + c*(cell+pad); y = 50 + pad + r*(cell+label_h+pad)
    im = Image.open(os.path.join(D,fn)).convert("RGB"); im.thumbnail((cell,cell))
    ox = x+(cell-im.width)//2; oy = y+(cell-im.height)//2
    canvas.paste(im,(ox,oy))
    draw.text((x+4,y+cell+8), fn.replace(".png",""), fill=(220,220,225), font=font)
out = os.path.join(D,"_FINAL2_SHEET.png")
canvas.save(out); print(out, canvas.size)
