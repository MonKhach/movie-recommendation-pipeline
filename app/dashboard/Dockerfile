# Use the official lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements from root directly
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the dashboard directory contents into the container
COPY app/dashboard .

# Expose the default Streamlit port
EXPOSE 8501

# Run the Streamlit application (Change dashboard.py if your main file has a different name)
CMD ["streamlit", "run", "frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]