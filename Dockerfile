# Use the official Python image as the base image
FROM python:3.10

# Set environment variables
ENV PORT1=8000

# Create a working directory
WORKDIR /app

# Copy your Flask apps into the container
COPY . .

# Make the Bash script executable
RUN chmod +x setup.sh

# Expose the ports on which the Flask apps will run
EXPOSE $PORT1

# Define the command to run both Flask apps
CMD ["./setup.sh"]
