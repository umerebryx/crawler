FROM ubuntu:14.04
RUN apt-get update
RUN apt-get -y install wget
RUN apt-get install -y python python-dev python-distribute python-pip
RUN apt-get -y install git
WORKDIR /home/ubuntu/experiment
RU git clone https://github.com/umerebryx/crawler.git
RUN pip install -r requirements.txt
