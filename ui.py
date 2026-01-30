import tkinter as tk
from actions import open_website
import json

with open("config.json", "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

def start_ui(on_message):
    # Başlangıç sekmelerini aç
    for site in CONFIG.get("default_tabs", []):
        open_website(site)

    # Ana pencere
    window = tk.Tk()
    window.title("JARVIS - Hacım Edition")
    window.geometry("500x550")

    # Chat kutusu
    chat_box = tk.Text(window, state="disabled", wrap="word", bg="#1e1e1e", fg="#ffffff", font=("Arial", 11))
    chat_box.pack(expand=True, fill="both", padx=5, pady=5)

    # Entry ve Send butonu çerçevesi
    input_frame = tk.Frame(window)
    input_frame.pack(fill="x", padx=5, pady=5)

    entry = tk.Entry(input_frame, font=("Arial", 12))
    entry.pack(side="left", fill="x", expand=True, padx=(0,5))

    send_button = tk.Button(input_frame, text="Send", command=lambda: send(), bg="#4CAF50", fg="white", font=("Arial", 11))
    send_button.pack(side="right")

    # Mesaj yazdırma fonksiyonu
    def write(sender, text):
        chat_box.config(state="normal")
        chat_box.insert(tk.END, f"{sender}: {text}\n")
        chat_box.config(state="disabled")
        chat_box.see(tk.END)

    # Gönderme fonksiyonu
    def send():
        text = entry.get()
        if not text.strip():
            return
        entry.delete(0, tk.END)
        write("Hacım", text)
        response = on_message(text)
        write("JARVIS", response)

    # Enter tuşuna basınca da gönder
    entry.bind("<Return>", lambda e: send())

    # Başlangıç mesajı
    write("JARVIS", "Hazırım Hacım. Seni dinliyorum.")

    window.mainloop()
