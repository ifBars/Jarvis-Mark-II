# Jarvis – Marvel Rivals AI Assistant

Jarvis is a modular, voice-controlled AI assistant inspired by Iron Man's system. Originally created by Patchi ([PatchiPup](https://www.youtube.com/@PatchiPup)), this project has been refactored to improve maintainability and extensibility. It now uses a modular design with separate files for configuration, audio processing, command parsing, and more.

## Features

- **Voice Recognition & TTS:** Press and hold the **T** key to activate your microphone; responses are spoken via text-to-speech.
- **Embedded Command Parsing:** Automatically detects and executes specific in-game commands embedded in the AI’s responses.
- **OBS Integration:** Control OBS recording and clip saving via WebSocket.
- **Music Playback:** Play, pause, resume, and skip songs from designated playlists.
- **External Configuration:** All settings (e.g., API keys, OBS info, Vosk model paths) are managed via a single `config.ini` file.
- **Modular Design:** Code is split into modules (`config.py`, `audio.py`, `chat.py`, `commands.py`, etc.) to simplify contributions and future extensions.

## Mark 2.0 Installation Google Doc

The installation guide for **Mark 2.0** is available in the Google Doc linked below:

[View the Google Doc](https://docs.google.com/document/d/1STOtrWikkjOU_NCjUmY4COfTySb01chrkCE3kcUkTGU/edit?usp=sharing)

*Created by cyburak*

## Mark 2.1 Installation

1. **Download the Repository:**
   - **With Git:**  
     If you have Git installed, clone the repository by running:
     ```bash
     git clone https://github.com/PatchiPup/Jarvis-Mark-II.git
     cd Jarvis-Mark-II
     ```
   - **Without Git:**  
     If you don't have Git, simply download the repository as a **.zip** file from the [GitHub page](https://github.com/PatchiPup/Jarvis-Mark-II) and extract it.

2. **Run the Setup:**
   DO NOT RUN AS ADMIN, IT WILL PROMPT YOU FOR ADMIN WHEN NEEDED
   ```bash
   setup.bat
   ```

3. **Start Jarvis:**
   DO NOT RUN AS ADMIN, IT WILL PROMPT YOU FOR ADMIN WHEN NEEDED
   ```bash
   start.bat
   ```

## Common Installation Issues

1. **No module named 'audioop'**
   - Any error relating to audioop, usually arises when you are using the latest version of python, 3.13, as audioop was removed from python in this version. This means if you are using python 3.13 or later, you will need to install [audioop-lts](https://pypi.org/project/audioop-lts/). The setup.bat should handle this for you, but in the case it doesn't and you get an audioop error, this is why, and installing it via pip should fix your issuie.
  
2. **No module named pynput**
   - Did you run the setup.bat first? If so, please seek help in the discord with screenshots of your error, jarvis folder, and config.ini

3. 