# Import the scoring/ranking function from the main application
from app.services.recommender import rank_movies

def test_rank_movies_sorting():
    """Verify that the rank_movies function mathematically sorts the mock list correctly."""
    
    # 1. ARRANGE: Create a mock list of dictionaries with 3 movies
    # We use 'rating' and 'vote_count' to exactly match your recommender.py code
    mock_data = [
        {"id": 1, "title": "Bad Movie", "rating": 3.0, "vote_count": 10},
        {"id": 2, "title": "Great Movie", "rating": 9.5, "vote_count": 5000},
        {"id": 3, "title": "Average Movie", "rating": 6.0, "vote_count": 300}
    ]
    
    # 2. ACT: Call the ranking function by passing the LIST (not a DataFrame)
    ranked_movies = rank_movies(mock_data)
    
    # 3. ASSERT: Check that the result is a list of dictionaries
    assert isinstance(ranked_movies, list)
    assert len(ranked_movies) == 3
    
    # Verify that after sorting, the movie with the highest rating and most votes is first
    first_movie = ranked_movies[0]["title"]
    assert first_movie == "Great Movie", f"Expected 'Great Movie' to be first, but got {first_movie}"
    
    # Verify that the worst movie is at the bottom of the list
    last_movie = ranked_movies[-1]["title"]
    assert last_movie == "Bad Movie", f"Expected 'Bad Movie' to be last, but got {last_movie}"

def test_rank_movies_empty_list():
    """Verify that the function handles empty lists correctly."""
    # ACT
    result = rank_movies([])
    # ASSERT
    assert result == []