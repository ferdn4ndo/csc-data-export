FROM python:3-alpine

LABEL maintaner="Fernando Constantino <const.fernando@gmail.com>"
LABEL org.opencontainers.image.authors="const.fernando@gmail.com"
LABEL version="1.0"
LABEL description="A customized data export tool (for a legacy system) using Python+MySQL"

# Based on https://www.caktusgroup.com/blog/2017/03/14/production-ready-dockerfile-your-python-django-app/

# Setting PYTHONUNBUFFERED to a non empty value ensures that the python output is sent straight to terminal (e.g. your
# container log) without being first buffered and that you can see the output of your application (e.g. django logs) in
# real time. This also ensures that no partial output is held in a buffer somewhere and never written in case the python
# application crashes.
# Font: https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /code/
WORKDIR /code/

# Copy in your requirements file
ADD requirements.txt /code/requirements.txt

ENV LIBRARY_PATH=/lib:/usr/lib

RUN set -ex \
  && apk add --no-cache --virtual .build-deps \
     gcc \
     musl-dev \
     zlib-dev \
     py-pip \
  && apk add --no-cache \
     build-base \
     mariadb-connector-c-dev \
  && apk add --no-cache \
      --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
      --repository http://dl-cdn.alpinelinux.org/alpine/edge/community \
  && python -m pip install -U --force-reinstall pip \
  && pip install --no-cache-dir -r /code/requirements.txt \
  && apk --purge del .build-deps \
  && rm -rf /tmp/requirements.txt

WORKDIR /code/src/

ADD ./src/ /code/src/

CMD ["./entrypoint.sh"]
