#!/usr/bin/env bash

# Build image
docker build --tag=alonmar/mlops-value_fifa_players . 

# List docker images
docker image ls

# Run flask app
docker run -p 127.0.0.1:8080:8080 alonmar/mlops-value_fifa_players
