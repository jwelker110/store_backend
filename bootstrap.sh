#! /usr/bin/env bash

# make sure we have the req packages
sudo apt-get update
sudo apt-get install -y python-pip python-dev libffi-dev nginx build-essential curl git m4 ruby texinfo libbz2-dev libcurl4-openssl-dev libexpat-dev libncurses-dev zlib1g-dev
# use pip to install
sudo pip install virtualenv