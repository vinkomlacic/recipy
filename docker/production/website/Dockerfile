FROM nginx:alpine

COPY ./docker/production/website/default.conf /etc/nginx/conf.d/default.conf

ADD ./website /var/www/html
