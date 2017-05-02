#!/bin/sh

sudo rm /etc/nginx/sites-enabled/default
sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/nginx.conf
sudo service nginx restart

sudo ln -sf /home/box/web/etc/hello.py /etc/gunicorn.d/hello.py
sudo ln -sf /home/box/web/etc/hello.wsgi /etc/gunicorn.d/hello.wsgi
sudo service gunicorn start

