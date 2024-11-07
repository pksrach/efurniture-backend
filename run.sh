#!/bin/bash

# Define environment variables
POSTGRES_HOST="your_host"
POSTGRES_PORT="5432"
POSTGRES_USER="your_usename"
POSTGRES_PASSWORD="your_password"
POSTGRES_DATABASE="efurniture"

CONTAINER=efurniture-backend
TAG=latest
IMAGE="pksrach/$CONTAINER:$TAG"

# Stop container
echo "Remove old container $CONTAINER..."
docker stop $CONTAINER

# Remove old container
docker rm $CONTAINER
echo "Finish remove old container $CONTAINER"

# Pull image
echo "Start pull image $IMAGE..."
docker pull $IMAGE
echo "Finish pull image $IMAGE"

# Run the Docker container
echo "Start run container $CONTAINER..."
docker run --name=$CONTAINER \
  --env=POSTGRES_HOST=$POSTGRES_HOST \
  --env=POSTGRES_PORT=$POSTGRES_PORT \
  --env=POSTGRES_USER=$POSTGRES_USER \
  --env=POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
  --env=POSTGRES_DATABASE=$POSTGRES_DATABASE \
  -p 9000:8000 \
  -d $IMAGE
  
echo "Finish run container $CONTAINER"
