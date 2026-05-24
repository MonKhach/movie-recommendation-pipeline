import aiohttp

from app.config import TMDB_ACCESS_TOKEN, TMDB_BASE_URL


async def fetch_movie_page(session, genre_ids, min_rating, min_votes, page):
    url = f"{TMDB_BASE_URL}/discover/movie"

    params = {
        "with_genres": ",".join(str(genre_id) for genre_id in genre_ids),
        "vote_average.gte": min_rating,
        "vote_count.gte": min_votes,
        "sort_by": "vote_average.desc",
        "page": page,
        "include_adult": "false",
        "language": "en-US",
    }

    async with session.get(url, params=params) as response:
        response.raise_for_status()
        return await response.json()


async def fetch_movies_by_genres(genre_ids, min_rating, min_votes, pages):
    if not TMDB_ACCESS_TOKEN:
        raise ValueError("TMDB_ACCESS_TOKEN is missing. Please add it to your .env file.")

    headers = {
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}",
        "accept": "application/json",
    }

    all_movies = []

    async with aiohttp.ClientSession(headers=headers) as session:
        for page in range(1, pages + 1):
            data = await fetch_movie_page(
                session=session,
                genre_ids=genre_ids,
                min_rating=min_rating,
                min_votes=min_votes,
                page=page,
            )

            movies = data.get("results", [])
            all_movies.extend(movies)

    return all_movies