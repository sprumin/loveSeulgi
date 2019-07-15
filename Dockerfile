FROM python:3-onbuild
MAINTAINER sprumin <sprumin123@gmail.com>
ENV PYTHONUNBUFFERED 1


RUN apt-get -y update
RUN apt-get -y install vim
RUN mkdir /LoveSeulgi

ADD . /LoveSeulgi

WORKDIR /LoveSeulgi

EXPOSE 8000

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install uwsgi
RUN chmod +x docker-entrypoint.sh

CMD ["/bin/bash", "docker-entrypoint.sh"]
