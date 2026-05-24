from typing import List, Optional
from pydantic import BaseModel

class MovieResponse(BaseModel):
    title: Optional[str]
    rating: Optional[float]
    vote_count: Optional[int]
    release_date: Optional[str]
    genre_ids: List[int]

class RecommendationResponse(BaseModel):
    selected_genres: List[str]
    genre_ids: List[int]
    count: int
    movies: List[MovieResponse]

class ErrorResponse(BaseModel):
    message: str

class GenreResponse(BaseModel):
    name: str
    id: int

class GenreListResponse(BaseModel):
    genres: List[GenreResponse]


