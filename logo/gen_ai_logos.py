#!/usr/bin/env python3
# Генерация логотипов через FAL (flux). 4 направления, по 2 исполнения = 8 AI-логотипов.
import os, re, json, urllib.request, urllib.error, time, sys

env = open(os.path.expanduser("~/.hermes/.env")).read()
m = re.search(r'FAL_KEY\s*=\s*["\']?([^"\'\n]+)', env)
FAL = m.group(1).strip()

OUT = os.path.expanduser("~/poodle/logo/ai")
os.makedirs(OUT, exist_ok=True)

# 4 направления × подвиды. Текст в промптах НЕ просим (AI коверкает кириллицу) — чистые эмблемы/иконки.
prompts = {
  "01_minimal_lux_a": "Luxury minimalist logo emblem for an elite dog kennel, single elegant gold star mark on deep black background, ultra clean, jewelry brand aesthetic like Chanel, vector style, centered, premium, sophisticated, no text",
  "02_minimal_lux_b": "Minimalist gold line-art crown above a small star, luxury monogram emblem, deep dark navy background, refined thin gold lines, high-end fashion brand mark, centered, elegant, no text",
  "03_emotion_poodle_a": "Elegant logo of a cute toy poodle head silhouette in gold, soft premium style, dark emerald background, warm luxury pet brand, refined and adorable, centered emblem, no text",
  "04_emotion_poodle_b": "Premium emblem of a fluffy white maltipoo puppy face, gold accents, dark luxury background, heartwarming high-end pet boutique logo, soft glow, centered, no text",
  "05_heraldry_a": "Royal heraldic crest emblem for a luxury dog dynasty, gold crown and laurel and star, dark background, coat of arms style, regal premium, intricate gold, centered, no text",
  "06_heraldry_b": "Luxury wax seal stamp emblem in gold, ornate circular crest with a star in center, dark background, royal dynasty mark, embossed, centered, no text",
  "07_surprise_a": "Constellation of stars forming an abstract dog shape, gold dots connected by thin lines, deep night-sky dark background, magical premium pet brand emblem, centered, no text",
  "08_surprise_b": "Art-deco luxury emblem combining a star and a stylized dog, gold and teal accents, geometric, dark background, modern premium monogram, centered, no text",
}

def gen(name, prompt):
    url = "https://fal.run/fal-ai/flux/dev"
    payload = json.dumps({"prompt": prompt, "image_size":"square_hd", "num_images":1, "num_inference_steps":28}).encode()
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Authorization", f"Key {FAL}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            data = json.loads(r.read())
        img_url = data["images"][0]["url"]
        # скачать
        dst = os.path.join(OUT, name + ".png")
        urllib.request.urlretrieve(img_url, dst)
        print(f"OK {name} -> {dst}")
        return True
    except urllib.error.HTTPError as e:
        print(f"ERR {name}: HTTP {e.code} {e.read()[:200]}")
    except Exception as e:
        print(f"ERR {name}: {type(e).__name__} {str(e)[:150]}")
    return False

ok=0
for name, p in prompts.items():
    if gen(name, p): ok+=1
    time.sleep(1)
print(f"\nГотово: {ok}/{len(prompts)} логотипов в {OUT}")
