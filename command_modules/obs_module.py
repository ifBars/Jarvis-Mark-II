import config
from localization import _
import time
import os
import sys
from contextlib import redirect_stderr
from config import update_obs

if config.WEBSOCKET_LIBRARY.lower() == "obsws-python":
    import obsws_python as obsws_lib
elif config.WEBSOCKET_LIBRARY.lower() == "obswebsocket":
    from obswebsocket import obsws, requests as obs_requests
    obsws_lib = obsws

OBS_HOST = config.OBS_HOST
OBS_PORT = config.OBS_PORT
OBS_PASSWORD = config.OBS_PASSWORD
WEBSOCKET_LIBRARY = config.WEBSOCKET_LIBRARY

def initialize_obs_replay_buffer():
    global OBS_HOST
    global OBS_PORT
    global OBS_PASSWORD
    global WEBSOCKET_LIBRARY
    connected = False
    while not connected:
        try:
            with redirect_stderr(open(os.devnull, 'w')):
                if WEBSOCKET_LIBRARY.lower() == "obsws-python":
                    ws = obsws_lib.ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD, timeout=3)
                    status = ws.get_replay_buffer_status()
                    connected = True
                    if not status.output_active:
                        ws.start_replay_buffer()
                        time.sleep(1)
                    ws.disconnect()
                else:
                    ws = obsws_lib(OBS_HOST, OBS_PORT, OBS_PASSWORD)
                    ws.connect()
                    connected = True
                    rb_status = ws.call(obs_requests.GetReplayBufferStatus())
                    if not rb_status.getResults().get('isActive'):
                        ws.call(obs_requests.StartReplayBuffer())
                        time.sleep(1)
                    ws.disconnect()
        except ConnectionRefusedError:
            input("Cannot connect to OBS. Please ensure OBS is running then press Enter to retry...")
        except Exception as e:
            if "failed to identify client with the server" in str(e):
                input("OBS websocket authentication failed. Please update your OBS settings in config.ini then press Enter to retry...")
                OBS_HOST, OBS_PORT, OBS_PASSWORD, WEBSOCKET_LIBRARY = update_obs()
            else:
                print(e)

initialize_obs_replay_buffer()

command_handlers = {
    "clp": lambda _: (save_clip, ()),
    "str": lambda _: (start_recording, ()),
    "spr": lambda _: (stop_recording, ())
}

commands_string = """
 clp()        - Save or clip replays  
 str()        - Start recording  
 spr()        - Stop recording  
"""

def save_clip():
    try:
        if config.WEBSOCKET_LIBRARY.lower() == "obsws-python":
            ws = obsws_lib.ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD, timeout=3)
            ws.save_replay_buffer()
            ws.disconnect()
        else:
            ws = obsws_lib(OBS_HOST, OBS_PORT, OBS_PASSWORD)
            ws.connect()
            ws.call(obs_requests.SaveReplayBuffer())
            ws.disconnect()
    except Exception as e:
        print(_("Error in save_clip:"), e)

def start_recording():
    try:
        if config.WEBSOCKET_LIBRARY.lower() == "obsws-python":
            ws = obsws_lib.ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD, timeout=3)
            ws.start_record()
            ws.disconnect()
            print(_("Recording Started!"))
        else:
            ws = obsws_lib(OBS_HOST, OBS_PORT, OBS_PASSWORD)
            ws.connect()
            ws.call(obs_requests.StartRecording())
            ws.disconnect()
            print(_("Recording Started!"))
    except Exception as e:
        print(_("Failed to start recording:"), e)

def stop_recording():
    try:
        if config.WEBSOCKET_LIBRARY.lower() == "obsws-python":
            ws = obsws_lib.ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD, timeout=3)
            ws.stop_record()
            ws.disconnect()
            print(_("Recording Stopped!"))
        else:
            ws = obsws_lib(OBS_HOST, OBS_PORT, OBS_PASSWORD)
            ws.connect()
            ws.call(obs_requests.StopRecording())
            ws.disconnect()
            print(_("Recording Stopped!"))
    except Exception as e:
        print(_("Failed to stop recording:"), e)
