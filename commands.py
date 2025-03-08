import time
import random
import numpy as np
import pyautogui
import os
import pygame
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from config import SOUNDS_DIR
from music import skip_song, toggle_pause, play_music
from obs_integration import stop_recording, start_recording, save_clip
from pynput.keyboard import Key, Controller as KeyController, KeyCode
from pynput.mouse import Controller as MouseController, Button
from tasks import add_task

keyboard = KeyController()
mouse = MouseController()
onteam = True

def fireshots(n):
    for _ in range(n):
        press('o')
        time.sleep(0.7)

def unibeam(n):
    pyautogui.mouseDown(button='right')
    time.sleep(n)
    pyautogui.mouseUp(button='right')

def press(key):
    if key.lower() == "shift":
        keyboard.press(Key.shift)
        time.sleep(random.uniform(0.1, 0.2))
        keyboard.release(Key.shift)
    else:
        keyboard.press(key)
        time.sleep(random.uniform(0.1, 0.2))
        keyboard.release(key)

def freaky():
    for _ in range(50):
        keyboard.press('u')
        time.sleep(0.01)
        keyboard.release('u')
        time.sleep(0.05)

def play_sound(sound):
    sound_path = os.path.join(SOUNDS_DIR, f"{sound}.mp3")
    if os.path.exists(sound_path):
        pygame.mixer.Sound(sound_path).play()

def insta_lock():
    screen_width, screen_height = pyautogui.size()
    tx = int(screen_width * 1800 / 1920)
    ty = int(screen_height * 650 / 1080)
    duration = 0.3
    steps = 30
    sx, sy = mouse.position
    p1 = (sx + 300, sy - 200)
    p2 = (tx - 100, ty + 200)
    p3 = (tx, ty)
    
    # Using cosine easing for natural acceleration and deceleration
    t_values = [(1 - np.cos(t * np.pi)) / 2 for t in np.linspace(0, 1, steps)]
    
    curve = [
        (
            (1 - t) ** 3 * sx + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0],
            (1 - t) ** 3 * sy + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
        )
        for t in t_values
    ]
    
    step_time = duration / steps
    for x, y in curve:
        mouse.position = (int(x), int(y))
        time.sleep(step_time)
    
    mouse.scroll(0, -1)
    mouse.scroll(0, -1)
    time.sleep(0.1)
    mouse.click(Button.left, 2)

def typerandom(message):
    for char in message:
        keyboard.press(char)
        time.sleep(random.uniform(0.02, 0.08))
        keyboard.release(char)

def chat(message, target):
    global onteam
    if target and not onteam:
        pyautogui.press("enter")
        press("\t")
        time.sleep(0.2)
        typerandom(message)
        pyautogui.press("enter")
        onteam = True
    elif not target and onteam:
        pyautogui.press("enter")
        press("\t")
        time.sleep(0.2)
        typerandom(message)
        pyautogui.press("enter")
        onteam = False
    else:
        pyautogui.press("enter")
        time.sleep(0.2)
        typerandom(message)
        pyautogui.press("enter")

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
muted = False

def toggle_mute():
    global muted
    muted = not muted
    volume.SetMute(muted, None)

def set_volume(level):
    volume.SetMasterVolumeLevelScalar(level / 100.0, None)

def change_volume(amount):
    current = volume.GetMasterVolumeLevelScalar() * 100
    new_level = max(0, min(100, current + amount))
    volume.SetMasterVolumeLevelScalar(new_level / 100.0, None)

def process_command(response):
    """
    Parse the LLM response for embedded command tokens.
    Schedule actions via add_task and return the cleaned response text and any sound effects.
    """
    sound_effects = []
    clean_response = []
    i = 0
    length = len(response)
    while i < length:
        if response[i:i+4] == "prs(":
            j = response.find(")", i)
            if j != -1:
                add_task(press, response[i+4:j])
                i = j
        elif response[i:i+4] == "msg(":
            j = response.find(")", i)
            if j != -1:
                content = response[i+4:j].strip()
                if content.endswith("true"):
                    add_task(chat, content[:-4].strip(), True)
                elif content.endswith("false"):
                    add_task(chat, content[:-5].strip(), False)
                i = j
        elif response[i:i+4] == "ply(":
            j = response.find(")", i)
            if j != -1:
                sound_effects.append(response[i+4:j])
                i = j
        elif response[i:i+4] == "dly(":
            j = response.find(")", i)
            if j != -1:
                add_task(time.sleep, float(response[i+4:j]))
                i = j
        elif response[i:i+4] == "vls(":
            j = response.find(")", i)
            if j != -1:
                add_task(set_volume, int(response[i+4:j]))
                i = j
        elif response[i:i+4] == "fre(":
            j = response.find(")", i)
            if j != -1:
                add_task(fireshots, int(response[i+4:j]))
                i = j
        elif response[i:i+4] == "uni(":
            j = response.find(")", i)
            if j != -1:
                add_task(unibeam, float(response[i+4:j]))
                i = j
        elif response[i:i+4] == "ext;":
            exit()
        elif response[i:i+4] == "frk;":
            add_task(freaky)
            i += 3
        elif response[i:i+4] == "lck;":
            add_task(insta_lock)
            i += 3
        elif response[i:i+4] == "clp;":
            add_task(save_clip)
            i += 3
        elif response[i:i+4] == "str;":
            add_task(start_recording)
            i += 3
        elif response[i:i+4] == "spr;":
            add_task(stop_recording)
            i += 3
        elif response[i:i+4] == "mut;":
            toggle_mute()
            i += 3
        elif response[i:i+4] == "vld;":
            add_task(change_volume, -10)
            i += 3
        elif response[i:i+4] == "vlu;":
            add_task(change_volume, 10)
            i += 3
        elif response[i:i+4] == "mpl(":
            j = response.find(")", i)
            if j != -1:
                play_music(response[i+4:j])
                i = j
        elif response[i:i+4] == "mps;":
            toggle_pause()
            i += 3
        elif response[i:i+4] == "skp;":
            skip_song()
            i += 3
        else:
            clean_response.append(response[i])
        i += 1
    return "".join(clean_response).strip(), sound_effects
