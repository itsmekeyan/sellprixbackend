#!/bin/bash

# Check if we're in production environment first
if [ "$ENVIRONMENT" = "production" ]; then
    # Load production environment file
    if [ -f ".env" ]; then
        echo "Loading production environment variables..."
        source .env
    else
        echo "Warning: .env file not found!"
        exit 1
    fi
else
    # Load development environment file
    if [ -f ".env.dev" ]; then
        echo "Loading development environment variables..."
        source .env.dev
    else
        echo "Warning: .env.dev file not found!"
        exit 1
    fi
fi

# Additional common environment variables
export APP_NAME="sellprix_backend"
export LOG_LEVEL="INFO"

echo "Starting server in ${ENVIRONMENT:-production} mode..."

# Start the FastAPI server using the same command as Dockerfile
python -m fast_api
