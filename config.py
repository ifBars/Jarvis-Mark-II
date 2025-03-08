import os
import configparser
import google.generativeai as genai

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# General settings
BASE_DIR = config['General']['base_dir']
API_KEY = config['General']['api_key']
VOICE_KEY = config['General']['voice_key']

# Vosk settings
VOSK_MODEL_PATH = os.path.join(BASE_DIR, config['Vosk']['model_path'])

# Speech engine selection
SPEECH_ENGINE = config['Speech']['engine'].lower()

# OBS settings
OBS_HOST = config['OBS']['host']
OBS_PORT = int(config['OBS']['port'])
OBS_PASSWORD = config['OBS']['password']

# Directories for sounds and music (relative to BASE_DIR)
SOUNDS_DIR = os.path.join(BASE_DIR, config['Sounds']['sounds_dir'])
MUSIC_DIR = os.path.join(BASE_DIR, config['Music']['music_dir'])

# Configure the generative AI API
genai.configure(api_key=API_KEY)
