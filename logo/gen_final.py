#!/usr/bin/env python3
# ФИНАЛ-ВАРИАНТЫ на базе выбранного знака: золотая линия, рука человека тянется к лапе пуделя,
# звезда в точке встречи, созвездия вокруг, профиль пуделя, текст "ИЗ ДИНАСТИИ ЗВЁЗД", круглая рамка.
# Движок GPT-5-Image. Разные фоны/акценты. Каждый отдельно, высокое качество.
import os, re, json, urllib.request, urllib.error, base64, time

env = open(os.path.expanduser("~/.hermes/.env")).read()
m = re.search(r'^OPENROUTER_API_KEY\s*=\s*["\']?([^"\'\n#]+)', env, re.M)
KEY = m.group(1).strip()

OUT = os.path.expanduser("~/poodle/logo/final")
os.makedirs(OUT, exist_ok=True)
MODEL = "openai/gpt-5-image"

# ДНК выбранного знака — описываем точно, чтобы держать преемственность
DNA = ("Elegant luxury emblem logo, fine single-weight GOLD line art, for a high-end toy-poodle kennel. "
       "Composition: a refined human hand reaching toward a toy-poodle paw, a delicate radiant STAR at the point "
       "where they meet (the bond), the graceful profile of a curly toy poodle's head, and small constellations of "
       "fine star-nodes around them (the Dynasty of Stars / a gentle AI network of light). Enclosed in a thin circular "
       "frame. Sophisticated serif lettering 'ИЗ ДИНАСТИИ ЗВЁЗД' in correct Cyrillic with elegant letter-spacing. "
       "Vector-clean, precise, prestigious like Cartier / Hermes / a heraldic kennel crest. Serious, timeless, premium, "
       "perfectly balanced and centered. Correct hand anatomy, correct paw, no extra fingers. ")

prompts = {
  "F1_black_gold":  DNA + "Background: deep rich black. The gold lines glow softly and luxuriously against the darkness. The most premium presentation.",
  "F2_teal_gold":   DNA + "Background: deep desaturated teal / midnight petrol blue. Gold lines elegant against teal, AI-light accent. Refined and modern-luxury.",
  "F3_cream_gold":  DNA + "Background: warm soft cream / ivory. Gold lines crisp and editorial, like an embossed luxury stationery mark. Clean and timeless.",
  "F4_mono_gold":   DNA + "Pure monochrome single-color gold version on charcoal, ultra clean, suitable for foil-stamp / engraving. No other colors.",
  "F5_stronger_dog":DNA + "Background deep black. Emphasis: make the toy-poodle's head profile MORE prominent and beautifully detailed (fluffy curls clearly rendered) while keeping the elegant gold line style. The dog is the hero.",
  "F6_ai_links":    DNA + "Background deep black. Emphasis: add subtle fine connecting lines between the constellation star-nodes and the hand & paw, clearly suggesting a warm AI network of light linking human and dog. Tech-as-light, still elegant.",
  "F7_icon_only":   ("Elegant luxury ICON only (NO text), fine gold line art on deep black: a human hand reaching to a toy-poodle paw with a radiant star at the meeting point and the profile of a curly toy poodle, small constellation nodes, thin circular frame. Vector-clean, premium, balanced, suitable as a round app avatar. Correct anatomy."),
  "F8_horizontal":  ("Elegant luxury HORIZONTAL lockup logo, fine gold line art on deep black: on the LEFT a compact round emblem (human hand reaching a toy-poodle paw, radiant star, curly poodle profile, constellation nodes, thin circular frame); on the RIGHT the wordmark 'ИЗ ДИНАСТИИ ЗВЁЗД' in elegant Cyrillic serif, with a small line 'питомник той-пуделей' beneath. Premium banner/header lockup, balanced, vector-clean."),
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
print(f"\n=== ГОТОВО FINAL: {ok}/{len(prompts)} в {OUT} ===")
