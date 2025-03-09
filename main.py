from input_listener import is_t_pressed
from audio import process_audio, speak, close_audio
from chat import send_to_jarvis
from exit import should_exit
from commands import process_command
from config import INPUT_START_KEY
from localization import _

def main():
    print(_("Press and hold {key} to communicate with Jarvis using your default microphone").format(key=INPUT_START_KEY))
    try:
        while True:
            if is_t_pressed():
                print(_("Listening..."))
                transcribed_text = process_audio(is_t_pressed)
                if transcribed_text:
                    print(_("You said:"), transcribed_text)
                    send_to_jarvis(transcribed_text, process_command, speak)
            
            if should_exit():
                print(_("Program Terminated"))
                break
    except KeyboardInterrupt:
        pass
    finally:
        close_audio()

if __name__ == '__main__':
    main()
