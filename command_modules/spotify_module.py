import random
import spotipy
from spotipy.oauth2 import SpotifyPKCE

# Authenticate using PKCE
sp = spotipy.Spotify(auth_manager=SpotifyPKCE(
    client_id="816bdceb410e4bb5b16ef27d7ae4b362", 
    redirect_uri="http://localhost:8888/callback",
    scope="user-modify-playback-state,user-read-playback-state,user-top-read",
    cache_path=".spotify_cache.json"  # Store token locally
))

# Get active device
devices = sp.devices()
device_id = None

playlist_data = sp.current_user_playlists()
user_playlists = ','.join([r["name"] for r in playlist_data["items"]])

if devices["devices"]:
    device_id = devices["devices"][0]["id"]  # Select first active device
else:
    print("No active Spotify device found!")

command_handlers = {
        "sps": lambda content: (play_song, (content)),
        "spa": lambda content: (play_artist, (content)),
        "spp": lambda content: (play_playlist, (content.split('$')[0], content.endswith("true"))),
        "saq": lambda content: (add_to_queue, (content)),
        "spj": lambda _: (play_jarvis_choice, ()),
        "ssh": lambda _: (shuffle, ()),
        "sau": lambda _: (pause, ()),
        "sre": lambda _: (resume, ()),
        "ssk": lambda _: (skip, ()),
    }
commands_string = f"""
  sps(n)      - Play a song on spotify. Can also include the artist name in the argument
  spa(n)      - Play an artist on spotify
  spp(n$shuffle)      - Search and Play za playlist on spotify (doesn't need to be one of user's playlists). shuffle argument is 'true' or 'false', User's Spotify Playlists: {user_playlists}
  saq(n)      - Add a song on queue on spotify
  spj()      - You choose and play a song on spotify.
  ssh()      - Shuffle queue
  sau()      - Pause spotify player.
  sre()      - Resume spotify player.
  ssk()      - Skip the current song on spotify.
  
  """

additional_info = """
When the user asks you to play a playlist on spotify don't limit yourself to the user's spotify playlists. If the requested one is not found in the available list then just execute the command nevertheless.
"""
def get_track(song):
    results = sp.search(q=song, type="track", limit=1)

    if results["tracks"]["items"]:
        return results["tracks"]["items"][0] # Get the first result
    else:
        print("Song not found")
        return None

def play_track(track):
    track_uri = track['uri']
    track_name = track['name']
    sp.start_playback(uris=[track_uri])   
    print(f"Playing: {track_name}")     

def play_song(song):
    track = get_track(song)
    if track:
        track_uri = track["uri"]
        print(f"Playing: {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")

        sp.start_playback(uris=[track_uri])

def play_artist(artist_name):
    """Plays the top track from a specified artist."""
    # Search for the artist
    results = sp.search(q=artist_name, limit=1, type="artist")
    
    if results["artists"]["items"]:
        artist = results["artists"]["items"][0]
        artist_id = artist["id"]

        # Get the artist's top tracks
        top_tracks = sp.artist_top_tracks(artist_id)
        
        if top_tracks["tracks"]:
            track_uris = [track["uri"] for track in top_tracks["tracks"]]
            sp.start_playback(uris=track_uris)
        else:
            print("No top tracks found for this artist.")
    else:
        print("Artist not found!")

def play_playlist(name, shuffle):

    if name in user_playlists:
        play_user_playlist(name, shuffle)
        print("found in own")
        return

    results = sp.search(q=name, limit=1, type="playlist")
    
    if results["playlists"]["items"]:
        playlists = results["playlists"]["items"][0]
        playlist_uri = playlists["uri"]
        sp.start_playback(context_uri=playlist_uri)
        sp.shuffle(state=shuffle)
        print(f"Started playing playlist: {playlists['name']}")
    else:
        print("Playlist not found!")

def play_user_playlist(playlist_name, shuffle):
    results = sp.current_user_playlists()
    for playlist in results["items"]:
        if playlist["name"] == playlist_name:
            sp.start_playback(context_uri=playlist["uri"])
            sp.shuffle(state=shuffle)
            print(f"Now Playing {playlist["name"]}\nShuffle:{shuffle}")
            return
    print(f"No playlist {playlist_name} found")

def play_jarvis_choice():
    # Either play a random track from user's top tracks or a random track from user's top artist
    if random.randint(0,1) == 0:
        top_tracks = sp.current_user_top_tracks() 
        if top_tracks['items']:
            # Choose a random track from the user's top tracks
            random_track = random.choice(top_tracks['items'])
            play_track(random_track)     
        else:
            print("No top tracks found.")
    else:
        top_artist = sp.current_user_top_artists()
        if top_artist["items"]:
            random_artist = random.choice(top_artist['items'])
            top_tracks = sp.artist_top_tracks(random_artist["id"])["tracks"]
            if top_tracks:
                random_track = random.choice(top_tracks)
                play_track(random_track)
            else:
                print(f"No top tracks for {random_artist["name"]} found.")    
        else:
            print("No top artists found.")      

def add_to_queue(song):
    track = get_track(song)
    track_uri = track["uri"]
    sp.add_to_queue(track_uri)
    print(f"Added On Queue: {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")

def pause():
    sp.pause_playback()
    print("Spotify Paused")

def resume():
    sp.start_playback()
    print("Spotify Resumed")

def skip():
    sp.next_track()
    print("Track Skipped")

def shuffle():
    sp.shuffle(state=True)
    print("Queue Shuffled")
