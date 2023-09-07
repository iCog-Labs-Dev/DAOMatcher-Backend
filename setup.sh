#!/bin/bash

cleanup() {
    echo -e "\nCleaning up..."
    if [ -n "$llm_pid" ]; then
        kill -TERM "$llm_pid"
    fi
    if [ -n "$app_pid" ]; then
        kill -TERM "$app_pid"
    fi
    if [ -n "$redis_pid" ]; then
        kill -TERM "$redis_pid"
    fi
    deactivate
    echo "Servers Terminated"
    exit 0
}

# Function to check if Redis is installed
check_redis_installed() {
    if [ -x "$(command -v redis-server)" ]; then
        return 0
    else
        return 1
    fi
}

# Function to install Redis
install_redis() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS using Homebrew
        brew install redis -q
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux using APT (Debian/Ubuntu)
        sudo apt-get update -q
        sudo apt-get install -y redis-server
    else
        echo "Unsupported operating system: $OSTYPE install redis-server manually and try running this script again"
        exit 1
    fi
}


trap cleanup SIGINT

echo "Setting up environment"

python3 -m venv Backend
source Backend/bin/activate     

echo "Installing requirements"
pip -q install -r requirements.txt

# Check if Redis is installed
if check_redis_installed; then
    echo "Redis is already installed."
else
    echo "Redis is not installed. Installing Redis..."
    install_redis
    wait
fi

echo "Starting LLM server on port 5001"
python3 -m src.LLM.LLMServer & 
llm_pid=$!

echo "Starting App server on port 5000"
python3 app.py &
app_pid=$!

# Start Redis server
echo "Starting Redis server..."
redis-server --port 5002 &
redis_pid=$!

wait