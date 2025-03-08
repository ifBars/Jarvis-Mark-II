import os
import configparser
import google.generativeai as genai

default_config = {
    'General': {
        'base_dir': 'C:\Jarvis-Mark-II',
        'api_key': 'your-api-key',
        'voice_key': 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enGB_GeorgeM'
    },
    'InputListener': {
        'talk_key': 't'
    },
    'Vosk': {
        'model_path': 'vosk-model-small-en-us-0.15'
    },
    'Speech': {
        'engine': 'speech_recognition'
    },
    'OBS': {
        'host': 'localhost',
        'port': '4455',
        'password': 'password'
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

BASE_DIR = config['General']['base_dir']
API_KEY = config['General']['api_key']
VOICE_KEY = config['General']['voice_key']
INPUT_START_KEY = config['InputListener']['talk_key']
VOSK_MODEL_PATH = os.path.join(BASE_DIR, config['Vosk']['model_path'])
SPEECH_ENGINE = config['Speech']['engine'].lower()
OBS_HOST = config['OBS']['host']
OBS_PORT = int(config['OBS']['port'])
OBS_PASSWORD = config['OBS']['password']
SOUNDS_DIR = os.path.join(BASE_DIR, config['Sounds']['sounds_dir'])
MUSIC_DIR = os.path.join(BASE_DIR, config['Music']['music_dir'])

genai.configure(api_key=API_KEY)
