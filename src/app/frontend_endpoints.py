from typing import Any
from fastapi import APIRouter, Body, HTTPException, Depends
from fastapi.responses import JSONResponse, Response
from sqlmodel import Session, select
from mutagen.mp3 import MP3
from mutagen.flac import FLAC

from .subsonic_response import SubsonicResponse
from .auth import authenticate_user

from . import db_loading
from . import database as db
from . import service_layer
from . import utils

frontend_router = APIRouter(prefix="/specific")


@frontend_router.get("/generateAvatar")
def generate_random_avatar(
    current_user: db.User = Depends(authenticate_user),
    session: Session = Depends(db.get_session),
):

    avatar = service_layer.generate_and_save_avatar(session, current_user)

    return Response(content=avatar, media_type="image/png")


@frontend_router.get("/getSortedArtistAlbums")
def get_sorted_artist_albums(
    id: int,
    size: int = 10,
    offset: int = 0,
    session: Session = Depends(db.get_session),
):
    album_service = service_layer.AlbumService(session)
    sortedAlbums = album_service.get_sorted_artist_albums(id, size, offset)

    rsp = SubsonicResponse()
    rsp.data["sortedAlbums"] = sortedAlbums
    return rsp.to_json_rsp()


@frontend_router.get("/getCoverArtPreview")
def get_cover_art_preview(
    id: int, session: Session = Depends(db.get_session)
) -> Response:
    track = session.exec(select(db.Track).where(db.Track.id == id)).one_or_none()
    if track is None:
        return JSONResponse({"detail": "No such id"}, status_code=404)

    return Response(content=track.cover, media_type=f"image/{track.cover_type}")


@frontend_router.get("/getTags")
def get_tags(id: int, session: Session = Depends(db.get_session)) -> JSONResponse:
    track = session.exec(select(db.Track).where(db.Track.id == id)).one_or_none()
    if track is None:
        return JSONResponse({"detail": "No such id"}, status_code=404)

    return JSONResponse(
        utils.get_base_tags(track, session) | utils.get_custom_tags(track)
    )


@frontend_router.put("/updateTags")
def update_tags(
    id: int,
    data: dict[str, Any] = Body(...),
    session: Session = Depends(db.get_session),
) -> JSONResponse:
    track = session.exec(select(db.Track).where(db.Track.id == id)).one_or_none()
    if track is None:
        return JSONResponse({"detail": "No such id"}, status_code=404)

    audio, audio_type = utils.update_tags(track, data, session)

    audio_info = db_loading.AudioInfo(track.file_path)
    match audio_type:
        case utils.AudioType.MP3:
            db_loading.extract_metadata_mp3(MP3(track.file_path), audio_info)
        case utils.AudioType.FLAC:
            db_loading.extract_metadata_flac(FLAC(track.file_path), audio_info)

    db_loading.load_audio_data(audio_info)

    return JSONResponse({"detail": "success"})
