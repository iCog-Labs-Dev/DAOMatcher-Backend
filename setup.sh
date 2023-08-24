#!/bin/bash

cleanup() {
    echo -e "\nCleaning up..."
    if [ -n "$llm_pid" ]; then
        kill -TERM "$llm_pid"
    fi
    if [ -n "$app_pid" ]; then
        kill -TERM "$app_pid"
    fi
    deactivate
    echo "Servers Terminated"
    exit 0
}

trap cleanup SIGINT

echo "Setting up environment"

python3 -m venv Backend
source Backend/bin/activate     

echo "Installing requirements"
pip -q install -r requirements.txt

echo "Starting LLM server on port 5001"
python3 -m src.LLM.LLMServer.py & 
llm_pid=$!

echo "Starting App server on port 5000"
python3 app.py &
app_pid=$!

wait