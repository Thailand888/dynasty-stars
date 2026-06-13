#!/usr/bin/env python3
# ЛЮКС-УРОВЕНЬ. Серьёзный знак: минимализм, монограмма, геральдика, золото/тёмное. НЕ мультик.
# Связь человек+собака + AI через изящный символ. Движок GPT-5-Image. Высокое качество, по одному.
import os, re, json, urllib.request, urllib.error, base64, time

env = open(os.path.expanduser("~/.hermes/.env")).read()
m = re.search(r'^OPENROUTER_API_KEY\s*=\s*["\']?([^"\'\n#]+)', env, re.M)
KEY = m.group(1).strip()

OUT = os.path.expanduser("~/poodle/logo/lux")
os.makedirs(OUT, exist_ok=True)
MODEL = "openai/gpt-5-image"

BASE = ("Ultra high-end luxury logo design, sophisticated and serious, for an elite toy-poodle kennel "
        "'Из Династии Звёзд' (Dynasty of Stars). Think the prestige of Cartier, Hermes, a Swiss watch maison, "
        "a heraldic European breeder house — refined, minimal, expensive, timeless. ABSOLUTELY NOT cartoon, "
        "NOT a mascot, NOT cute, NOT childish, NOT playful. Elegant restraint, fine thin precise linework, "
        "deep premium palette: matte black / midnight charcoal background with refined gold and subtle "
        "platinum-teal accent. The mark subtly expresses the noble bond between human and dog, and AI as a "
        "discreet refined light/constellation woven into the geometry. Perfect symmetry, generous negative space, "
        "vector-crisp, museum-grade brand mark, centered, high resolution. ")

prompts = {
  "L01_crest":      BASE + "A refined heraldic emblem: an elegant elongated poodle silhouette in noble profile within a thin gold ring, a single subtle star above, fine engraved detailing. Aristocratic, serious, timeless luxury crest.",
  "L02_monogram":   BASE + "A sophisticated gold monogram of the letters 'ДЗ' elegantly intertwined, with one fine poodle-curl flourish and a tiny constellation accent, like a luxury fashion house monogram. Minimal, expensive, serious.",
  "L03_line_bond":  BASE + "A single continuous fine gold line forming a graceful poodle silhouette that elegantly connects to a human hand, a small refined star where they meet. Minimal luxury line-art mark, the human-dog bond as one elegant stroke.",
  "L04_star_poodle":BASE + "An elegant standing toy poodle rendered in fine gold line on black, crowned by a discreet refined constellation of small stars, framed in a slim circular frame. Noble, prestigious, like a champion seal.",
  "L05_seal":       BASE + "A luxury wax-seal style round emblem in gold on deep black: a noble poodle head in elegant minimal engraving, encircled by fine text and a delicate star, a refined AI node-line woven subtly into the border.",
  "L06_shield":     BASE + "A minimal aristocratic shield/crest with a single elegant poodle head and a guiding star above, very fine gold linework, restrained and serious, heraldic luxury house mark.",
  "L07_constellation": BASE + "A refined emblem where an elegant poodle profile is drawn from connected fine gold star-points (a constellation), expressing the Dynasty of Stars and discreet AI, sophisticated and minimal on black.",
  "L08_hand_paw_lux": BASE + "An exquisite minimal gold mark: a refined human hand and an elegant poodle paw meeting to form a subtle star of light between them, expressing the noble bond elevated by refined technology. Luxury, serious, timeless.",
}

def gen(name, prompt):
    body = json.dumps({"model": MODEL, "messages":[{"role":"user","content":prompt}], "modalities":["image","text"]}).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body, method="POST")
    req.add_header("Authorization", f"Bearer {KEY}"); req.add_header("Content-Type","application/json")
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
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
print(f"\n=== ГОТОВО LUX: {ok}/{len(prompts)} в {OUT} ===")
