# Fetch ubuntu 18.04 LTS docker image
FROM ubuntu:18.04

#build command: docker run -it --mount type=bind,src="$(pwd)",target=/src/app/ ubuntu /bin/bash

ENV DEBIAN_FRONTEND=noninteractive 
#COPY Transcribvr.py /etc/app/Transcribvr.py

#uncomment this line to find the fastest ubuntu repository at the time. Probably overkill, so disabling for now
#Note that this functionality is untested and might need debugging a bit.

# Update apt, and install Java + curl + wget on your ubuntu image.
RUN \
  apt-get update

RUN \
  apt-get install -y curl

RUN \
  apt-get install -y vim

RUN \  
  apt-get install -y python3.8 python3.8-dev python3.8-distutils python3.8-venv

RUN \
  update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

RUN \  
  apt-get install -y python3-pip

RUN \
  pip3 install --upgrade pip

RUN \  
  apt-get install -y git

RUN \ 
  pip3 install --upgrade setuptools

RUN \
  pip3 install Cython

RUN \
  apt-get install -y python3-numpy

RUN \ 
  pip3 install setuptools-rust

RUN \
  pip3 install torch==1.9.0 -f https://download.pytorch.org/whl/torch_stable.html

RUN \
  pip3 install git+https://github.com/openai/whisper.git

RUN \ 
  pip3 install jiwer

RUN \ 
  pip3 install pandas

RUN \
  pip install -U torch torchaudio --no-cache-dir

#RUN \
#  source ~/.bashrc

SHELL ["/bin/bash", "-c"] 

RUN \
  export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1

#COPY requirements.txt requirements.txt
#RUN pip3 install -r requirements.txt