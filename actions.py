import webbrowser
import os

def open_website(url):
    try:
        webbrowser.open(url)
        return "Açıyorum Hacım."
    except:
        return "Web sitesini açamadım Hacım."

def open_app(path):
    try:
        os.startfile(path)
        return "Uygulama açıldı Hacım."
    except:
        return "Uygulamayı bulamadım Hacım."
