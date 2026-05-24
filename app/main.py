from fastapi import FastAPI
from app.api.routes import router as movie_router

app = FastAPI(
    title = 'Movie Recommendation API',
    description = 'High-performance movie recommendation and rating analysis pipline',
    version = '1.0.0'
)

@app.get('/')
def home():
    return {
        'message': 'Movie recommendation API is running'
    }

app.include_router(movie_router, prefix = '/api', tags = ['Movies'])