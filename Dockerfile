# Use the official Python image as the base image
FROM python:3.11.5-slim-bookworm

ENV YOUR_ENV=PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=1.8.2

# System dependencies
RUN apt-get update && apt-get install -y python3-pip
RUN pip install poetry

# Set environment variables
ENV PORT1=8000

# Create a working directory
WORKDIR /app
# Copy other files to the working directory
COPY . .

# Installing packages
RUN poetry install

# Make the Bash script executable
RUN chmod +x setup.sh

# Expose the ports on which the Flask apps will run
EXPOSE $PORT1

# Define the command to run both Flask apps
CMD ["./setup.sh"]
