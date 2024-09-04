# Use an official Ubuntu runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install Python and other dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip ffmpeg && \
    apt-get clean

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in the requirements file
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port on which FastAPI will run
EXPOSE 8000
