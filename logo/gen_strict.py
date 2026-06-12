#!/usr/bin/env python3
# СТРОГИЕ AI-tech логотипы. Деловой минимализм, монохром, AI-элементы. БЕЗ золота/короны/блёсток.
import os, re, json, urllib.request, urllib.error, base64, time

env = open(os.path.expanduser("~/.hermes/.env")).read()
m = re.search(r'^OPENROUTER_API_KEY\s*=\s*["\']?([^"\'\n#]+)', env, re.M)
KEY = m.group(1).strip()

OUT = os.path.expanduser("~/poodle/logo/ai2")
os.makedirs(OUT, exist_ok=True)
MODEL = "google/gemini-3-pro-image-preview"

# Общая ДНК: строгий, корпоративный, tech, монохром + один холодный акцент, AI-мотив, много воздуха.
BASE = ("Minimalist corporate tech logo, extremely clean and strict, sophisticated restraint, "
        "monochrome graphite and off-white with a single cool muted accent (steel blue / desaturated teal), "
        "lots of negative space, precise geometry, flat vector, professional brand mark like Palantir, Linear, OpenAI, Anduril, "
        "dark charcoal background, NO gold, NO crown, NO glitter, NO ornate decoration, NO gradients of color, serious and premium, centered. ")

prompts = {
  # 1 — Монограмма-чип (буквы DZ как микросхема / AI)
  "01_mono_chip_a": BASE + "A geometric monogram of letters D and Z constructed from thin circuit-board lines and small nodes, like a silicon chip, an abstract AI mark, strict and architectural.",
  "02_mono_chip_b": BASE + "A single strict letterform monogram inside a precise hexagon, fine connecting node-lines suggesting a neural network, minimal AI tech emblem.",
  # 2 — Звезда из нейросети (наш смысл «звёзды» + AI)
  "03_neural_star_a": BASE + "An abstract star formed by connected neural-network nodes and edges, clean geometric constellation, minimal AI mark, strict symmetry.",
  "04_neural_star_b": BASE + "A minimalist four-point star drawn as a single continuous precise line merging into a circuit trace, subtle node dots, strict tech emblem.",
  # 3 — Пёс через геометрию данных (строгий силуэт)
  "05_geo_dog_a": BASE + "A strict geometric minimal silhouette of a dog head built from clean straight lines and a few node points, suggesting AI/data, architectural mark, not cute, serious and refined.",
  "06_geo_dog_b": BASE + "An ultra-minimal line-only dog profile that doubles as an abstract data-flow path, single weight strokes, strict corporate tech logo.",
  # 4 — Абстрактный AI-знак (без буквальности, premium tech)
  "07_abstract_a": BASE + "An abstract premium AI emblem: a precise orbit ring with a small luminous node, suggesting a guiding star and machine intelligence, strict minimal, architectural.",
  "08_abstract_b": BASE + "A strict minimal emblem of intersecting precise lines forming an implied star at the center where node-dots meet, neural-network feel, corporate AI brand mark.",
  "09_abstract_c": BASE + "A confident minimal wordmark-less symbol: a single elegant geometric glyph combining a star point and a circuit node, perfectly balanced, serious tech-luxury brand mark.",
}

def gen(name, prompt):
    body = json.dumps({"model": MODEL, "messages":[{"role":"user","content":prompt}], "modalities":["image","text"]}).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body, method="POST")
    req.add_header("Authorization", f"Bearer {KEY}"); req.add_header("Content-Type","application/json")
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=240) as r:
                data = json.loads(r.read())
            msg = data["choices"][0]["message"]; imgs = msg.get("images") or []
            if not imgs: print(f"NOIMG {name}"); return False
            b64 = imgs[0]["image_url"]["url"].split(",",1)[1]
            open(os.path.join(OUT,name+".png"),"wb").write(base64.b64decode(b64))
            print(f"OK {name}"); return True
        except urllib.error.HTTPError as e:
            print(f"ERR {name}: {e.code} {e.read()[:120]}")
            if e.code in (429,503): time.sleep(5); continue
            return False
        except Exception as e:
            print(f"ERR {name}: {type(e).__name__} {str(e)[:120]}"); time.sleep(3)
    return False

ok=0
for n,p in prompts.items():
    if gen(n,p): ok+=1
    time.sleep(2)
print(f"\n=== ГОТОВО: {ok}/{len(prompts)} строгих лого в {OUT} ===")
