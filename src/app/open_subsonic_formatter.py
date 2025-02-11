from typing import List

from src.app.dto import *


class OpenSubsonicFormatter:
    @staticmethod
    def format_genre(genre: Genre):
        return {
            "albumCount": genre.albumCount,
            "songCount": genre.songCount,
            "value": genre.name,
        }

    @staticmethod
    def format_genres(genres: List[Genre]):
        return {"genre": list(map(OpenSubsonicFormatter.format_genre, genres))}
