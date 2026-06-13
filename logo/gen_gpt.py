#!/usr/bin/env python3
# ДВИЖОК 2: OpenAI GPT-5-Image (через OpenRouter). Мультяшно-премиум той-пудель + AI. Чистая геометрия лого.
import os, re, json, urllib.request, urllib.error, base64, time

env = open(os.path.expanduser("~/.hermes/.env")).read()
m = re.search(r'^OPENROUTER_API_KEY\s*=\s*["\']?([^"\'\n#]+)', env, re.M)
KEY = m.group(1).strip()

OUT = os.path.expanduser("~/poodle/logo/gpt")
os.makedirs(OUT, exist_ok=True)
MODEL = "openai/gpt-5-image"

BASE = ("Professional logo design, premium cartoon mascot of an adorable toy poodle for a luxury dog kennel "
        "named 'Из Династии Звёзд' (Dynasty of Stars). Clean modern flat vector style, polished and high-end, "
        "cute and sweet but refined and serious, NOT childish, NOT cheap. Rich tasteful colors: deep teal, warm "
        "cream, soft charcoal, one elegant accent. Subtle AI / tech motif woven in (fine glowing nodes, a neural "
        "constellation, a circuit ring). Perfectly balanced centered emblem, crisp clean shapes, vector logo quality "
        "with sharp edges, soft dark premium background. ")

prompts = {
  "g01_head_ring":   BASE + "A cute fluffy toy poodle face mascot, big sweet eyes, gentle smile, framed by a thin glowing teal AI orbit ring of small nodes. Iconic balanced emblem.",
  "g02_star_crown":  BASE + "A sweet toy poodle head whose curls are crowned by a delicate constellation of glowing AI star-nodes, regal yet adorable — the Dynasty-of-Stars idea.",
  "g03_full_proud":  BASE + "A full-body elegant toy poodle sitting proudly like a champion, fluffy groomed pompoms, a small glowing neural star above its head. Dignified luxury mascot.",
  "g04_heart_ai":    BASE + "An adorable toy poodle face beside a small glowing heart formed from neural-network nodes. Warm, loving, premium.",
  "g05_paw_chip":    BASE + "A cute toy poodle raising one fluffy paw, the paw pad subtly drawn as a tiny circuit / AI chip. Sweet and clever.",
  "g06_icon_min":    BASE + "An ultra-clean minimal cute toy poodle face icon for an app avatar, bold simple shapes, one subtle teal AI node accent, lots of negative space. Instantly recognizable.",
  "g07_badge":       BASE + "A cute toy poodle face inside a refined modern crest / shield badge with thin circuit detailing. Prestigious luxury kennel emblem.",
  "g08_duotone":     BASE + "A cute toy poodle mascot head in a bold two-tone duotone style, deep teal and warm cream only, sharp clean modern shapes, one tiny AI node.",
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
            if not imgs:
                print(f"NOIMG {name}: {str(msg.get('content'))[:120]}"); return False
            b64 = imgs[0]["image_url"]["url"].split(",",1)[1]
            open(os.path.join(OUT,name+".png"),"wb").write(base64.b64decode(b64))
            print(f"OK {name}"); return True
        except urllib.error.HTTPError as e:
            print(f"ERR {name}: {e.code} {e.read()[:160]}")
            if e.code in (429,503): time.sleep(5); continue
            return False
        except Exception as e:
            print(f"ERR {name}: {type(e).__name__} {str(e)[:120]}"); time.sleep(3)
    return False

ok=0
for n,p in prompts.items():
    if gen(n,p): ok+=1
    time.sleep(2)
print(f"\n=== ГОТОВО GPT-5-IMAGE: {ok}/{len(prompts)} в {OUT} ===")
