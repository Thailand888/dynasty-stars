#!/usr/bin/env python3
# КОНЦЕПЦИЯ: связь человек+собака + AI как тёплый свет, осветляющий жизнь. Движок GPT-5-Image.
import os, re, json, urllib.request, urllib.error, base64, time

env = open(os.path.expanduser("~/.hermes/.env")).read()
m = re.search(r'^OPENROUTER_API_KEY\s*=\s*["\']?([^"\'\n#]+)', env, re.M)
KEY = m.group(1).strip()

OUT = os.path.expanduser("~/poodle/logo/bond")
os.makedirs(OUT, exist_ok=True)
MODEL = "openai/gpt-5-image"

BASE = ("Professional premium logo design for a luxury toy-poodle kennel named 'Из Династии Звёзд' (Dynasty of Stars). "
        "The core idea: the bond and love between a human and their dog, a warm community of dog owners, and how new AI "
        "technology brings warmth and light into this caring world, brightening human life. Clean modern flat vector "
        "style, polished and high-end, warm and emotional but refined and serious, NOT childish, NOT cheap. "
        "Warm palette: soft glowing teal and warm golden light, cream, gentle charcoal. The AI is shown as a WARM glow / "
        "a gentle constellation of light-nodes / a soft luminous star — light that brightens life, not cold tech. "
        "Perfectly balanced centered emblem, crisp clean vector shapes, soft dark premium background. ")

prompts = {
  # Связь человек+собака через свет AI
  "b01_hand_paw":   BASE + "A human hand and a fluffy toy-poodle paw gently reaching toward each other, and between them a warm glowing star made of soft AI light-nodes — the bond illuminated by technology. Elegant minimal emblem, like the touch in Creation of Adam but tender and modern.",
  "b02_hand_paw_heart": BASE + "A human hand and a dog paw forming the two halves of a heart, with a gentle constellation of warm AI light-nodes glowing inside the heart. Love between human and dog amplified by technology.",
  # Человек и пудель под общей звездой
  "b03_silhouette_star": BASE + "Warm silhouette of a person and an elegant toy poodle standing together side by side, looking up at a shared glowing star-constellation of AI light above them that bathes them in warm light. Emotional, premium, the dog brightening the owner's life.",
  "b04_embrace": BASE + "A gentle scene of a person tenderly holding a cute toy poodle, a soft halo of warm AI light-nodes glowing around them like a guardian star. Loving bond, premium mascot emblem.",
  # Сообщество владельцев — круг/орбита вокруг AI-света
  "b05_community_orbit": BASE + "A circular emblem: small simplified figures of people and toy poodles arranged around a central warm glowing AI star-core, like a family/dynasty orbiting a guiding light. A community of dog lovers united, premium and warm.",
  # Сердце руки+лапы+узлов
  "b06_glow_paw_hand": BASE + "A soft open human palm cradling a glowing toy-poodle paw print, warm radiant light and tiny AI nodes emanating outward, symbolizing care and technology brightening life. Tender premium emblem.",
  # Пудель как источник света для человека
  "b07_poodle_light": BASE + "A cute toy poodle whose heart glows with a warm AI light that radiates gently toward a human silhouette, lighting up their face with a soft smile. The dog and AI brighten human life. Emotional premium logo.",
  # Минимал-знак: лапа + рука сливаются в звезду
  "b08_paw_hand_star": BASE + "An ultra-clean minimal mark where a human hand line and a dog paw line merge upward into a single warm glowing star formed of AI nodes. Sophisticated, symbolic, premium, usable as an icon.",
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
print(f"\n=== ГОТОВО BOND: {ok}/{len(prompts)} в {OUT} ===")
