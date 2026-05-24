import pandas as pd
import numpy as np

def rank_movies(movies: list, limit: int = 10) -> list:
    """
    Takes a raw list of movies, cleans the data, calculates a custom score, 
    and returns the top ranked movies.
    """
    if not movies:
        return []
        
    # 1. Create a pandas DataFrame for easier data manipulation
    df = pd.DataFrame(movies)
    
    # 2. Data Cleaning
    # Check if 'rating' and 'vote_count' columns exist in the data
    if 'rating' not in df.columns or 'vote_count' not in df.columns:
        return movies[:limit]
        
    # Drop movies that have missing (NaN) or zero values for rating or votes
    df = df.dropna(subset=['rating', 'vote_count'])
    df = df[(df['rating'] > 0) & (df['vote_count'] > 0)]
    
    if df.empty:
        return []

    # 3. Calculate the custom score (Scoring)
    # Normalize the rating (TMDB rating is 0-10, we scale it to 0-1)
    normalized_rating = df['rating'] / 10.0
    
    # Apply log transformation to vote_count to handle outliers 
    # (prevents movies with 1M votes from completely dominating movies with 1K votes)
    log_votes = np.log1p(df['vote_count'])
    
    # Min-Max normalize the log-transformed votes (scale to 0-1)
    min_log_votes = log_votes.min()
    max_log_votes = log_votes.max()
    
    if max_log_votes == min_log_votes:
        normalized_log_votes = 0.0
    else:
        normalized_log_votes = (log_votes - min_log_votes) / (max_log_votes - min_log_votes)
        
    # Final formula: 70% weight to the movie's rating, 30% weight to its popularity (votes)
    df['score'] = (normalized_rating * 0.7) + (normalized_log_votes * 0.3)
    
    # 4. Sort and filter
    # Sort by the calculated score in descending order and keep the top 'limit' movies
    df = df.sort_values(by='score', ascending=False)
    top_movies = df.head(limit)
    
    # 5. Return the result as a standard list of dictionaries
    # Drop the temporary 'score' column as it's not needed in the API response
    top_movies = top_movies.drop(columns=['score'])
    return top_movies.to_dict(orient='records')