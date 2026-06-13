#!/usr/bin/env python3
# Генерация логотипов через OpenRouter — ЛУЧШАЯ модель Gemini 3 Pro Image (Nano Banana Pro).
# 10 эмблем: 4 направления, несколько исполнений в каждом.
import os, re, json, urllib.request, urllib.error, base64, time

env = open(os.path.expanduser("~/.hermes/.env")).read()
m = re.search(r'^OPENROUTER_API_KEY\s*=\s*["\']?([^"\'\n#]+)', env, re.M)
KEY = m.group(1).strip()

OUT = os.path.expanduser("~/poodle/logo/ai")
os.makedirs(OUT, exist_ok=True)

MODEL = "google/gemini-3-pro-image-preview"

prompts = {
  # === Направление 1: Минимал-люкс (Chanel/ювелирка) ===
  "01_minimal_a": "A luxury minimalist logo emblem for an elite premium dog kennel named 'Dynasty of Stars'. A single elegant faceted gold star mark like a cut diamond, jewelry-brand aesthetic of Cartier and Chanel, deep matte black background, ultra clean negative space, perfectly centered, sophisticated high-end, professional vector-style logo.",
  "02_minimal_b": "An ultra minimalist luxury monogram emblem: a thin gold line crown above a small radiant star, deep dark navy background, refined elegant gold linework, haute couture brand mark, lots of negative space, centered, professional logo.",
  # === Направление 2: Эмоция (милый пудель, тёплый премиум) ===
  "03_poodle_a": "An elegant luxury logo emblem of a cute toy poodle head silhouette rendered in polished gold, soft premium style, dark emerald green gradient background, warm adorable high-end pet brand, refined and clean, centered, professional logo.",
  "04_poodle_b": "A premium minimalist logo of a fluffy white maltipoo puppy face, delicate gold linework accents, dark luxury background with soft golden glow, heartwarming high-end pet boutique brand mark, centered, professional logo.",
  "05_poodle_c": "A sophisticated gold line-art emblem of a sitting toy poodle in profile beneath a single star, luxury pet dynasty logo, deep black background, elegant thin gold lines, centered, professional vector logo.",
  # === Направление 3: Геральдика (герб, корона, печать) ===
  "06_heraldry_a": "A royal heraldic crest emblem for a luxury dog dynasty, ornate gold crown with laurel wreath and a crowning star, dark background, regal coat of arms, intricate gold detailing, symmetrical, centered, professional logo.",
  "07_heraldry_b": "A luxury gold wax-seal stamp emblem, ornate circular crest with a radiant star in the center surrounded by fine filigree, dark background, royal dynasty embossed seal, centered, professional logo.",
  # === Направление 4: Удиви (намешать стили) ===
  "08_surprise_a": "A constellation of gold stars connected by delicate thin lines forming an elegant abstract dog silhouette, deep night-sky dark background with subtle teal nebula, magical premium pet brand emblem, centered, professional logo.",
  "09_surprise_b": "An art-deco luxury emblem fusing a faceted star and a stylized elegant poodle, symmetrical gold geometry with teal accents, dark background, modern premium monogram, centered, professional logo.",
  "10_surprise_c": "A premium circular badge emblem: a regal poodle head inside a golden ring of stars, deep dark background, gold and subtle teal, luxury pet dynasty crest fusing heraldry and modern minimalism, centered, professional logo.",
}

def gen(name, prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role":"user","content": prompt}],
        "modalities": ["image","text"]
    }).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {KEY}")
    req.add_header("Content-Type", "application/json")
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=240) as r:
                data = json.loads(r.read())
            msg = data["choices"][0]["message"]
            imgs = msg.get("images") or []
            if not imgs:
                print(f"NOIMG {name}: {str(msg)[:140]}"); return False
            durl = imgs[0]["image_url"]["url"]
            b64 = durl.split(",",1)[1]
            open(os.path.join(OUT, name + ".png"),"wb").write(base64.b64decode(b64))
            print(f"OK {name}")
            return True
        except urllib.error.HTTPError as e:
            print(f"ERR {name}: HTTP {e.code} {e.read()[:160]}")
            if e.code in (429,503): time.sleep(5); continue
            return False
        except Exception as e:
            print(f"ERR {name}: {type(e).__name__} {str(e)[:140]}"); time.sleep(3)
    return False

ok=0
for name,p in prompts.items():
    if gen(name,p): ok+=1
    time.sleep(2)
print(f"\n=== ГОТОВО: {ok}/{len(prompts)} логотипов в {OUT} ===")
