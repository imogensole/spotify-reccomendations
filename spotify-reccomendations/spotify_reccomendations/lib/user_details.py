import spotipy
from spotify_reccomendations.lib.spotify_auth import SpotifyAuth

class SpotifyUser:
    def __init__(self, token_info):
        self.token_info = token_info
        self.sp = SpotifyAuth().spotify_client()
        self.user = self.sp.current_user()

    def display_name(self) -> str:
        return self.user.get("display_name")

    def profile_image(self) -> str:
        return self.user.get("images")[0].get("url")
