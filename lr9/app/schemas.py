from pydantic import BaseModel

class MovieBase(BaseModel):
    title: str
    genre: str
    year: int

class MovieCreate(MovieBase):
    pass

class MovieUpdate(BaseModel):
    title: str = None
    genre: str = None
    year: int = None

class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True
