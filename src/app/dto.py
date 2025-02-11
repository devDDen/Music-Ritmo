from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Genre:
    albumCount: int
    songCount: int
    name: str


@dataclass
class GenreItem:
    name: str


@dataclass
class ArtistItem:
    id: int
    name: str
    album_count: int | None = None
    cover_art_id: int | None = None
    starred: datetime | None = None


@dataclass
class Track:
    id: int
    title: str
    album: str | None = None
    album_id: int | None = None
    artist: str | None = None
    artist_id: int | None = None
    track_number: int | None = None
    disc_number: int | None = None
    year: int | None = None
    genre: str | None = None
    cover_art_id: int | None = None
    file_size: int | None = None
    content_type: str | None = None
    duration: int | None = None
    bit_rate: int | None = None
    sampling_rate: int | None = None
    bit_depth: int | None = None
    channel_count: int | None = None
    path: str | None = None
    play_count: int = 0
    created: datetime | None = None
    starred: datetime | None = None
    bpm: int | None = None
    comment: str | None = None
    artists: List[ArtistItem] = field(default_factory=list)
    genres: List[GenreItem] = field(default_factory=list)
