#!/usr/bin/env python3
# ПАЧКА 2: ещё 14 мультяшно-премиум той-пуделей + AI. Другие позы/ракурсы/настроения. Сочно, мило, hi-end.
import os, re, json, urllib.request, urllib.error, base64, time

env = open(os.path.expanduser("~/.hermes/.env")).read()
m = re.search(r'^OPENROUTER_API_KEY\s*=\s*["\']?([^"\'\n#]+)', env, re.M)
KEY = m.group(1).strip()

OUT = os.path.expanduser("~/poodle/logo/ai3")
os.makedirs(OUT, exist_ok=True)
MODEL = "google/gemini-3-pro-image-preview"

BASE = ("Premium cartoon mascot logo of an adorable toy poodle, modern flat vector illustration, "
        "clean confident linework, polished and high-end like a luxury brand mascot, "
        "cute and sweet but refined and serious, rich vibrant yet tasteful color palette, "
        "subtle AI / tech motif woven in, smooth rounded shapes, perfect symmetry and balance, "
        "centered emblem on a soft dark premium background, professional brand mark, NOT childish, NOT cheap, "
        "luxury kennel for elite toy poodles. ")

prompts = {
  "10_wink_node":      BASE + "Cheeky cute toy poodle winking with one eye, tongue slightly out, a small floating teal AI node sparkle, playful but premium mascot.",
  "11_chip_collar":    BASE + "Toy poodle head with an elegant smart-collar that has a glowing AI gem, deep navy and gold-cream palette, regal and sweet luxury mascot.",
  "12_galaxy_fur":     BASE + "Adorable toy poodle whose fluffy curls subtly contain tiny twinkling stars like a soft galaxy, dreamy premium mascot, teal and violet tasteful tones.",
  "13_3d_glossy":      BASE + "Cute toy poodle mascot in a glossy soft 3D render style, rounded clean shapes, big shiny eyes, a small orbiting AI ring, premium app-icon look.",
  "14_badge_crest":    BASE + "Cute toy poodle face inside a refined modern crest/shield badge with thin circuit detailing, luxury kennel emblem, sweet and prestigious.",
  "15_pixel_heart":    BASE + "Toy poodle mascot holding a small glowing heart icon made of neural nodes between its paws, warm and loving, vibrant premium colors.",
  "16_minimal_curl":   BASE + "Extremely minimal cute toy poodle made almost entirely of three soft fluffy curl shapes and two sweet dot eyes, one tiny teal node, clean iconic emblem.",
  "17_sleeping":       BASE + "Adorable toy poodle curled up sleeping peacefully with a tiny floating zzz that turns into AI nodes, cozy premium pastel-on-dark mascot.",
  "18_proud_sit":      BASE + "Elegant proud toy poodle sitting upright like a show champion, fluffy groomed pompoms, a subtle star of light nodes above, dignified luxury mascot.",
  "19_two_tone":       BASE + "Cute toy poodle mascot head in a bold two-tone duotone style, deep teal and warm cream only, sharp clean shapes, modern premium emblem.",
  "20_line_mono":      BASE + "Single continuous elegant line-art toy poodle face that is sweet and recognizable, one small filled teal AI node for the eye, sophisticated minimal premium mark.",
  "21_emoji_set":      BASE + "A single super cute toy poodle face with a big warm friendly smile, designed like a flagship emoji / sticker, bold clean shapes, one teal AI sparkle, irresistible and premium.",
  "22_constellation":  BASE + "Cute toy poodle silhouette filled softly with a constellation of connected glowing AI star-nodes, the dynasty-of-stars concept, premium and magical yet clean.",
  "23_tech_goggles":   BASE + "Charming toy poodle wearing tiny stylish smart-glasses / AR visor with a faint teal HUD glow, smart and adorable, premium tech mascot, sweet expression.",
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
print(f"\n=== ГОТОВО ПАЧКА 2: {ok}/{len(prompts)} в {OUT} ===")
