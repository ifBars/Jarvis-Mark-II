import gettext
import os

LOCALE_DIR = os.path.join(os.path.dirname(__file__), "locales")

def set_language(lang):
    global _
    try:
        translation = gettext.translation("messages", localedir=LOCALE_DIR, languages=[lang])
        translation.install()
        _ = translation.gettext
    except FileNotFoundError:
        print(f"Warning: No translation file found for {lang}, defaulting to English.")
        _ = lambda s: s  # Falls back to original text