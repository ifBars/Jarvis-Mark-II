# Jarvis – Marvel Rivals AI Assistant

Jarvis is a modular, voice-controlled AI assistant inspired by Iron Man's system. Originally created by Patchi ([PatchiPup](https://www.youtube.com/@PatchiPup)), this project has been refactored to improve maintainability and extensibility. It now uses a modular design with separate files for configuration, audio processing, command parsing, and more.

## Features

- **Voice Recognition & TTS:** Press and hold the **T** key to activate your microphone; responses are spoken via text-to-speech.
- **Embedded Command Parsing:** Automatically detects and executes specific in-game commands embedded in the AI’s responses.
- **OBS Integration:** Control OBS recording and clip saving via WebSocket.
- **Music Playback:** Play, pause, resume, and skip songs from designated playlists.
- **External Configuration:** All settings (e.g., API keys, OBS info, Vosk model paths) are managed via a single `config.ini` file.
- **Modular Design:** Code is split into modules (`config.py`, `audio.py`, `chat.py`, `commands.py`, etc.) to simplify contributions and future extensions.

## Installation

1. **Download the Repository:**
   - **With Git:**  
     If you have Git installed, clone the repository by running:
     ```bash
     git clone https://github.com/ifBars/Jarvis-Mark-II.git
     cd Jarvis-Mark-II
     ```
   - **Without Git:**  
     If you don't have Git, simply download the repository as a **.zip** file from the [GitHub page](https://github.com/ifBars/Jarvis-Mark-II) and extract it.

2. **Run the Setup:**
   ```bash
   setup.bat
   ```

3. **Start Jarvis:**
   ```bash
   start.bat
   ```