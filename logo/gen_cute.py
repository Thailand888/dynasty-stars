#!/usr/bin/env python3
# МУЛЬТЯШНО-ПРЕМИУМ той-пудель + AI. Сочно, красочно, мило, но строго и hi-end (не детсад).
import os, re, json, urllib.request, urllib.error, base64, time

env = open(os.path.expanduser("~/.hermes/.env")).read()
m = re.search(r'^OPENROUTER_API_KEY\s*=\s*["\']?([^"\'\n#]+)', env, re.M)
KEY = m.group(1).strip()

OUT = os.path.expanduser("~/poodle/logo/ai3")
os.makedirs(OUT, exist_ok=True)
MODEL = "google/gemini-3-pro-image-preview"

# ДНК: премиум-мультяшный мэскот, чистый вектор, сочные но благородные цвета, мило+дорого, AI-мотив, строгая композиция.
BASE = ("Premium cartoon mascot logo of an adorable toy poodle, modern flat vector illustration, "
        "clean confident linework, polished and high-end like a luxury brand mascot (think premium app icon, "
        "Duolingo/Pixar level of polish but more sophisticated and upscale), cute and sweet but refined and serious, "
        "rich vibrant yet tasteful color palette, deep teal and warm cream with a single elegant accent, "
        "subtle AI / tech motif woven in, smooth rounded shapes, perfect symmetry and balance, "
        "centered emblem on a soft dark premium background, professional brand mark, NOT childish, NOT cheap, "
        "luxury kennel for elite toy poodles. ")

prompts = {
  # 1 — Милый мэскот-голова той-пуделя + AI-нимб
  "01_mascot_head_a": BASE + "Cute toy poodle face mascot, fluffy curly ears, big sweet sparkling eyes, gentle smile, a thin glowing teal AI orbit ring / halo of small nodes around the head suggesting intelligence, mascot logo, adorable yet premium.",
  "02_mascot_head_b": BASE + "Charming toy poodle head facing forward, soft fluffy pompom curls, kind expressive eyes, sitting inside a clean circular badge with subtle circuit-line decoration, luxury mascot emblem, sweet and high-end.",
  # 2 — Той-пудель в полный рост, элегантный, с AI-звездой
  "03_full_poodle_a": BASE + "Full-body cute toy poodle standing elegantly and proudly, fluffy pompom tail and paws, a small glowing star with neural nodes above its head, graceful luxury mascot, sweet but dignified posture.",
  "04_full_poodle_b": BASE + "Adorable seated toy poodle mascot with a tiny elegant collar that glows like a smart AI device, curly fluffy coat, big charming eyes, premium playful luxury brand character.",
  # 3 — Пудель + звезда (наш смысл «Династия Звёзд»)
  "05_poodle_star_a": BASE + "Cute toy poodle cuddling or reaching toward a soft glowing star made of tiny AI nodes, warm sweet emotional scene, premium mascot logo, the star and dog form a balanced emblem.",
  "06_poodle_star_b": BASE + "Toy poodle mascot head where a sparkling AI constellation-star sits like a tiara crown of light nodes, sweet regal and adorable, luxury but cute, clean vector emblem.",
  # 4 — Голова + сердце/лапа из нейросети (милота + AI)
  "07_paw_ai_a": BASE + "Cute toy poodle peeking with a fluffy paw raised, the paw pad subtly drawn as a tiny circuit / AI chip pattern, sweet and clever, premium mascot mark.",
  "08_heart_ai_b": BASE + "Adorable toy poodle face with a small glowing heart made of neural-network nodes floating beside it, warm loving premium mascot, vibrant tasteful colors.",
  # 5 — Иконка-эмодзи стиль, очень чистая, для аватара
  "09_icon_clean": BASE + "Ultra-clean minimal cute toy poodle face icon, perfect for an app avatar, simple bold shapes, one subtle teal AI node accent, instantly recognizable, sweet premium emblem, lots of negative space.",
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
print(f"\n=== ГОТОВО: {ok}/{len(prompts)} мультяшно-премиум лого в {OUT} ===")
