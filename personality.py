import os
import json

def load_personality(personality_name, lang="en"):
    personality_file = os.path.join("personalities", f"{personality_name}.json")
    try:
        with open(personality_file, "r", encoding="utf8") as f:
            print(_("Loading personality: {personality}").format(personality=personality_name))
            personality_data = json.load(f)
        return personality_data.get(lang, personality_data.get("en"))
    except FileNotFoundError:
        print(_("Warning: Personality '{personality}' not found. Falling back to 'jarvis'.").format(personality=personality_name))
        fallback_file = os.path.join("personalities", "jarvis.json")
        with open(fallback_file, "r", encoding="utf8") as f:
            personality_data = json.load(f)
        return personality_data.get(lang, personality_data.get("en"))