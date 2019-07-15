FROM nginx:latest
MAINTAINER sprumin <sprumin@gmail.com>

COPY nginx.conf /etc/nginx/nginx.conf
COPY loveseulgi /etc/nginx/sites-available/

RUN mkdir -p /etc/nginx/sites-enabled/\
    && ln -s /etc/nginx/sites-available/loveseulgi /etc/nginx/sites-enabled/loveseulgi

CMD ["nginx", "-g", "daemon off;"]
