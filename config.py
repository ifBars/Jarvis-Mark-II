import os
import sys
import configparser
import re
import google.generativeai as genai
from localization import set_language
from pathlib import Path

def load_config(config, config_file, default_config):
    """
    Reads the configuration from `config_file`, adds any missing sections/options
    from `default_config`, and ensures that all default modules are present in the
    enabled_modules option (while preserving commented-out lines).
    """
    config.read(config_file)
    changed = False
    for section, options in default_config.items():
        if not config.has_section(section):
            config.add_section(section); changed = True
        for key, value in options.items():
            if not config.has_option(section, key):
                config.set(section, key, value); changed = True

    default_modules = [line.strip() for line in default_config.get("General", {}).get("enabled_modules", "").splitlines() if line.strip()]
    update_enabled_modules(config_file, default_modules)

    if changed:
        with open(config_file, 'w') as f:
            config.write(f)
    return config


def update_enabled_modules(config_file, default_modules):
    """
    Updates the enabled_modules block in the [General] section of the config file,
    appending any missing modules while preserving commented-out lines.
    """
    with open(config_file, 'r') as f:
        lines = f.readlines()

    # Locate the [General] section.
    gen_start = next((i for i, l in enumerate(lines) if re.match(r'\s*\[General\]\s*$', l)), None)
    if gen_start is None:
        return
    gen_end = next((i for i, l in enumerate(lines[gen_start+1:], start=gen_start+1) if re.match(r'\s*\[.*\]\s*$', l)), len(lines))

    # Find the enabled_modules line.
    em_idx = next((i for i in range(gen_start, gen_end) if re.match(r'\s*enabled_modules\s*=.*$', lines[i])), None)

    def get_module(line):
        s = line.lstrip()
        if s and s[0] in (';', '#'):
            s = s[1:].strip()
        return s.split()[0] if s.split() else ""

    if em_idx is not None:
        block_start = em_idx
        block_end = block_start + 1
        while block_end < gen_end and lines[block_end].startswith((" ", "\t")):
            block_end += 1
        block_lines = lines[block_start:block_end]
        eq_index = block_lines[0].find('=')
        values = [block_lines[0][eq_index+1:].rstrip()] + [l.rstrip() for l in block_lines[1:]]
        existing = {get_module(v) for v in values if get_module(v)}
        missing = [m for m in default_modules if m not in existing]
        if missing:
            indent = next((re.match(r'^(\s+)', l).group(1) for l in values[1:] if re.match(r'^(\s+)', l)), "\t")
            values += [indent + m for m in missing]
            new_block = [block_lines[0][:eq_index+1] + " " + values[0].lstrip() + "\n"] + [v + "\n" for v in values[1:]]
            lines = lines[:block_start] + new_block + lines[block_end:]
            with open(config_file, 'w') as f:
                f.writelines(lines)
    else:
        new_block = []
        if default_modules:
            new_block.append("enabled_modules = " + default_modules[0] + "\n")
            new_block.extend("\t" + m + "\n" for m in default_modules[1:])
        lines = lines[:gen_end] + new_block + lines[gen_end:]
        with open(config_file, 'w') as f:
            f.writelines(lines)

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
        'ultron_startup': 'true',
        'interrupt_jarvis': 'true',
        'enabled_modules': 'main_module\nmusic_module\nobs_module\nspotify_module\nmacro_module'
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
    },
    'Macros': {
        'macros_dir': 'macros'
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
ULTRON_STARTUP = config.getboolean('General', 'ultron_startup', fallback=True)
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
MACRO_DIR = os.path.join(BASE_DIR, config['Macros']['macros_dir'])

genai.configure(api_key=API_KEY)
set_language(LANGUAGE)
print(f"Loaded language: {LANGUAGE}")