import os

from dotenv import load_dotenv
from flask import session
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

load_dotenv()

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")


class SpotifyAuth:
    def __init__(self, token_info=None):
        self.sp_oauth = SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope="playlist-read-private user-top-read user-read-recently-played user-library-read user-read-private",
        )
        self.token_info = token_info

    def auth_url(self) -> str:
        return self.sp_oauth.get_authorize_url()

    def handle_auth_callback(self, code) -> None:
        token_info = self.sp_oauth.get_access_token(code)
        session["token_info"] = token_info
        print(f"Token obtained with scopes: {token_info.get('scope', 'No scope info')}")

    def spotify_user_client(self) -> spotipy.Spotify:
        if not self.token_info:
            self.token_info = session.get("token_info", None)

        if not self.token_info:
            raise Exception("No token info found")

        try:
            if self.sp_oauth.is_token_expired(self.token_info):
                self.token_info = self.sp_oauth.refresh_access_token(
                    self.token_info["refresh_token"]
                )
                session["token_info"] = self.token_info

            return spotipy.Spotify(auth=self.token_info["access_token"])
        except Exception as e:
            print(f"Error creating Spotify client: {e}")
            session.clear()
            raise Exception("Invalid or expired token")

    def spotify_app_client(self) -> spotipy.Spotify:
        auth_manager = SpotifyClientCredentials(
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET
        )
        return spotipy.Spotify(auth_manager=auth_manager)
