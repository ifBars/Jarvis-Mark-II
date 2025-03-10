# Jarvis – Marvel Rivals AI Assistant

## Table of Contents
- [Jarvis – Marvel Rivals AI Assistant](#jarvis--marvel-rivals-ai-assistant)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Installation Guides](#installation-guides)
    - [Mark 2.1 Installation](#mark-21-installation)
    - [Mark 2.0 Installation Google Doc](#mark-20-installation-google-doc)
  - [Locales](#locales)
    - [How It Works](#how-it-works)
    - [Directory Structure](#directory-structure)
    - [Adding New Languages](#adding-new-languages)
  - [Common Installation Issues](#common-installation-issues)
  - [Changelog](#changelog)

---

## Overview

Jarvis is a modular, voice-controlled AI assistant inspired by Iron Man's system. Originally created by Patchi ([PatchiPup](https://www.youtube.com/@PatchiPup)), this project has been refactored to improve maintainability and extensibility. It now uses a modular design with separate files for configuration, audio processing, command parsing, and more.

## Features

- **Voice Recognition & TTS:** Press and hold the **T** key to activate your microphone; responses are spoken via text-to-speech.
- **Embedded Command Parsing:** Automatically detects and executes specific in-game commands embedded in the AI’s responses.
- **OBS Integration:** Control OBS recording and clip saving via WebSocket.
- **Music Playback:** Play, pause, resume, and skip songs from designated playlists.
- **External Configuration:** All settings (e.g., API keys, OBS info, Vosk model paths) are managed via a single `config.ini` file.
- **Modular Design:** Code is split into modules (`config.py`, `audio.py`, `chat.py`, `commands.py`, etc.) to simplify contributions and future extensions.

## Installation Guides

### Mark 2.1 Installation

1. **Download the Repository:**
   - **With Git:**  
     ```bash
     git clone https://github.com/PatchiPup/Jarvis-Mark-II.git
     cd Jarvis-Mark-II
     ```
   - **Without Git:**  
     If you don't have Git, simply download the repository as a **.zip** file from the [GitHub page](https://github.com/PatchiPup/Jarvis-Mark-II/archive/refs/heads/main.zip) and extract it.

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

### Mark 2.0 Installation Google Doc

The installation guide for **Mark 2.0** is available in the Google Doc linked below:

[View the Google Doc](https://docs.google.com/document/d/1STOtrWikkjOU_NCjUmY4COfTySb01chrkCE3kcUkTGU/edit?usp=sharing)

*Created by cyburak*

## Locales

Jarvis is designed to offer a localized user experience by supporting multiple languages. The language is selected by modifying the `language` option in the `config.ini` file. The current supported locales are:

- **en**: English (default)
- **es**: Spanish
- **pt**: Portuguese
- **fr**: French

### How It Works

When Jarvis starts, it reads the `language` setting from `config.ini` and loads the corresponding language files from the `locales` directory. This ensures that all messages and prompts appear in the selected language.

### Directory Structure

The project uses a clear directory structure for managing locale files. Here’s an example of the structure:

```
Jarvis/
└── locales/
    ├── en/
    │   └── LC_MESSAGES/
    │       ├── messages.mo
    │       └── messages.po
    ├── es/
    │   └── LC_MESSAGES/
    │       ├── messages.mo
    │       └── messages.po
    ├── pt/
    │   └── LC_MESSAGES/
    │       ├── messages.mo
    │       └── messages.po
    ├── fr/
    │   └── LC_MESSAGES/
    │       ├── messages.mo
    │       └── messages.po
    └── system_instructions.json
    └── setup_instructions.json
```

Each language folder contains an `LC_MESSAGES` subdirectory, which in turn houses the `messages.po` and 'messages.mo' files containing all the translatable strings.

### Adding New Languages

Collaborators can easily add support for new languages by following these steps:

1. **Create a New Folder:**  
   Under the `locales` directory, create a new folder using the appropriate ISO language code (e.g., `de` for German).

2. **Set Up the Directory Structure:**  
   Inside your new language folder, create a subdirectory named `LC_MESSAGES`.

3. **Add the Translation File:**  
   Create a `messages.po` file within the `LC_MESSAGES` folder. Use the same keys and structure as the existing locale `messages.po` files to maintain consistency. (ex: msgid, msgstr)

4. **Translate System Instructions:**
   In addition to the messages, translate the `system_instructions.json` file located in the `locales` directory. Ensure that the translations follow the original structure and context.

5. **Translate Setup & Start Scripts Messages**
   Finally before compiling and testing, translate the `setup_instructions.json` file located in the `locales` directory. Ensure that the translations follow the original structure and context. Then edit setup.bat, and add your language option to the language selection section.

5. **Compile the File:**  
   Use `msgfmt` to compile the `messages.po` file into a `messages.mo` file:
   ```bash
   msgfmt locales/de/LC_MESSAGES/messages.po -o locales/de/LC_MESSAGES/messages.mo
   ```
   Replace `de` with the desired language code as needed.

6. **Update Configurations:**  
   To test your new language, update the `language` setting in `config.ini` to your new language code (e.g., `de`) and run Jarvis.

## Common Installation Issues

1. **No module named audioop**
   - Any error relating to audioop, usually arises when you are using the latest version of python, 3.13, as audioop was removed from python in this version. This means if you are using python 3.13 or later, you will need to install [audioop-lts](https://pypi.org/project/audioop-lts/). The setup.bat should handle this for you, but in the case it doesn't and you get an audioop error, this is why, and installing it via pip should fix your issue.
  
2. **No module named pynput**
   - Did you run the setup.bat first? If so, please seek help in the discord with screenshots of your error, jarvis folder, and config.ini

3. **No such file or directory**
   - Usually this means your base_dir in config.ini is not set correctly, you can try running setup.bat again, or setting the base_dir manually.

4. **Could not find a version that satisfies the requirement audioop-lts**
   - This means you are on python 3.12 or earlier, and do not need to install audioop-lts

5. **Start/Stop Recording is not working**
   - First ensure you have the latest version of Jarvis. Then check what version of OBS you have. If you have OBS 27.x or earlier, ensure `websocket_library` inside `config.ini` is set to `obswebsocket`. If you have OBS 28.x or later, ensure `websocket_library` inside `config.ini` is set to `obsws-python`.

## Changelog

For a detailed list of changes and updates, please refer to the [CHANGELOG.MD](CHANGELOG.MD) file.
