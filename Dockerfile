# Use the official Python image as the base image
FROM python:3.11

#Installing system dependecies
RUN apt-get update && apt-get install -y python3-pip # Install prerequisite packages (adjust based on your system)
RUN pip install poetry

# Set environment variables
ENV PORT1=8000 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=1.8.2

# Create a working directory
WORKDIR /app

# Copy your Flask apps into the container
COPY . .

# Installing packages
RUN poetry install

# Make the Bash script executable
RUN chmod +x setup.sh

# Expose the ports on which the Flask apps will run
EXPOSE $PORT1

# Define the command to run both Flask apps
CMD ["./setup.sh"]
