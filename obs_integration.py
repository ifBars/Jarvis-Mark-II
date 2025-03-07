from obswebsocket import obsws, requests
import config

OBS_HOST = config.OBS_HOST
OBS_PORT = config.OBS_PORT
OBS_PASSWORD = config.OBS_PASSWORD

def save_clip():
    try:
        ws = obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD)
        ws.connect()
        ws.call(requests.StartReplayBuffer())
        ws.call(requests.SaveReplayBuffer())
        ws.disconnect()
    except Exception:
        pass

def start_recording():
    try:
        ws = obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD)
        ws.connect()
        ws.call(requests.StartRecording())
        ws.disconnect()
        print("Recording Started!")
    except Exception as e:
        print("Failed to start recording:", e)

def stop_recording():
    try:
        ws = obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD)
        ws.connect()
        ws.call(requests.StopRecording())
        ws.disconnect()
        print("Recording Stopped!")
    except Exception as e:
        print("Failed to stop recording:", e)
