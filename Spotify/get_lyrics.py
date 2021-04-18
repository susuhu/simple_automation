"""
Simple API practice.
Get lyrics from geniuslyrics for the current song playing on your Spotify
With some beautiful printing ;)

"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import lyricsgenius as lg
from rich import print
from rich.highlighter import Highlighter
from random import randint


class Rainbow(Highlighter):
    """for colorfull printing."""

    def highlight(sefl, text):
        for idx in range(len(text)):
            text.stylize(f"color({randint(40,220)})", idx, idx + 1)
            text.stylize("bold")


class SpotifyAPI:
    """create a Spotify API"""

    def __init__(self, client_id, client_secret, redirect_uri, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope

    def get_token(self):
        sp_auth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
        )
        try:
            token = sp_auth.get_cached_token()
        except:
            token = sp_auth.get_access_token()
        return token["access_token"]

    def get_current_song(self):
        sp_obj = spotipy.Spotify(auth=self.get_token())
        current_song = sp_obj.currently_playing()
        song_title = current_song["item"]["name"].split("(")[0].upper()
        artist = current_song["item"]["album"]["artists"][0]["name"].upper()
        return song_title, artist


class geniuslyrics_API:
    """genius lyrisc object"""

    def __init__(self, genius_access_token, title, artist):
        self.genius_access_token = genius_access_token
        self.title = title
        self.artist = artist

    # create genius object
    def create_genius_obj(self):
        return lg.Genius(self.genius_access_token)

    # find the song on geniuslyrics
    def find_song_on_genius(self):
        return self.create_genius_obj().search_song(
            title=self.title, artist=self.artist
        )

    def print_lyrics(self):
        # print the lyrics
        song = self.find_song_on_genius()
        try:
            lyrics = song.lyrics
            s_lyrics = lyrics.split("\n")
            for line in s_lyrics:
                print(f"[r][rosy_brown][b]{line}[/rosy_brown][/r][/b]")
        except:
            print(
                "[r][bold red]Sorry,lyrics [b]NOT[/b] found...[/bold red][/r]:disappointed_relieved:"
            )


if __name__ == "__main__":

    # scope for get current playing
    scope = "user-read-currently-playing"
    # scope = "user-follow-read"
    CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
    CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
    REDIRECT_URI = os.environ["SPOTIPY_REDIRECT_URL"]
    GENIUS_ACCESS_TOKEN = os.environ["GENIUS_ACCESS_TOKEN"]

    rainbow_formating = Rainbow()

    my_spotify = SpotifyAPI(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=scope,
    )
    print(
        ":stuck_out_tongue_winking_eye::stuck_out_tongue_winking_eye::stuck_out_tongue_winking_eye::stuck_out_tongue_winking_eye::stuck_out_tongue_winking_eye:"
    )

    title, artist = my_spotify.get_current_song()

    print("[b]Song name:[/b] ", end="")
    print(rainbow_formating(title))
    print("[b]Artist:[/b] ", end="")
    print(rainbow_formating(artist))
    print(":microphone::microphone::microphone::microphone::microphone:")
    print()
    my_Genius = geniuslyrics_API(
        genius_access_token=GENIUS_ACCESS_TOKEN, title=title, artist=artist
    )

    my_Genius.print_lyrics()
