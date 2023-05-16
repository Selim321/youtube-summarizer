# Use an official Python runtime as a parent image
FROM python:3.11.3-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app

# Expose port 8000 for the FastAPI app to listen on
EXPOSE 8000

# Start the FastAPI app when the container launches
CMD uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
