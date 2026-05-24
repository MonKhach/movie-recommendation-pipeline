import os
from dotenv import load_dotenv

# 1. Get the absolute path of the directory where this test file is located ('tests' folder)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Go one level up to the application root folder and point exactly to the .env file
env_path = os.path.join(current_dir, "..", ".env")

# 3. Force load environment variables from that specific path BEFORE importing the app
load_dotenv(dotenv_path=env_path)

# Now it is safe to import the app because the environment variables are successfully loaded
from fastapi.testclient import TestClient
from app.main import app

# Create a virtual test client to make requests to our FastAPI app
client = TestClient(app)

def test_home_endpoint():
    """Test the root (Home) endpoint to ensure it runs correctly."""
    response = client.get("/")
    
    # Assert that the status code is 200 OK
    assert response.status_code == 200
    # Assert that the response message matches the expected output
    assert response.json() == {"message": "Movie recommendation API is running"}

def test_genres_endpoint():
    """Test the genres endpoint to ensure it returns supported genres."""
    response = client.get("/api/genres")
    
    # Assert that the status code is 200 OK
    assert response.status_code == 200
    
    data = response.json()
    # Verify that the "genres" key exists in the response JSON
    assert "genres" in data
    # Verify that the list of genres is not empty
    assert len(data["genres"]) > 0

def test_recommendations_endpoint():
    """Test the recommendations endpoint with a valid genre and parameters."""
    response = client.get("/api/recommendations?genres=Comedy&limit=3")
    
    if response.status_code != 200:
        print("\n" + "="*40)
        print("🚨 ERROR DETAILS FROM SERVER 🚨")
        print(response.text)
        print("="*40 + "\n")
    
    # Assert that the status code is 200 OK
    assert response.status_code == 200
    
    data = response.json()
    # Verify that the response contains the "movies" key
    assert "movies" in data
    
    # Check the structure of the returned movies if the list is not empty
    if len(data["movies"]) > 0:
        first_movie = data["movies"][0]
        assert "title" in first_movie
        assert "rating" in first_movie
        assert "vote_count" in first_movie

def test_invalid_genre_endpoint():
    """Verify that requesting an invalid/unsupported genre returns a 400 Bad Request error."""
    
    # We request a non-existent genre, e.g., "AlienGenre123"
    response = client.get("/api/recommendations?genres=AlienGenre123&limit=3")
    
    # Verify that the API does not crash and correctly returns a 400 Bad Request status
    assert response.status_code == 400
    
    # FastAPI usually includes error details in the "detail" key
    data = response.json()
    assert "detail" in data        