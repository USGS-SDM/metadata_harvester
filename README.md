# metadata_harvester

This repository contains **Dockerfile** of [metadata_harvesting](https://github.com/USGS-SDM/metadata_harvester) 
for [Docker](https://www.docker.com/)'s [automated build](https://registry.hub.docker.com/r/tudor_garbulet/metadata_harvester/) 
published to the public [Docker Hub Registry](https://registry.hub.docker.com/).

## Informations

Metadata_harvester is a collection of scripts that handle the harvesting of USGS metadata from different providers
* Based on Python 3 official Image [python:3](https://hub.docker.com/_/python/)
* Install [Docker](https://www.docker.com/)

## Run image from docker hub

    docker run -dti tudorgarbulet/metadata_harvester

## Build from source

Clone github repo:

    git clone https://github.com/USGS-SDM/metadata_harvester
    cd metadata_harvester
    docker build -t "metadata_harvester" .
    docker run -dti metadata_harvester

## Usage

You can ssh into the running container by running the following:

    docker exec -it <image_hash> /bin/bash

To get the image hash, run `docker ps`.
