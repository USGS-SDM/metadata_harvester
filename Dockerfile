# VERSION 1.0.0
# AUTHOR: Tudor Garbulet
# DESCRIPTION: Collection of scripts that handle the harvesting of USGS metadata from different providers
# BUILD: docker build --rm -t tudorgarbulet/metadata_harvester .
# SOURCE: https://github.com/USGS-SDM/metadata_harvester

FROM python:3
MAINTAINER USGS-SDM

# Create and set the working directory to /data
RUN mkdir /data
RUN mkdir /data/harvesting_logs
WORKDIR /data

COPY requirements.txt ./
COPY harvestWAF.sh ./
COPY harvestWAF.py ./
COPY getwebdir.py ./

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get -y install cron
RUN apt-get update && apt-get -y install nano
RUN apt-get update && apt-get -y install vim

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/harvest-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/harvest-cron

# Apply cron job
RUN crontab /etc/cron.d/harvest-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log


