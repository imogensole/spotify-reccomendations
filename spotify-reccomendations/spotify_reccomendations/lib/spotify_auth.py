import os

from dotenv import load_dotenv
from flask import session
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

class SpotifyAuth:
    def __init__(self):
        self.sp_oauth = SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope="playlist-read-private user-top-read user-read-recently-played user-library-read",    
        )
    
    def auth_url(self) -> str:
        return self.sp_oauth.get_authorize_url()

    def handle_auth_callback(self, code) -> None:
        token_info = self.sp_oauth.get_access_token(code)
        session["token_info"] = token_info

    def spotify_client(self) -> spotipy.Spotify:
        token_info = session.get("token_info", None)

        if not token_info:
            raise "Exception: No token info found"
        if self.sp_oauth.is_token_expired(token_info):
            token_info = self.sp_oauth.refresh_access_token(token_info["refresh_token"])
            session["token_info"] = token_info
        
        return spotipy.Spotify(auth=token_info["access_token"])
