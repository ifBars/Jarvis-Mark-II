# Changelog

**All Credits To ([PatchiPup](https://www.youtube.com/@PatchiPup)) for the original idea and creation**

Contributions are welcome – please add your entries in the appropriate section, crediting your name.

## [Mark 1] - Feb. 10th, 2025 (Patchi)
- **Original Implementation:**  
  - Created by Patchi as demonstrated in the first YouTube video.  

## [Mark 2] - March 2nd, 2025 (Patchi)
- **Updated Public Version:**  
  - Created by Patchi in the second YouTube video and released for public download.
  - Improved functionality and additional commands compared to Mark 1.

## [Mark 2.1] - March 6th, 2025 (ifBars)
- **Streamlined Setup Process**
  - Mark 2.1 comes with setup and start batch files that automate the process of setting up and running Jarvis. Simply run setup.bat to install everything needed, make any necesarry changes to config.ini, then run start.bat to start Jarvis.
- **Modularization:**  
  - Refactored the original single-file code into multiple modules:
    - `config.py` – Loads configuration from an external `config.ini` file.
    - `tasks.py` – Implements an asynchronous task queue.
    - `audio.py` – Handles text-to-speech and audio capture.
    - `chat.py` – Manages the generative AI chat session.
    - `commands.py` – Parses and executes embedded commands.
    - `music.py` – Manages music playback.
    - `obs_integration.py` – Integrates OBS WebSocket commands.
    - `input_listener.py` – Monitors keyboard input.
    - `main.py` – Main application loop.
    - `start.bat` – An easy way to start Jarvis.
    - `setup.bat` – Automates the installation process for Jarvis.
- **Configuration Template:**  
  - All settings (API key, OBS details, model paths, etc.) are now managed via a single `config.ini` file, providing an easier setup process. setup.bat also automates filling out part of this config file.
- **Documentation:**  
  - Added a README and a CHANGELOG to facilitate contributions from the community.

## [Mark 2.2] - March 8th, 2025 (Supereiris)
- **Command Modularization**
  - Commands can now be written in different modules which allows for easy addition/removal. Any modules under the `command_modules` folder are automatically added to the system on launch.

  - HOW TO WRITE A COMMAND MODULE:
    - 1. Create a python script under `command_modules` folder.

    - 2. Create a dictionary named `command_handlers` and add the commands in this format: `"cmd": lambda content: (function_name, (arg1, arg2, ...))`
      - Change the following fields ONLY:
        - `cmd` - The command name (3 letters EXACTLY)
        - `function_name` - The name of the function to be executed (probably a function in the same file)
        - `arg` - The arguments of the function (all placed in a tuple)

      - `content` - This is the arguments that jarvis is passing (just a string) and can be processed to form the args (the name of the variable is not important). Can also be replaced with `_` if it is not  going to be used.

    - 3. Create a string named `commands_string` to and add the description of the commands you entered above. This is going to be passed in jarvis. To keep the formatting consistent it is better to use this format: `cmd()        - Description of command`

    - 4. If you wish create another variable `additional_info` and add any extra information you would like to pass to jarvis.

    - *IMPORTANT: the variable names `command_handlers, commands_string, additional_info` should NOT be changed*

- **New Files Added**
  - `command_modules_init.py` - Initializes the command modules
  - `exit.py` - Handles the command for the termination of the program
  - `obs_module.py` - Moved OBS related commands to this module
  - `music_module.py` - Moved music related commands to this module
  - `main_module.py` - Moved remaining commands to this module

- **Modifications in Existing Scripts**
  - `main.py` - Added the functionality to terminate script from command
  - `chat.py` - Modified to support command modularization and removed sound list
  - `commands.py` - Modified to support command modularization
  - `tasks.py` - Modified to support command modularization.
  
## [Mark 2.3] - March 9th, 2025 (ifBars)
- **Localization & Bug fixes**
  - Jarvis now has a localization system, that allows contributors to add translations for new languages. Refer to readme for how to contribute to localization.
  
- **Auto-Updater**
  - Jarvis now has an updater system, that checks for any updates and asks you if you want to install them upon running Jarvis, automatically installing the updates if you say yes.
  - The updater system works like so, setup.bat installs git for the user and initializes the repo if it is not already. Then updater.py compares the local and latest commit, pulling the latest commit if necesarry.

## [Mark 2.4] - March 11th, 2025 (Supereiris)
- **Spotify Module**
  - Jarvis can now connect to your spotify and play songs and playlists for you.
  
  - Features:
    - Play a song, playlist or artist's top songs
    - Play a playlist the user has created
    - Option to shuffle playlists
    - Add a song to the queue
    - Shuffle queue
    - Pause/Resume/Skip player
    - Let Jarvis choose and play a song
  
  - Requirements:
    - To use the commands, open spotify BEFORE launching Jarvis.
    - Some of the features like skip require a premium spotify subscription.     
  
  **Interrupt Jarvis**
  Jarvis stops talking when you press the key to talk. Can be toggled off in config.ini

## [Mark 2.4.1] - March 11th, 2025 (Supereiris)
- **Toggleable Modules**
  - Modules can now be enabled/disabled in config.ini.
  - To disable a module just comment out the line by placing a ';' in the start.

- **Updated README.MD**
  - Added a tutorial on how to set up the Spotify Module

## [Mark 2.4.2] - March 13th, 2025 (ifBars)
- **Macros**
  - Jarvis now has a macro system, that allows users to have Jarvis create macros that run Jarvis commands, and run them upon request.
  
- **More Personalities**
  - Added some ChatGPT generated personalities

- **Improvements to README**
  - Added Macros & Personalities sections to README

## [Mark 2.4.2] - March 13th, 2025 (ifBars)
- **Macros Bug Fix**
  - Fixed the bug where Jarvis had issues finding your macros directory

- **Fast Whisper Support**
  - Jarvis now supports the Fast Whisper model for speech recognition via setting engine to fast_whisper in config

*This release is based on Patchi's Mark 2 implementation and modularized by multiple contributors. Contributions and pull requests are welcome!*