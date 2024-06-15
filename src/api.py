from db import db
from models.Artist import Artist
from models.Song import Song
from fastapi import FastAPI, APIRouter, Request, HTTPException
from typing import Union
import uuid
import os
import sys
sys.path.append(os.path.join(os.path.abspath(
    os.path.abspath(os.path.dirname(__file__)))))


app = FastAPI(
    title="API Floppotron",
    description="Esta es la API para gestionar las canciones y artistas para el Floppotron",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={
        "displayRequestDuration": True,
        "tryItOutEnabled": True,
    },
)
tags_metadata = [
    {
        "name": "songs",
        "description": "Canciones del Floppotron",
    },
    {
        "name": "artists",
        "description": "Artistas de las pistas del Floppotron",
    },
]

router = APIRouter()


@app.get("/", include_in_schema=False)
async def index():
    return {"Mensaje": "Bienvenido a la API de las canciones del Floppotron. Accede al Swagger en 127.0.0.1:8000/docs"}


############
# Songs
############

@router.get("/songs", tags=["songs"])
async def get_songs(request: Request, limit: int = 5, offset: int = 1):
    session = uuid.uuid4()
    order = {}
    filter = {}
    if 'application/json' in request.headers.get('Content-Type', ''):
        body = await request.json()
        if 'order' in body:
            order = body['order']
        if 'filter' in body:
            filter = body['filter']

    next = f"/songs?limit={limit}&offset={offset + 1}"

    songs = db.get_songs(limit=limit, offset=offset,
                         order_dict=order, filter_dict=filter)

    if not songs:
        raise HTTPException(
            status_code=404, detail="No se encontraron canciones")
    if "error" in songs:
        raise HTTPException(status_code=500, detail=songs["error"])

    return {"session": session, "success": True, "next": next, "songs": songs}


@router.get("/songs/{song_id}", tags=["songs"])
async def get_song(song_id: int):
    session = uuid.uuid4()

    song = db.get_song(song_id=song_id)

    if not song:
        raise HTTPException(
            status_code=404, detail="No se encontró la canción")
    if "error" in song:
        raise HTTPException(status_code=500, detail=song["error"])

    return {"session": session, "success": True, "songs": song}


@router.post("/songs", tags=["songs"])
async def create_song(request: Request, song: Union[Song, None] = None):
    session = uuid.uuid4()

    if not song:
        raise HTTPException(
            status_code=400, detail="No se ha proporcionado una canción")

    song = db.create_song(song)

    if not song:
        raise HTTPException(
            status_code=404, detail=f"No se ha encontrado el artista especificado")
    if isinstance(song, dict) and "error" in song:
        raise HTTPException(status_code=500, detail=song["error"])

    return {"session": session, "success": True, "created_song": song}


@router.put("/songs/{song_id}", tags=["songs"])
async def update_song(song_id: int, body: dict):
    session = uuid.uuid4()

    song = db.update_song(song_id=song_id, changes=body)

    if not song:
        raise HTTPException(
            status_code=404, detail=f"No se ha encontrado la canción con ID {song_id}")
    if isinstance(song, dict) and "error" in song:
        raise HTTPException(status_code=500, detail=song["error"])

    return {"session": session, "success": True, "updated_song": song}


@router.delete("/songs/{song_id}", tags=["songs"])
async def delete_song(song_id: int):
    session = uuid.uuid4()

    song = db.delete_song(song_id=song_id)

    if not song:
        raise HTTPException(
            status_code=404, detail=f"No se ha encontrado la canción con ID {song_id}")
    if isinstance(song, dict) and "error" in song:
        raise HTTPException(status_code=500, detail=song["error"])

    return {"session": session, "success": True, "deleted_song": song}


############
# Artists
############

@router.get("/artists", tags=["artists"])
async def get_artists(request: Request, limit: int = 5, offset: int = 1):
    session = uuid.uuid4()
    order = {}
    filter = {}
    if 'application/json' in request.headers.get('Content-Type', ''):
        body = await request.json()
        if 'order' in body:
            order = body['order']
        if 'filter' in body:
            filter = body['filter']

    next = f"/artists?limit={limit}&offset={offset + 1}"

    artists = db.get_artists(limit=limit, offset=offset,
                             order_dict=order, filter_dict=filter)

    if not artists:
        raise HTTPException(
            status_code=404, detail="No se encontraron artistas")
    if "error" in artists:
        raise HTTPException(status_code=500, detail=artists["error"])

    return {"session": session, "success": True, "next": next, "artists": artists}


@router.get("/artists/{artist_id}", tags=["artists"])
async def get_artists(artist_id: int):
    session = uuid.uuid4()

    artist = db.get_artist(artist_id=artist_id)

    if not artist:
        raise HTTPException(
            status_code=404, detail="No se encontró el artista")
    if "error" in artist:
        raise HTTPException(status_code=500, detail=artist["error"])

    return {"session": session, "success": True, "artists": artist}


@router.post("/artists", tags=["artists"])
async def create_artist(request: Request, artist: Union[Artist, None] = None):
    session = uuid.uuid4()

    if not artist:
        raise HTTPException(
            status_code=400, detail="No se ha proporcionado un artista")

    artist = db.create_artist(artist)

    if not artist:
        raise HTTPException(
            status_code=404, detail=f"No se ha encontrado el artista especificado")
    if isinstance(artist, dict) and "error" in artist:
        raise HTTPException(status_code=500, detail=artist["error"])

    return {"session": session, "success": True, "created_artist": artist}


@router.put("/artists/{artist_id}", tags=["artists"])
async def update_artist(artist_id: int, body: dict):
    session = uuid.uuid4()

    artist = db.update_artist(artist_id=artist_id, changes=body)

    if not artist:
        raise HTTPException(
            status_code=404, detail=f"No se ha encontrado el artista con ID {artist_id}")
    if isinstance(artist, dict) and "error" in artist:
        raise HTTPException(status_code=500, detail=artist["error"])

    return {"session": session, "success": True, "updated_artist": artist}


@router.delete("/artists/{artist_id}", tags=["artists"])
async def delete_artist(artist_id: int):
    session = uuid.uuid4()

    artist = db.delete_artist(artist_id=artist_id)

    if not artist:
        raise HTTPException(
            status_code=404, detail=f"No se ha el artista con ID {artist_id}")
    if isinstance(artist, dict) and "error" in artist:
        raise HTTPException(status_code=500, detail=artist["error"])

    return {"session": session, "success": True, "deleted_artist": artist}

app.include_router(router)
