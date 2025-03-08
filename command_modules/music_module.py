import os
import pygame
import threading
import time
import random
from config import MUSIC_DIR

pygame.mixer.init()

music_queue = []
current_song_index = 0
playing = False

def get_playlists():
    """Return a list of folder names in MUSIC_DIR (each representing a playlist)."""
    try:
        return [d for d in os.listdir(MUSIC_DIR) if os.path.isdir(os.path.join(MUSIC_DIR, d))]
    except Exception as e:
        print("Error reading MUSIC_DIR:", e)
        return []

# Dynamically list available playlists in the commands string.
available_playlists = ", ".join(get_playlists())

command_handlers = {
    "skp": lambda _: (skip_song, ()),
    "mps": lambda _: (toggle_pause, ()),
    "mpl": lambda content: (play_music, (content,))
}

commands_string = f"""
 mpl(name)   - Start a music playlist. Available playlists: {available_playlists}
 mps()       - Pause or resume music  
 skp()       - Skip the current song 
"""

def music_thread(folder):
    global music_queue, current_song_index, playing
    music_folder = os.path.join(MUSIC_DIR, folder)
    if os.path.exists(music_folder):
        music_queue = [os.path.join(music_folder, f) for f in os.listdir(music_folder)
                       if f.endswith(('.mp3', '.wav'))]
        if music_queue:
            playing = True
            current_song_index = 0
            while playing:
                pygame.mixer.music.load(music_queue[current_song_index])
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() > 0:
                    pygame.time.wait(1000)
                    if not playing:
                        return
                current_song_index = (current_song_index + 1) % len(music_queue)
    else:
        print("Playlist not found. Available playlists:", ", ".join(get_playlists()))

def play_music(folder):
    if folder not in get_playlists():
        print(f"Playlist '{folder}' not found. Available playlists: {', '.join(get_playlists())}")
        return
    threading.Thread(target=music_thread, args=(folder,), daemon=True).start()

def toggle_pause():
    global playing
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        playing = False
    else:
        pygame.mixer.music.unpause()
        playing = True

def skip_song():
    global current_song_index, music_queue
    if music_queue:
        pygame.mixer.music.stop()
        current_song_index = (current_song_index + 1) % len(music_queue)
        pygame.mixer.music.load(music_queue[current_song_index])
        pygame.mixer.music.play()
