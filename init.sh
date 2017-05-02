#!/bin/sh

sudo rm /etc/nginx/sites-enabled/default
sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/nginx.conf
sudo service nginx restart

sudo ln -sf /home/box/web/etc/hello.wsgi /etc/gunicorn.d/hello.wsgi
sudo ln -sf /home/box/web/etc/qa.wsgi /etc/gunicorn.d/qa.wsgi

sudo service gunicorn start


