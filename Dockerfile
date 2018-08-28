# Latest Ubuntu LTS
FROM ubuntu:18.10

MAINTAINER Sebastien Williams-Wynn "s.williamswynn.mail@gmail.com"

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ENV TERM=xterm-256color

RUN apt-get update
RUN apt-get install -y \
        python3 \
        python3-dev \
        python3-pip \
        build-essential

COPY . /scap-registry
WORKDIR /scap-registry

RUN python3 setup.py install

# Specify the application configurations
ENV APP_ENV=dev

EXPOSE 5000

CMD scap-registry
