#!/usr/bin/env python3
# ОБЪЁМ: золотой 3D-эмблема в стиле ТГ-историй питомника. Сочное тиснёное золото, блики, глубина.
import os, re, json, urllib.request, urllib.error, base64, time

env = open(os.path.expanduser("~/.hermes/.env")).read()
m = re.search(r'^OPENROUTER_API_KEY\s*=\s*["\']?([^"\'\n#]+)', env, re.M)
KEY = m.group(1).strip()

OUT = os.path.expanduser("~/poodle/logo/gold3d")
os.makedirs(OUT, exist_ok=True)
MODEL = "openai/gpt-5-image"

# Референс: глянцевое 3D золото с бликами, мягкие тени, premium, тёплый фон. Наша композиция.
BASE = ("Elegant refined logo emblem with a SUBTLE light 3D effect — gentle soft embossing, delicate gold foil sheen, "
        "soft shadows giving just a little depth, NOT heavy, NOT a thick chunky metal sign, keep it tasteful, fine and "
        "sophisticated like premium letterpress / soft gold-foil stamping on luxury paper. Thin elegant line-art kept "
        "intact, only lightly raised. Warm cream-ivory background, soft natural lighting, gentle and classy. "
        "A circular medallion emblem: inside it a graceful human hand on the left reaching toward an elegant toy poodle "
        "head on the right, a small refined 4-point star sparkle where they almost meet, delicate star-constellations "
        "around the rim. Warm soft gold with a gentle luminous quality, lightly dimensional but still delicate and "
        "minimal. Sophisticated, warm, expensive, understated luxury, centered, ultra clean. ")

prompts = {
  "G1_foil":     BASE + "Soft warm gold foil sheen, gentle highlights, light embossing — like elegant gold stamping on cream paper.",
  "G2_champ":    BASE + "Delicate champagne-gold tone, very refined, barely-there soft 3D relief, understated and classy.",
  "G3_warmlit":  BASE + "Warm soft studio light catching the thin gold lines, subtle depth, juicy but tasteful, gentle glow.",
  "G4_softemb":  BASE + "Light tasteful embossed relief on cream, soft shadows, the lines gently raised, delicate premium gold-foil look.",
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
print(f"\n=== ГОТОВО GOLD3D: {ok}/{len(prompts)} в {OUT} ===")
