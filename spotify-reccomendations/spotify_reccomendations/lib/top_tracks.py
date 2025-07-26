import polars as pl

class TopTracks:
    schema = pl.Schema(
        [
            ("name", pl.Utf8),
            ("artist", pl.Utf8),
            ("album", pl.Utf8),
            ("duration_ms", pl.Int64),
            ("cover_image", pl.Utf8),
        ]
    )

    def __init__(self, dataframe):
        if dataframe.schema != self.schema:
            raise ValueError("Dataframe schema does not match expected schema")
        self.dataframe = dataframe

