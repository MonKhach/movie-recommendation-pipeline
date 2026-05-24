# Use the official lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /code

# Copy requirements from root directly
COPY requirements.txt /code/requirements.txt

# Install the required dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the app directory content into /code/app
COPY app /code/app

# Start the FastAPI server using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]