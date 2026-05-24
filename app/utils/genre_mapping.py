GENRE_NAME_TO_ID = {
    "Action": 28,
    "Adventure": 12,
    "Animation": 16,
    "Comedy": 35,
    "Crime": 80,
    "Documentary": 99,
    "Drama": 18,
    "Family": 10751,
    "Fantasy": 14,
    "History": 36,
    "Horror": 27,
    "Music": 10402,
    "Mystery": 9648,
    "Romance": 10749,
    "Science Fiction": 878,
    "TV Movie": 10770,
    "Thriller": 53,
    "War": 10752,
    "Western": 37,
}


def get_genre_ids(genre_names):
    genre_ids = []
    invalid_genres = []

    for genre in genre_names:
        normalized_genre = genre.strip().title()

        if normalized_genre in GENRE_NAME_TO_ID:
            genre_ids.append(GENRE_NAME_TO_ID[normalized_genre])
        else:
            invalid_genres.append(genre)

    return genre_ids, invalid_genres

def get_supported_genres():
    genres = []
    for genre_name, genre_id in sorted(GENRE_NAME_TO_ID.items()):
        genres.append(
            {
                'name': genre_name,
                'id': genre_id
            }
        )
    return genres