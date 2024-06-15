from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, relationship

from models.Artist import Artist as ArtistModel
from models.Song import Song as SongModel

DATABASE_URL = "sqlite:///data/floppotron.db"
Base = declarative_base()

# Crear las tablas en la base de datos


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True,
                autoincrement=True, index=True, nullable=True)
    name = Column(String, index=True, nullable=False)
    country = Column(String, nullable=True)
    born_year = Column(Integer, nullable=True)

    songs = relationship("Song", back_populates="artist")

    def __repr__(self):
        return f"{self.name} from {self.country} born in {self.born_year} with songs {[song.name for song in self.songs]}"


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True,
                autoincrement=True, index=True, nullable=True)
    name = Column(String, index=True, nullable=False)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    created_year = Column(Integer, nullable=True)
    format_type = Column(String, nullable=True)
    duration = Column(Integer, nullable=True)
    path = Column(String, nullable=False)

    artist = relationship("Artist", back_populates="songs")

    def __repr__(self):
        return f"{self.name} composed by {self.artist.name} created in {self.created_year} in format {self.format_type} with duration {self.duration} and path {self.path}"


# Crear la base de datos
engine = create_engine(DATABASE_URL, echo=True)
# Crear la tabla en la base de datos
Base.metadata.create_all(bind=engine)
# Crear la sesión de la base de datos
Session = sessionmaker(bind=engine)
session = Session()

filter_ops = {
    '=': lambda field, value: field == value,
    '!=': lambda field, value: field != value,
    '>': lambda field, value: field > value,
    '<': lambda field, value: field < value,
    '>=': lambda field, value: field >= value,
    '<=': lambda field, value: field <= value,
    'like': lambda field, value: field.like(value),
}


def get_songs(limit, offset, order_dict, filter_dict):
    page = (offset - 1) * limit

    with session as db:
        try:
            query = db.query(Song)

            if filter_dict:
                try:
                    query = query.filter(filter_ops[filter_dict.get("op", "=")](
                        getattr(Song, filter_dict["field"]), filter_dict["value"]))
                except AttributeError as e:
                    return {"error": f"Un campo especificado en filter no existe en la tabla Song: {e}"}

            if order_dict:
                try:
                    for key, value in order_dict.items():
                        query = query.order_by(getattr(Song, key).desc(
                        ) if value == "desc" else getattr(Song, key))
                except AttributeError as e:
                    return {"error": f"Un campo especificado en order no existe en la tabla Song: {e}"}
            else:
                query = query.order_by(Song.id)

            # Añadimos límite y paginación
            query = query.limit(limit).offset(page)
            result = query.all()

            if not result:
                return {"error": f"No se han encontrado canciones"}

            songs = [repr(song) for song in result]

            return {"songs": songs}
        except Exception as e:
            return {"error": f"Error al obtener las canciones: {e}"}


def get_song(song_id):

    with session as db:
        try:
            query = db.query(Song)\
                .filter(Song.id == song_id)\
                .order_by(Song.id)

            result = query.first()

            if not result:
                return {"error": f"No se ha encontrado la canción"}

            song = repr(result)

            return song
        except Exception as e:
            return {"error": f"Error al obtener la canción: {e}"}


def create_song(song: SongModel):
    with session as db:
        try:
            db_artist = db.query(Artist).filter(
                Artist.id == song.artist_id).first()
            if not db_artist:
                return None
            song = Song(name=song.name, artist_id=song.artist_id, created_year=song.created_year,
                        format_type=song.format_type, duration=song.duration, path=song.path)
            db.add(song)
            db.commit()
            db.refresh(song)
        except Exception as e:
            return {"error": f"Error al crear la canción: {e}"}
        return song


not_modifiable_fields = [
    "id", "artist_id", "created_year", "format_type", "duration", "path"
]


def update_song(song_id, changes):
    for field in changes.keys():
        if field in not_modifiable_fields:
            return {"error": f"El campo '{field}' no se puede modificar"}
        if not hasattr(Song, field):
            return {"error": f"El campo '{field}' no existe en la tabla Song"}

    with session as db:
        try:
            db_song = db.query(Song).filter(Song.id == song_id).first()
            if not db_song:
                return None

            for field, value in changes.items():
                setattr(db_song, field, value)
            db.commit()
            db.refresh(db_song)
        except Exception as e:
            return {"error": f"Error al crear la canción: {e}"}
        return db_song


def delete_song(song_id):
    with session as db:
        try:
            db_song = db.query(Song).filter(Song.id == song_id).first()
            if not db_song:
                return None
            db.delete(db_song)
            db.commit()
        except Exception as e:
            return {"error": f"Error al eliminar la canción: {e}"}
        return song_id


def get_artists(limit, offset, order_dict, filter_dict):
    page = (offset - 1) * limit

    with session as db:
        try:
            query = db.query(Artist)

            if filter_dict:
                try:
                    query = query.filter(filter_ops[filter_dict.get("op", "=")](
                        getattr(Artist, filter_dict["field"]), filter_dict["value"]))
                except AttributeError as e:
                    return {"error": f"Un campo especificado en filter no existe en la tabla Artist: {e}"}

            if order_dict:
                try:
                    for key, value in order_dict.items():
                        query = query.order_by(getattr(Artist, key).desc(
                        ) if value == "desc" else getattr(Artist, key))
                except AttributeError as e:
                    return {"error": f"Un campo especificado en order no existe en la tabla Artist: {e}"}
            else:
                query = query.order_by(Artist.id)

            # Añadimos límite y paginación
            query = query.limit(limit).offset(page)
            result = query.all()

            if not result:
                return {"error": f"No se han encontrado artistas"}

            artists = [repr(artist) for artist in result]

            return {"artists": artists}
        except Exception as e:
            return {"error": f"Error al obtener los artistas: {e}"}


def get_artist(artist_id):
    with session as db:
        try:
            query = db.query(Artist)\
                .filter(Artist.id == artist_id)\
                .order_by(Artist.id)

            result = query.first()

            if not result:
                return {"error": f"No se ha encontrado el artista"}

            artist = repr(result)

            return artist
        except Exception as e:
            return {"error": f"Error al obtener el artista: {e}"}


def create_artist(artist: ArtistModel):
    with session as db:
        try:
            artist = Artist(name=artist.name,
                            country=artist.country, born_year=artist.born_year)
            db.add(artist)
            db.commit()
            db.refresh(artist)
        except Exception as e:
            return {"error": f"Error al crear el artista: {e}"}
        return artist


def update_artist(artist_id, changes):
    for field in changes.keys():
        if field in not_modifiable_fields:
            return {"error": f"El campo '{field}' no se puede modificar"}
        if not hasattr(Artist, field):
            return {"error": f"El campo '{field}' no existe en la tabla Artist"}

    with session as db:
        try:
            db_artist = db.query(Artist).filter(Artist.id == artist_id).first()
            if not db_artist:
                return None

            for field, value in changes.items():
                setattr(db_artist, field, value)
            db.commit()
            db.refresh(db_artist)
        except Exception as e:
            return {"error": f"Error al crear el artista: {e}"}
        return db_artist


def delete_artist(artist_id):
    with session as db:
        try:
            db_artist = db.query(Artist).filter(Artist.id == artist_id).first()
            if not db_artist:
                return None
            if db_artist.songs:
                return {"error": f"No se puede eliminar el artista {db_artist.name} porque tiene canciones asociadas"}
            db.delete(db_artist)
            db.commit()
        except Exception as e:
            return {"error": f"Error al eliminar el artista: {e}"}
        return artist_id
