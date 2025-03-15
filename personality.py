import os
import json
from config import SOUNDS_DIR, ULTRON_STARTUP
import pygame

def load_personality(personality_name, lang="en"):
    personality_file = os.path.join("personalities", f"{personality_name}.json")
    try:
        with open(personality_file, "r", encoding="utf8") as f:
            print(_("Loading personality: {personality}").format(personality=personality_name))
            personality_data = json.load(f)
            if personality_name.lower() == "ultron" and ULTRON_STARTUP:
                sound_path = os.path.join(SOUNDS_DIR, "ultron.mp3")
                if os.path.exists(sound_path):
                    pygame.mixer.Sound(sound_path).play()
        return personality_data.get(lang, personality_data.get("en"))
    except FileNotFoundError:
        print(_("Warning: Personality '{personality}' not found. Falling back to 'jarvis'.").format(personality=personality_name))
        fallback_file = os.path.join("personalities", "jarvis.json")
        with open(fallback_file, "r", encoding="utf8") as f:
            personality_data = json.load(f)
        return personality_data.get(lang, personality_data.get("en"))