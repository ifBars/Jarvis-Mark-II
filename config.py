import os
import sys
import configparser
import google.generativeai as genai
from localization import set_language
from pathlib import Path

def update_language(lang):
    """Update the language setting in the config file."""
    config.set("Settings", "language", lang)
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)
    print(_("Language updated to {lang}. Restart the application to apply changes.").format(lang=lang))
    
def update_personality(new_personality):
    """Update the personality setting in the config file."""
    config.set("General", "personality", new_personality)
    with open(config_file, "w") as configfile:
        config.write(configfile)
    print(_("Personality updated to {personality}. Restarting the application.").format(personality=new_personality))

default_config = {
    'General': {
        'language': 'en',
        'base_dir': r'C:\Jarvis-Mark-II',
        'api_key': 'your_api_key',
        'voice_key': r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enGB_GeorgeM',
        'personality': 'jarvis',
        'interrupt_jarvis': 'true'
    },
    'Gemini': {
        'model': 'gemini-2.0-flash'
    },
    'InputListener': {
        'talk_key': 't'
    },
    'Vosk': {
        'model_path': 'vosk-model-small-en-us-0.15'
    },
    'Speech': {
        'engine': 'speech_recognition',
        'vb_cable': 'false',
        'vb_cable_device': 'Voicemeeter Input'
    },
    'OBS': {
        'host': 'localhost',
        'port': '4455',
        'password': 'password',
        'websocket_library': 'obsws-python'
    },
    'Sounds': {
        'sounds_dir': 'sounds'
    },
    'Music': {
        'music_dir': 'music'
    }
}

config_file = 'config.ini'
config = configparser.ConfigParser(inline_comment_prefixes=('#', ';'))

if not os.path.exists(config_file):
    config.read_dict(default_config)
    with open(config_file, 'w') as f:
        config.write(f)
else:
    config.read(config_file)
    changed = False
    for section, options in default_config.items():
        if not config.has_section(section):
            config.add_section(section)
            changed = True
        for key, value in options.items():
            if not config.has_option(section, key):
                config.set(section, key, value)
                changed = True
    if changed:
        with open(config_file, 'w') as f:
            config.write(f)
            
LANGUAGE = config.get('General', 'language', fallback='en')
BASE_DIR = config['General']['base_dir']
API_KEY = config['General']['api_key']
VOICE_KEY = config['General']['voice_key']
PERSONALITY = config.get('General', 'personality', fallback='jarvis')
GEMINI_MODEL = config.get('Gemini', 'model', fallback='gemini-2.0-flash')
INPUT_START_KEY = config['InputListener']['talk_key']
INTERRUPT_JARVIS = config['InputListener']['interrupt_jarvis'] == 'true'
VOSK_MODEL_PATH = os.path.join(BASE_DIR, config['Vosk']['model_path'])
SPEECH_ENGINE = config['Speech']['engine'].lower()
VB_CABLE = config.getboolean('Speech', 'vb_cable', fallback=False)
VB_CABLE_DEVICE = config.get('Speech', 'vb_cable_device', fallback='Voicemeeter Input')
OBS_HOST = config['OBS']['host']
OBS_PORT = int(config['OBS']['port'])
OBS_PASSWORD = config['OBS']['password']
WEBSOCKET_LIBRARY = config['OBS']['websocket_library']
SOUNDS_DIR = os.path.join(BASE_DIR, config['Sounds']['sounds_dir'])
MUSIC_DIR = os.path.join(BASE_DIR, config['Music']['music_dir'])

genai.configure(api_key=API_KEY)
set_language(LANGUAGE)
print(f"Loaded language: {LANGUAGE}")