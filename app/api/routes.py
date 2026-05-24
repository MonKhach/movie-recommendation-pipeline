from fastapi import APIRouter, Query, HTTPException

from app.services.movie_api import fetch_movies_by_genres
from app.utils.genre_mapping import get_genre_ids, get_supported_genres
from app.schemas import RecommendationResponse, GenreListResponse

router = APIRouter()

@router.get(
        "/genres", 
        response_model=GenreListResponse,
        summary='Get supported movie genres',
        description='Returns the list of supported movies and their TMDB genre IDs.',
)
def get_genres():
    return {
        'genres': get_supported_genres()
    }

@router.get(
        "/recommendations", 
        response_model=RecommendationResponse,
        summary='Get movie recommendations',
        description=(
            'Returns recommended movies based on the selected genres, minimum rating,'
            'minimum vote count, result limit, and number of TMDB pages to fetch.'
        ),
)
async def get_recommendations(
    genres: str = Query(..., description="Comma-separated movie genres, for example: Action,Comedy"),
    min_rating: float = Query(7.0, ge=0, le=10),
    min_votes: int = Query(500, ge=0),
    limit: int = Query(10, ge=1, le=50),
    pages: int = Query(1, ge=1, le=5),
):
    selected_genres = [
        genre.strip().title()
        for genre in genres.split(",")
        if genre.strip()
    ]

    genre_ids, invalid_genres = get_genre_ids(selected_genres)

    if invalid_genres:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Some genres are not supported.",
                "invalid_genres": invalid_genres,
                "supported_genres_endpoint": "/api/genres"
            },
        )

    try:
        movies = await fetch_movies_by_genres(
            genre_ids=genre_ids,
            min_rating=min_rating,
            min_votes=min_votes,
            pages=pages,
        )
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail={
                'message': 'Failed to fetch data from external movie API.',
                'error': str(error)
            },
        )

    simplified_movies = []

    for movie in movies[:limit]:
        simplified_movies.append(
            {
                "title": movie.get("title"),
                "rating": movie.get("vote_average"),
                "vote_count": movie.get("vote_count"),
                "release_date": movie.get("release_date"),
                "genre_ids": movie.get("genre_ids"),
            }
        )

    return {
        "selected_genres": selected_genres,
        "genre_ids": genre_ids,
        "count": len(simplified_movies),
        "movies": simplified_movies,
    }