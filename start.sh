#!/bin/bash

# Source the configuration file
source ./config.local.conf

# Add NPM_PATH to the PATH environment variable
export PATH=$PATH:$NPM_PATH

# Change to the directory containing this script
cd "$(dirname "$0")" || exit

# Function to check if Nginx is running
is_nginx_running() {
    pgrep -x nginx >/dev/null
}

# Stop Nginx if it's running
if is_nginx_running; then
    echo "Stopping existing Nginx process..."
    sudo nginx -s stop
    sleep 2
fi

# Start Nginx with the custom config
echo "Starting Nginx..."
sudo nginx -c "$(pwd)/proxy/nginx.conf"

# Change to the ui directory
cd ./ui || exit

# Start the React app using Vite on port 6000
npm run dev -- --port 6000 &

# Store the process ID of the Vite dev server
VITE_PID=$!

# Wait for the Vite dev server to start (adjust sleep time if needed)
sleep 2

echo "React app started on port 6000 with PID: $VITE_PID"

# Change to the app directory
cd ../app || exit

# Activate the virtual environment
source venv/bin/activate

# Start the Flask app in the background
python app.py &

# Store the process ID of the Flask app
FLASK_PID=$!

# Wait for the Flask app to start (adjust sleep time if needed)
sleep 2

echo "Flask app started on port 5000 with PID: $FLASK_PID"

cd docs
python serve_docs.py &

DOCS_PID=$!

sleep 2

echo "DOCS app started on port 7000 with PID: $DOCS_PID"

# Function to stop processes
stop_processes() {
    echo "Stopping processes..."
    
    # Stop Flask app
    if [ -n "$FLASK_PID" ]; then
        echo "Stopping Flask app (PID: $FLASK_PID)"
        kill $FLASK_PID
    fi

    if [ -n "$DOCS_PID" ]; then
        echo "Stopping Docs app (PID: $DOCS_PID)"
        kill $DOCS_PID
    fi
    
    # Stop React app
    if [ -n "$VITE_PID" ]; then
        echo "Stopping React app (PID: $VITE_PID)"
        kill $VITE_PID
    fi
    
    # Stop Nginx
    if is_nginx_running; then
        echo "Stopping Nginx..."
        sudo nginx -s stop
    fi
}

# Set up trap to stop all processes when the script is terminated
trap 'stop_processes' EXIT INT TERM

# Keep the script running
wait $FLASK_PID $VITE_PID $DOCS_PID