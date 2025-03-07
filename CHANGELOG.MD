# Changelog

Contributions are welcome – please add your entries in the appropriate section, crediting your name.

## [Mark 1] - Feb. 10th, 2025
- **Original Implementation:**  
  - Created by Patchi as demonstrated in the first YouTube video ([PatchiPup](https://www.youtube.com/@PatchiPup)).  

## [Mark 2] - March 2nd, 2025
- **Updated Public Version:**  
  - Created by Patchi in the second YouTube video and released for public download.
  - Improved functionality and additional commands compared to Mark 1.

## [Mark 2.1] - March 6th, 2025
- **Modularization by ifBars:**  
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
- **Configuration Template:**  
  - All settings (API key, OBS details, model paths, etc.) are now managed via a single `config.ini` file, providing an easier setup process.
- **Documentation:**  
  - Added a README and a CHANGELOG to facilitate contributions from the community.

*This release is based on Patchi's Mark 2 implementation and modularized by ifBars. Contributions and pull requests are welcome!*