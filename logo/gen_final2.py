#!/usr/bin/env python3
# ФИНАЛ v2: чистая композиция (как F3), БЕЗ пересвета/glow, резкие тонкие линии, ПРАВИЛЬНЫЙ текст.
import os, re, json, urllib.request, urllib.error, base64, time

env = open(os.path.expanduser("~/.hermes/.env")).read()
m = re.search(r'^OPENROUTER_API_KEY\s*=\s*["\']?([^"\'\n#]+)', env, re.M)
KEY = m.group(1).strip()

OUT = os.path.expanduser("~/poodle/logo/final2")
os.makedirs(OUT, exist_ok=True)
MODEL = "openai/gpt-5-image"

# Жёстко: тонкая чёткая линия, НИКАКОГО glow/свечения/тумана, плоско, как гравюра/эмблема. Текст точный.
BASE = ("Elegant luxury emblem logo for a high-end toy-poodle kennel. Fine thin clean line-art engraving style, "
        "like a prestigious crest / Cartier seal / heraldic monogram. CRISP SHARP THIN LINES, flat, NO glow, NO blur, "
        "NO haze, NO soft light bloom, high contrast, precise and legible. Inside a clean circular frame: on the left a "
        "graceful human hand reaching toward an elegant toy poodle head on the right (like the touch in Creation of Adam), "
        "a small refined star where they almost meet, delicate constellation dots and lines around the rim. "
        "Below the circle, in a refined serif typeface with wide letter spacing, the EXACT Cyrillic text spelled "
        "letter by letter: И-З  Д-И-Н-А-С-Т-И-И  З-В-Ё-З-Д  (\"ИЗ ДИНАСТИИ ЗВЁЗД\"), spelled correctly, do not omit any letter. "
        "Sophisticated, serious, timeless, expensive, minimal. ")

prompts = {
  "v1_black":   BASE + "Gold thin lines on a deep solid black background, crisp and luminous but with sharp edges (no blur).",
  "v2_cream":   BASE + "Dark charcoal-gold thin lines on a warm cream / ivory background, like fine letterpress engraving.",
  "v3_white":   BASE + "Elegant dark gold thin lines on a pure clean white background, minimal and premium.",
  "v4_navy":    BASE + "Soft gold thin lines on a deep midnight navy background, refined and serious.",
  "v5_emerald": BASE + "Gold thin lines on a deep emerald / forest green background, jewelry-box luxury feel.",
  "v6_icon":    "Elegant luxury emblem icon for a toy-poodle kennel, fine thin clean gold line-art on deep black, NO glow NO blur sharp edges, a circular crest with a human hand reaching toward an elegant toy poodle head, a small star between them, delicate constellation dots around the rim. NO TEXT at all, just the symbol, perfectly centered, premium app-icon quality.",
}

def gen(name, prompt):
    body = json.dumps({"model": MODEL, "messages":[{"role":"user","content":prompt}], "modalities":["image","text"]}).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body, method="POST")
    req.add_header("Authorization", f"Bearer {KEY}"); req.add_header("Content-Type","application/json")
    for attempt in range(3):
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
            print(f"ERR {name}: {type(e).__name__} {str(e)[:120]}"); time.sleep(4)
    return False

ok=0
for n,p in prompts.items():
    if gen(n,p): ok+=1
    time.sleep(2)
print(f"\n=== ГОТОВО FINAL2: {ok}/{len(prompts)} в {OUT} ===")
