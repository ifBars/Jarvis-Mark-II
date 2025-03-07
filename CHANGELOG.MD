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

*This release is based on Patchi's Mark 2 implementation and modularized by ifBars. Contributions and pull requests are welcome!*