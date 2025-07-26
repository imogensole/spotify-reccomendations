import spotipy
import polars as pl

from spotify_reccomendations.lib.spotify_auth import SpotifyAuth
from spotify_reccomendations.lib.top_tracks import TopTracks

class SpotifyRequests:
    def __init__(self, token_info):
        self.token_info = token_info
        self.sp = SpotifyAuth().spotify_client()

    @staticmethod
    def _format_top_tracks(top_tracks) -> pl.DataFrame:
        formatted_tracks = []
        for track in top_tracks:
            formatted_tracks.append(
                {
                    "name": track.get("name"),
                    "artist": track.get("artists")[0].get("name"),
                    "album": track.get("album").get("name"),
                    "duration_ms": track.get("duration_ms"),
                    "cover_image": track.get("album").get("images")[0].get("url"),
                }
            )
        return pl.DataFrame(formatted_tracks)

    def user_top_tracks(self) -> TopTracks:
        top_tracks = self.sp.current_user_top_tracks(limit=10)['items']
        return TopTracks(self._format_top_tracks(top_tracks))