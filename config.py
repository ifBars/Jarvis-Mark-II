import os
import sys
import configparser
import google.generativeai as genai
from localization import set_language
from pathlib import Path

def load_config(config, config_file, default_config):
    """Reads the configuration from `config_file`, adds any missing sections
    or options from `default_config`, and writes changes back if needed."""
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

    return config

def update_language(lang):
    """Update the language setting in the config file."""
    config.set("Settings", "language", lang)
    with open(config_file, "w") as configfile:
        config.write(configfile)
    print(_("Language updated to {lang}. Restart the application to apply changes.").format(lang=lang))
    
def update_personality(new_personality):
    """Update the personality setting in the config file."""
    config.set("General", "personality", new_personality)
    with open(config_file, "w") as configfile:
        config.write(configfile)
    print(_("Personality updated to {personality}. Restarting the application.").format(personality=new_personality))

def update_obs():
    global config
    config = load_config(config, config_file, default_config)
    OBS_HOST = config['OBS']['host']
    OBS_PORT = int(config['OBS']['port'])
    OBS_PASSWORD = config['OBS']['password']
    WEBSOCKET_LIBRARY = config['OBS']['websocket_library']
    return OBS_HOST, OBS_PORT, OBS_PASSWORD, WEBSOCKET_LIBRARY

default_config = {
    'General': {
        'language': 'en',
        'base_dir': r'C:\Jarvis-Mark-II',
        'api_key': 'your_api_key',
        'voice_key': r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enGB_GeorgeM',
        'personality': 'jarvis',
        'interrupt_jarvis': 'true',
        'enabled_modules': 'main_module\nmusic_module\nobs_module\nspotify_module'
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
    'Spotify': {
        'client_id': 'your_spotify_app_client_id'
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
    config = load_config(config, config_file, default_config)
            
LANGUAGE = config.get('General', 'language', fallback='en')
BASE_DIR = config['General']['base_dir']
API_KEY = config['General']['api_key']
VOICE_KEY = config['General']['voice_key']
ENABLED_MODULES = config['General']['enabled_modules'].splitlines()
PERSONALITY = config.get('General', 'personality', fallback='jarvis')
GEMINI_MODEL = config.get('Gemini', 'model', fallback='gemini-2.0-flash')
SPOTIFY_CLIENT_ID = config['Spotify']['client_id']
INPUT_START_KEY = config['InputListener']['talk_key']
INTERRUPT_JARVIS = config['General']['interrupt_jarvis']
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