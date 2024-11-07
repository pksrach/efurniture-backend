#!/bin/bash

CONTAINER=efurniture-backend
TAG=latest
IMAGE="pksrach/$CONTAINER:$TAG"

docker build -t $IMAGE .