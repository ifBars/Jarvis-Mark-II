# Jarvis – Marvel Rivals AI Assistant

## Table of Contents
- [Jarvis – Marvel Rivals AI Assistant](#jarvis--marvel-rivals-ai-assistant)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Installation Guides](#installation-guides)
    - [Mark 2.1 Installation Video Guide](#mark-21-installation-video-guide)
    - [Mark 2.1 Installation Text Guide](#mark-21-installation-text-guide)
    - [Mark 2.0 Installation Google Doc](#mark-20-installation-google-doc)
  - [Speech Engines](#speech-engines)
    - [Vosk](#vosk)
    - [speech\_recognition](#speech_recognition)
    - [faster\_whisper](#faster_whisper)
  - [Spotify Module Set Up](#spotify-module-set-up)
  - [Macros](#macros)
    - [Manually Creating Macros](#manually-creating-macros)
  - [Personalities](#personalities)
    - [Creating a Personality](#creating-a-personality)
    - [Personality Credits](#personality-credits)
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

- **Macros:** Users can request to have Jarvis create Macros that can run a set sequence of commands upon request.
- **Voice Recognition & TTS:** Press and hold the **T** key to activate your microphone; responses are spoken via text-to-speech.
- **Embedded Command Parsing:** Automatically detects and executes specific in-game commands embedded in the AI’s responses.
- **OBS Integration:** Control OBS recording and clip saving via WebSocket.
- **Music Playback with Spotify Integration:** Play, pause, resume, and skip songs from designated playlists.
- **External Configuration:** All settings (e.g., API keys, OBS info, Vosk model paths) are managed via a single `config.ini` file.
- **Modular Design:** Code is split into modules (`config.py`, `audio.py`, `chat.py`, `commands.py`, etc.) to simplify contributions and future extensions.

## Installation Guides

### Mark 2.1 Installation Video Guide

[https://www.youtube.com/watch?v=AaZ1x0DO-ZE](https://www.youtube.com/watch?v=AaZ1x0DO-ZE)

### Mark 2.1 Installation Text Guide

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

## Speech Engines

Jarvis supports three different speech recognition engines—**vosk**, **speech_recognition**, and **faster_whisper**—each designed to address varying needs in terms of performance, accuracy, and system resource usage. You can switch between the 3 by putting their name as the engine property under the Speech category of your config.ini file.

### Vosk

Vosk is a lightweight engine that shines on low-hardware machines. It can deliver decent results , making it a suitable for lower-end PCs. However, its simplicity comes at the cost of recognition accuracy compared to its peers.

### speech_recognition

In most cases, the **speech_recognition** engine offers better results than vosk while maintaining similar performance. It is well balanced between speed and accuracy, making it a great all-around choice.

### faster_whisper

For users who desire the best accuracy in recognition, **faster_whisper** is the top performer. Leveraging advanced algorithms from OpenAI, it provides state-of-the-art recognition quality that outperforms the other two engines. The trade-off is its higher system resource usage.

## Spotify Module Set Up

To be able to use the Spotify module of Jarvis you need to create a Spotify Developer App and obtain the Client ID. This guide will walk you through the entire process. (Super Simple!)

- **Step 1**: Create a Spotify Developer Account

   Before you can create an app, you need a Spotify Developer account.

   1. Go to the Spotify Developer Dashboard (https://developer.spotify.com/dashboard).
   2. Click Log in and sign in with your Spotify account.
   3. If prompted, accept the terms and conditions.

- **Step 2**: Create a New Spotify App

   1. Once logged in, click "Create an App".
   2. Enter the App Name and App Description (e.g., "Jarvis").
   3. Set the Redirect URI to **http://127.0.0.1:8888/callback**
   4. Toggle 'Web API' option
   5. Agree to the Spotify API terms and click Create.

- **Step 3**: Get Your Client ID
   
   After creating the app:

   1. Open the app in the Spotify Developer Dashboard.
   2. Click 'Settings' on top right
   3. Copy the Client ID

- **Step 4**: Insert your Client ID to config.ini

   Open config.ini and under 'Spotify' enter your Client ID in the field 'client_id'

**You Are Done!**

The spotify module should now be working. Beware that some features like 'skip song' require a premium spotify membership to work.

## Macros

Jarvis allows you to automate complex tasks by creating macros—sequences of multiple actions executed in order. You can quickly create macros through simple voice commands. For example:

> "Jarvis, create a new macro to initiate flight for 3 seconds, then stop flying, wait 1 second, fire 5 shots, and save it as fly and shoot."

Jarvis supports using any existing commands within macros. Adding brief delays (e.g., a 1-second wait) between actions can greatly improve macro reliability. Without appropriate delays, certain actions may overlap or fail to execute correctly. In the above example, firing immediately after stopping flight might result in the first shot failing because the action to stop flying hasn't fully completed yet.

### Manually Creating Macros

Alternatively, you can manually create macros by adding a new JSON file within the `macros` folder. Use hyphens (`-`) or underscores (`_`) instead of spaces for file names. For instance, a macro named `fly-and-shoot.json` would contain:

```json
{
  "name": "fly-and-shoot",
  "commands": ["prs(shift)", "dly(3)", "prs(shift)", "dly(1)", "fre(5)"]
}
```

## Personalities

Jarvis supports different "personalities," which are essentially different Gemini system instructions. You can ask Jarvis to load a new personality at any time, and you can also request a list of the available personalities. Alternatively, you can manually change the personality directly from the `config.ini` file.

### Creating a Personality

To create a new personality:

1. **Copy the Base File:**  
   Duplicate the `personalities/jarvis.json` file from the repository as your starting point.

2. **Rename the File:**  
   Rename the copied file to match your new personality (for example, `friday.json`, `karen.json`, `ultron.json`, etc.).

3. **Modify the Content:**  
   Open your new file and update the `"base"` section in each language block (`"en"`, `"es"`, `"pt"`, `"fr"`, etc.) to define the unique tone, style, and behavior of your personality.

4. **Adjust the Ending (Optional):**  
   Modify the `"ending"` section if necessary, to customize how commands are finalized.

5. **Save and Load:**  
   Save your changes and load the new personality in your app—either via a command or by editing the `config.ini` file.

For an example of a personality file, refer to the [personalities/jarvis.json](./personalities/jarvis.json) in the repository.

### Personality Credits

We welcome and appreciate community contributions to the personality files! Below is a list of contributors who have added or updated personality files in this repository:

- **Patchi** – Created the original Jarvis personality
- **tschadov** – Created the Heimdall personality
- **ChatGPT Generated Personalities** – Friday, Karen, Ultron (These are encouraged to community improvements/modifications)

If you've created or modified a personality and would like to be credited, please follow these guidelines:

1. **Pull Request Details:**  
   When submitting a pull request with a new or updated personality, add your credit here so this list can be up-to-date.

Thank you for helping build a forward-thinking community!

## Locales

Jarvis is designed to offer a localized user experience by supporting multiple languages for most things. The language is selected by modifying the `language` option in the `config.ini` file. The current supported locales are:

- **en**: English (default)
- **es**: Spanish
- **pt**: Portuguese
- **fr**: French

These locales need to be updated upon every single update, and I nor other contributors cannot guarantee that these will be updated regularly. PRs for translations are always welcomed, and if you would like Jarvis to be translated into your langauge, or better support for an existing translation, please open an issue on the Github.

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

6. **INVALID_CLIENT: Invalid redirect URI**
   - If you are getting this error when setting up the spotify module, usually this is caused by attempted to connect your spotify account to the wrong spotify app. Ensure your client_id in config.ini matches your client_id from the spotify developer page of your created spotify app.

7. **Couldn't find ffpmeg or avconv**
   - This means you do not have ffpmeg installed, however Jarvis uses de-compressed audio files, so ffmpeg is not needed. So as long as your Jarvis is still working correctly, you can safely ignore this error. Otherwise ask for help in the discord.

## Changelog

For a detailed list of changes and updates, please refer to the [CHANGELOG.MD](CHANGELOG.MD) file.
