#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont
D = os.path.expanduser("~/poodle/logo/ai3")
files = sorted([f for f in os.listdir(D) if f.endswith(".png")])
cols, cell, pad, label_h = 5, 360, 16, 34
rows = (len(files)+cols-1)//cols
W = cols*cell + pad*(cols+1)
H = rows*(cell+label_h) + pad*(rows+1)
canvas = Image.new("RGB",(W,H),(18,20,24))
draw = ImageDraw.Draw(canvas)
try: font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
except: font = ImageFont.load_default()
for i,fn in enumerate(files):
    r,c = divmod(i,cols)
    x = pad + c*(cell+pad); y = pad + r*(cell+label_h+pad)
    try:
        im = Image.open(os.path.join(D,fn)).convert("RGB")
        im.thumbnail((cell,cell))
        ox = x+(cell-im.width)//2; oy = y+(cell-im.height)//2
        canvas.paste(im,(ox,oy))
    except Exception as e:
        draw.text((x,y),f"ERR {e}",fill=(255,80,80),font=font)
    draw.text((x+4,y+cell+6), fn.replace(".png",""), fill=(210,215,225), font=font)
out = os.path.join(D,"_CONTACT_SHEET.png")
canvas.save(out)
print(out, canvas.size)
