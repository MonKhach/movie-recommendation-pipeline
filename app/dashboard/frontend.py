import streamlit as st
import requests

# Backend API base URL
BACKEND_URL = "http://127.0.0.1:8000"

# Configure the Streamlit page layout and title
st.set_page_config(page_title="Movie Recommendation System", layout="wide")
st.title("🎬 Movie Recommendation & Rating Analysis Dashboard")

# Fetch supported movie genres from the FastAPI backend dynamically
try:
    genres_res = requests.get(f"{BACKEND_URL}/api/genres").json()
    genre_dict = {g["name"]: g["name"] for g in genres_res.get("genres", [])}
except Exception:
    st.error("Could not connect to the FastAPI backend. Please make sure the server is running.")
    genre_dict = {}

# Sidebar control panel setup for user inputs
st.sidebar.header("Filter Options")
selected_genres = st.sidebar.multiselect("Select Genre(s):", list(genre_dict.keys()))
min_rating = st.sidebar.slider("Minimum Rating:", 1.0, 10.0, 7.0, 0.1)
min_votes = st.sidebar.number_input("Minimum Vote Count:", value=500, step=50)
limit = st.sidebar.slider("Number of Movies to Display:", 1, 20, 10)

# Process logic when the action button is clicked
if st.sidebar.button("Get Recommendations"):
    if not selected_genres:
        st.warning("Please select at least one genre before submitting.")
    else:
        # Format selected genres into a comma-separated string for the API parameter
        genres_str = ",".join(selected_genres)
        params = {
            "genres": genres_str,
            "min_rating": min_rating,
            "min_votes": min_votes,
            "limit": limit
        }
        
        # Display a loading spinner while fetching recommendations from the backend
        with st.spinner("Analyzing movie metrics and calculating statistical scores..."):
            res = requests.get(f"{BACKEND_URL}/api/recommendations", params=params)
            
            if res.status_code == 200:
                data = res.json()
                movies = data.get("movies", [])
                
                if not movies:
                    st.info("No movies found matching the selected criteria.")
                
                # Render the ranked results in a structured container format
                for idx, movie in enumerate(movies, start=1):
                    with st.container():
                        st.subheader(f"{idx}. 🍿 {movie['title']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"⭐️ **Rating:** {movie['rating']:.2f} / 10")
                            st.write(f"📅 **Release Date:** {movie['release_date']}")
                        with col2:
                            st.write(f"🗳️ **Total Votes:** {movie['vote_count']}")
                        
                        # Add a visual separator between movie items
                        st.markdown("---")
            else:
                st.error("Failed to retrieve recommendations from the server. Check your backend logs.")