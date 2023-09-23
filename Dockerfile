# Use the official Python image as the base image
FROM python:3.10

# Set environment variables
ENV PORT1=8000

# Create a working directory
WORKDIR /app

# Copy your Flask apps into the container
COPY app.py /app
COPY src/LLM/ /app/src/LLM/
COPY src/Scraping/ /app/src/Scraping/
COPY src/ServerLogic/ /app/src/ServerLogic/
COPY .env /app/

# Copy your Bash script into the container
COPY setup.sh /app
COPY requirements.txt /app

# Make the Bash script executable
RUN chmod +x setup.sh

# Expose the ports on which the Flask apps will run
EXPOSE $PORT1

# Define the command to run both Flask apps
CMD ["/bin/bash","-c","source .env && ./setup.sh"]