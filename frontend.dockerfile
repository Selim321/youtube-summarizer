# Base image
FROM python:3.11.3-slim-buster

# Set working directory
WORKDIR /app

# Copy dependencies file
COPY requirements.txt .

# Install dependencies
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy app files
COPY . /app

# Set environment variable
ENV STREAMLIT_SERVER_PORT 8501

# Expose port
EXPOSE 8501

# Start Streamlit app
ENTRYPOINT ["streamlit", "run", "frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]
