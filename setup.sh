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


trap cleanup SIGINT

echo "Installing requirements..."
pip install -r requirements.txt
echo "Starting LLM server on port $LLM_PORT"
python3 -m src.LLM.LLMServer & 
llm_pid=$!

echo "Starting App server on port $PORT"
gunicorn 'app:create_app()' --worker-class gevent --bind 0.0.0.1:$PORT &
app_pid=$!

wait
