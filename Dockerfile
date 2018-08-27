# Latest Ubuntu LTS
FROM ubuntu:18.10

MAINTAINER Sebastien Williams-Wynn "s.williamswynn.mail@gmail.com"

RUN apt-get update
RUN apt-get install -y \
        python3 \
        python3-dev \
        python3-pip \
        build-essential

COPY . /scap-registry
WORKDIR /scap-registry

ENV APP_ENV dev
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN python3 setup.py install

ENV FLASK_APP=scap_registry/app.py

EXPOSE 5000

CMD python3 -m flask run
