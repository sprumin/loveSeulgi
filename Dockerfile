FROM python:3-onbuild
MAINTAINER sprumin <sprumin123@gmail.com>

EXPOSE 8000

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install uwsgi

RUN chmod +x docker-entrypoint.sh

CMD ["/bin/bash", "docker-entrypoint.sh"]
