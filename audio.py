import tempfile
import threading
import time
import pyttsx3
import pygame
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import config

# Initialize pyttsx3 engine and set voice.
engine = pyttsx3.init()
pygame.mixer.init()
print(f"[DEBUG] Using {config.VOICE_KEY} voice for tts")
voices = engine.getProperty('voices')
for v in voices:
    print(v.id)
engine.setProperty('voice', config.VOICE_KEY)
speech_channel = pygame.mixer.Channel(1)

def speak(text, rate=170, pitch_factor=0.98):
    """Convert text to speech and play asynchronously."""
    def _speak():
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_filename = temp_file.name
        temp_file.close()

        engine.setProperty('rate', rate)
        engine.save_to_file(text, temp_filename)
        engine.runAndWait()

        sound = AudioSegment.from_file(temp_filename, format="wav")
        new_sample_rate = int(sound.frame_rate * pitch_factor)
        pitched_sound = sound._spawn(sound.raw_data, overrides={"frame_rate": new_sample_rate})
        pitched_sound = pitched_sound.set_frame_rate(44100)
        pitched_sound.export(temp_filename, format="wav")

        playback = pygame.mixer.Sound(temp_filename)
        speech_channel.play(playback)
        while speech_channel.get_busy():
            time.sleep(0.1)
    threading.Thread(target=_speak, daemon=True).start()

# Set up Vosk model and PyAudio stream.
vosk_model = Model(config.VOSK_MODEL_PATH)
recognizer = KaldiRecognizer(vosk_model, 16000)
mic = pyaudio.PyAudio()
stream = mic.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=8192
)

def process_audio(is_t_pressed):
    """
    Capture audio while the T key is held.
    Return the transcribed text.
    """
    audio_frames = []
    while is_t_pressed():
        data = stream.read(4096, exception_on_overflow=False)
        audio_frames.append(data)
    if audio_frames:
        for frame in audio_frames:
            recognizer.AcceptWaveform(frame)
        result = json.loads(recognizer.FinalResult())
        return result.get("text", "")
    return None

def close_audio():
    stream.stop_stream()
    stream.close()
    mic.terminate()
