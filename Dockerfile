# syntax=docker/dockerfile:1
# escape=`

#Base image
FROM python:3.12-slim

# System libs 
RUN apt-get update `
    && apt-get install -y --no-install-recommends build-essential `
    && rm -rf /var/lib/apt/lists/*

#Install python packages and dependencies 
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

# Copy project code
COPY . . 

# Expose streamlit port
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"]

