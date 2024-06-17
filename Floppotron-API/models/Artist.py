from pydantic import BaseModel
from typing import Union


class Artist(BaseModel):
    name: str
    country: Union[str, None] = None
    born_year: Union[int, None] = None

    def __repr__(self):
        return f"Artist {self.name} from {self.country} born in {self.born_year}"
