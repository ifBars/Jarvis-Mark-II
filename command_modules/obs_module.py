import config
from localization import _

if config.WEBSOCKET_LIBRARY.lower() == "obsws-python":
    import obsws_python as obsws_lib
elif config.WEBSOCKET_LIBRARY.lower() == "obswebsocket":
    from obswebsocket import obsws, requests as obs_requests
    obsws_lib = obsws

OBS_HOST = config.OBS_HOST
OBS_PORT = config.OBS_PORT
OBS_PASSWORD = config.OBS_PASSWORD

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
            ws.start_replay_buffer()
            ws.save_replay_buffer()
            ws.disconnect()
        else:
            ws = obsws_lib(OBS_HOST, OBS_PORT, OBS_PASSWORD)
            ws.connect()
            ws.call(obs_requests.StartReplayBuffer())
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