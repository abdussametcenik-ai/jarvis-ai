import json
import re
import webbrowser

MEMORY_FILE = "memory.json"
RESPONSES_FILE = "responses.json"
CONFIG_FILE = "config.json"

# Yüklemeler
def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default

MEMORY = load_json(MEMORY_FILE, {})
RESPONSES = load_json(RESPONSES_FILE, {})
CONFIG = load_json(CONFIG_FILE, {"commands": {}})

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def think(text):
    raw = text.strip()
    t = raw.lower()

    # 1️⃣ Öğretilmiş cevaplar
    if t in RESPONSES:
        return RESPONSES[t]

    # 2️⃣ KOMUTLAR (AÇ)
    for cmd, url in CONFIG.get("commands", {}).items():
        if t == cmd:
            webbrowser.open(url)
            return f"{cmd.replace(' aç','').title()} açıyorum Hacım 🚀"

    # 3️⃣ Öğretme modu
    if MEMORY.get("learning"):
        key = MEMORY["learning"]
        RESPONSES[key] = raw
        save_json(RESPONSES_FILE, RESPONSES)
        MEMORY["learning"] = None
        save_json(MEMORY_FILE, MEMORY)
        return "Tamam Hacım, bunu öğrendim ✅"

    # 4️⃣ Sabit sohbet
    if t in ["selam", "merhaba"]:
        return "Selam Hacım 👋"

    if t in ["naber", "ne haber"]:
        return "İyidir Hacım, senden naber?"

    if t == "nasılsın":
        return "İyiyim Hacım, sen nasılsın?"

    if t in ["bende iyiyim", "ben de iyiyim"]:
        return "Buna sevindim Hacım 😎"

    # 5️⃣ Kimlik
    if "benim adım ne" in t:
        return f"Adın {MEMORY.get('name','(bilinmiyor)')} Hacım."

    if "ben kimim" in t:
        return f"Sen {MEMORY.get('name','bir efsanesin')} Hacım."

    if t.startswith("benim adım"):
        name = raw[len("benim adım"):].replace("kaydet", "").strip()
        if name:
            MEMORY["name"] = name.title()
            save_json(MEMORY_FILE, MEMORY)
            return f"Tamam Hacım, adını {MEMORY['name']} olarak kaydettim."

    # 6️⃣ Matematik
    if re.search(r"\d", t):
        expr = re.findall(r"[\d\+\-\*/\s]+", t)
        if expr:
            try:
                return f"Hesapladım Hacım: {eval(expr[0])}"
            except:
                pass

    # 7️⃣ Öğrenme teklif et (EN SON)
    MEMORY["learning"] = t
    save_json(MEMORY_FILE, MEMORY)
    return "Buna nasıl cevap vereyim Hacım?"
