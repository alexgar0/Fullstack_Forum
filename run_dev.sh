#!/bin/bash

# Stop on Ctrl+c
cleanup() {
    echo -e "\nStopping services"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    sudo docker compose stop postgres
    echo "Stopped"
    exit
}

trap cleanup SIGINT

# Run DB
sudo docker compose up -d postgres

echo "Waiting for DB"
until [ "$(sudo docker inspect -f '{{.State.Health.Status}}' postgres_container)" == "healthy" ]; do
    sleep 1
done

# Run backend
source ./backend/.venv/bin/activate
start & 
BACKEND_PID=$!

# Run frontend
cd ./frontend/
npm run dev &
FRONTEND_PID=$!

wait