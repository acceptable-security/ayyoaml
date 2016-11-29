#!/bin/bash

echo "~ Installing ayyoa.ml! ~"

if [[ $(id -u) -ne 0 ]] ; then echo "Please run as root" ; exit 1 ; fi

echo "~ Getting dependencies ~"
sudo apt-get install -y make git tar
sudo apt-get install -y libpcre3-dev libpcre++-dev libssl-dev
sudo apt-get install -y python-setuptools python-pip
sudo pip install flask


echo "~ Downloading nginx 1.11.6 ~"
sudo wget -P /tmp http://nginx.org/download/nginx-1.11.6.tar.gz
sudo tar -zxvf /tmp/nginx-1.11.6.tar.gz -C /tmp

echo "~ Downloading nginx-rtmp-module ~"
sudo git clone https://github.com/arut/nginx-rtmp-module.git /tmp/rtmpmod

echo "~ Compiling nginx ~"
cd /tmp/nginx-1.11.6
./configure --add-module=../rtmpmod/ \
            --with-http_ssl_module \
            --user=nginx \
            --group=nginx \
            --prefix=/usr/local/nginx \
            --sbin-path=/usr/local/nginx/nginx \
            --conf-path=/usr/local/nginx/nginx.conf \
            --pid-path=/usr/local/nginx/nginx.pid \
sudo make
sudo make install

echo "~ Creating an nginx user ~"
sudo adduser --system --no-create-home --disabled-login --disabled-password --group nginx

echo "~ Loading the nginx configuration ~"
sudo cp nginx/nginx.conf /etc/nginx/nginx.conf

echo "~ Loading the systemd sevice ~"
sudo cp nginx/nginx.service /lib/systemd/system/nginx.service
sudo chmod +x /lib/systemd/system/nginx.service

echo "~ Loading the http page ~"
sudo mkdir -p /var/www/http
sudo cp -v -r http/* /var/www/http

echo "~ Loading the authentication server ~"
sudo mkdir -p /var/www/auth
sudo cp -v -r auth/* /var/www/auth

echo "Process complete ;w;"
echo "To launch, use the ./start.sh script"
chmod +x ./start.sh
