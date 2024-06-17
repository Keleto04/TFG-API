from pydantic import BaseModel
from typing import Union


class Song(BaseModel):
    name: str
    artist_id: Union[int, None] = None
    created_year: Union[int, None] = None
    format_type: Union[str, None] = None
    duration: Union[float, None] = None
    path: str

    def __repr__(self):
        return f"Song {self.name} by {self.artist_id} created in {self.created_year} in format {self.format_type} with duration {self.duration} and path {self.path}"
