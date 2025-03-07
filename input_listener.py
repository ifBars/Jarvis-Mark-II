from pynput.keyboard import Key, KeyCode, Listener

# Use a mutable container to track T key status.
t_pressed_flag = [False]

def on_press(key):
    if isinstance(key, KeyCode) and key.char == 't':
        t_pressed_flag[0] = True

def on_release(key):
    if isinstance(key, KeyCode) and key.char == 't':
        t_pressed_flag[0] = False

listener = Listener(on_press=on_press, on_release=on_release)
listener.start()

def is_t_pressed():
    return t_pressed_flag[0]
