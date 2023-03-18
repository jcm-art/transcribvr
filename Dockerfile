# Fetch ubuntu 18.04 LTS docker image
FROM ubuntu:18.04
SHELL ["/bin/bash", "-c"] 

# Build commands (for a clean docker build with no cacheing): 
# docker build --no-cache -t transcbvr-ubuntu18.04 .

# Build commands (to update docker build): 
# For M2 Mac: 
#   docker build -t transcbvr-ubuntu18.04 .
# For circle CI: 
#   Images built using the circle CI pipeline, imformation in config.yml

# Run command:
# docker run -it --mount type=bind,src="$(pwd)",target=/src/transcribvr/ transcbvr-ubuntu18.04 bash

ENV DEBIAN_FRONTEND=noninteractive 

# Update apt, and install Java + curl + wget on your ubuntu image.
RUN apt-get update \
    && apt-get install -y curl \
    && apt-get install -y vim \
    && apt-get install -y python3.8 python3.8-dev python3.8-distutils python3.8-venv \
    && apt-get install -y python3-pip \
    && apt-get install -y git \
    && apt-get install -y python3-numpy


RUN \
  update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

RUN \
  pip3 install --upgrade pip
  
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN \
  apt-get install -y ffmpeg

RUN \
  export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1


# COPY .transcbvr /src/transcribvr/
# Attempt to avoid copy, run though config.yml

#To get updated requirements from pip3: pip3 freeze > requirements.txt

# TODO - should be fixed
#Error - Currently must run the following to get docker working:
#  source ~/.bashrc
#   export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1
