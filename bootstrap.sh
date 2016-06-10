#! /usr/bin/env bash

# this is going to set up almost everything for us.
# you will still need to create the store_app file and
# place it in /etc/nginx/sites-available/

echo "Starting the provision of this Vagrant machine..."
sudo -u vagrant bash <<EOF
# make sure we have the req packages
sudo apt-get update
sudo apt-get install -y python-pip python-dev libffi-dev nginx build-essential curl git m4 ruby texinfo libbz2-dev libcurl4-openssl-dev libexpat-dev libncurses-dev zlib1g-dev
# use pip to install
sudo pip install virtualenv

# upgrade python
cd /usr/src
sudo wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
sudo tar xzf Python-2.7.10.tgz
sudo ./configure
sudo make altinstall
cd /home/vagrant

# create the backend
# ------------------
echo "Creating the backend..."
echo "-----------------------"
git clone https://github.com/jwelker110/store_backend.git
cd store_backend
git checkout udacity

# setup our virtual environment, install deps
virtualenv --python=/usr/bin/python2.7 store-env
source store-env/bin/activate
pip install -r requirements.txt
# need uwsgi as well
pip install uwsgi

# we need to have a config_secret file
cd store_app/config
mv config_example.py config_secret.py

# let's create our 'secret' key
touch client_secret.json
touch secret_keys.json
echo "{\"JWT_CIPHER\": \"this is the JWT cipher\"}" >> secret_keys.json

echo "Setting up uWSGI and nginx"
echo "--------------------------"
# setup uWSGI according to 
# https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04
cd /home/vagrant
cd store_backend/
sudo mv store_app.conf /etc/init/
sudo start store_app

# remove the default site from nginx please
sudo mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default_copy

cd /home/vagrant
cd store_backend
sudo mv store_app_server /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/store_app_server /etc/nginx/sites-enabled

echo "Creating the frontend now..."
echo "----------------------------"

cd /home/vagrant
git clone https://github.com/jwelker110/store_frontend.git
cd store_frontend
git checkout udacity

echo "About to install npm so go make some food and relax for a bit..."
echo "----------------------------------------------------------------"

# we need to have nodejs installed but the most recent version is
# not going to work
curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g npm
# install npm packages
npm install
sudo npm install -g yo gulp bower

echo "Installing bower deps meow..."
echo "-----------------------------"
# install bower dep
bower install --allow-root

# generate our project for the first time!
echo "Gulp may take some time to run (5 minutes)..."
gulp

sudo service nginx reload
EOF