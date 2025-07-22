#!/bin/bash

APP_NAME="teapot-api"
IMAGE_NAME="teapot-api"

# # Build the Docker image
docker build -t $IMAGE_NAME .

# # Stop and remove the existing container
docker rm -f $APP_NAME 2>/dev/null

# Run the new container
docker run -d \
    --name $APP_NAME \
    --env-file .env \
    -p 8080:80 \
    $IMAGE_NAME
