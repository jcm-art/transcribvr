# Fetch ubuntu 18.04 LTS docker image
FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive 
COPY Transcribvr.py /etc/app/Transcribvr.py

#uncomment this line to find the fastest ubuntu repository at the time. Probably overkill, so disabling for now
#Note that this functionality is untested and might need debugging a bit.

# Update apt, and install Java + curl + wget on your ubuntu image.
RUN \
  apt-get update && \
  apt-get install -y curl vim wget expect git zip unzip && \
  apt-get install -y openjdk-8-jdk 

RUN \
  apt-get install -y python3 \
  apt-get install -y python3-pip