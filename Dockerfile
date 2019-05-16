FROM python:3-onbuild
MAINTAINER sprumin <sprumin123@gmail.com>

EXPOSE 8000

RUN pip install -r requirements.txt
RUN chmod +x docker-entrypoint.sh

CMD ["/bin/bash", "docker-entrypoint.sh"]
