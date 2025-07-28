import polars as pl

from spotify_reccomendations.lib.spotify_api.spotify_auth import SpotifyAuth
from spotify_reccomendations.lib.models.top_tracks import TopTracks


class SpotifyRequests:
    def __init__(self, token_info):
        auth = SpotifyAuth(token_info)
        self.user_spotify_client = auth.spotify_user_client()
        self.app_spotify_client = auth.spotify_app_client()

    @staticmethod
    def _format_tracks(top_tracks) -> pl.DataFrame:
        formatted_tracks = []
        for track in top_tracks:

            formatted_tracks.append(
                {
                    "name": track.get("name"),
                    "artist": track.get("artists")[0].get("name"),
                    "album": track.get("album").get("name"),
                    "duration_ms": track.get("duration_ms"),
                    "cover_image": track.get("album").get("images")[0].get("url"),
                    "track_id": track.get("id"),
                }
            )
        return pl.DataFrame(formatted_tracks)

    def user_top_tracks(self, num_tracks: int = 10) -> TopTracks:
        top_tracks = self.user_spotify_client.current_user_top_tracks(limit=num_tracks)[
            "items"
        ]
        return TopTracks(self._format_tracks(top_tracks))

    def get_track_info(self, tracks) -> dict:
        track_info = []
        for track in tracks:
            query = f'track:"{track.get("name")}" artist:"{track.get("artist")}"'
            results = self.app_spotify_client.search(q=query, type="track", limit=1)
            if results.get("tracks").get("items"):
                track_info.append(results.get("tracks").get("items")[0])
            else:
                continue
        return self._format_tracks(track_info)
