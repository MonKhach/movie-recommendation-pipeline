# Movie Recommendation & Rating Analysis Dashboard

A Full-Stack Movie Recommendation application built with Python. It utilizes **FastAPI** for the backend API, **Streamlit** for the interactive frontend dashboard, and **Docker Compose** for seamless containerization and local development. The system fetches live data from **The Movie Database (TMDB) API** and processes recommendations using **Pandas**.

## 🚀 Features
* **Interactive Dashboard:** Filter movies by genre, minimum rating, and minimum vote count.
* **FastAPI Backend:** High-performance REST API endpoints for fetching genres and recommendations.
* **Data Pipelines:** Integrated with TMDB API for up-to-date movie metadata.
* **Dockerized Architecture:** Easily run the entire stack with a single command.

---

## 🛠️ Project Structure
```text
movie-recommendation-pipeline/
├── app/                  # FastAPI Backend source code
│   ├── api/              # API routes and endpoints
│   ├── dashboard/        # Streamlit Frontend source code
│   ├── services/         # Core logic (TMDB client & recommender)
│   └── utils/            # Helper functions (genre mapping, config)
├── tests/                # Unit & Integration tests (pytest)
├── .env                  # Environment variables (TMDB Token)
├── docker-compose.yml    # Docker Compose configuration
└── requirements.txt      # Python dependencies