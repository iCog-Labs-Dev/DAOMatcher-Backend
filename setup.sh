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
echo "Setting up environment"

# echo "Installing Poetry"
# pip install poetry

# echo "Installing requirements..."
# poetry install

# echo "Activating environment"
# poetry shell

echo "Migrating database to latest version"
flask db stamp head
flask db migrate
flask db upgrade

echo "Starting LLM server on port 5001"
gunicorn -w 1 'src.globals:llm_app' --timeout 180 --bind 127.0.0.1:5001 &
# python3 -m src.LLM.LLMServer &
llm_pid=$!

echo "Starting App server on port 8000"
gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 2 'app:create_app()' --timeout 180 &
app_pid=$!

wait
