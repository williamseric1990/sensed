#!/bin/sh

sudo apt-get install git python3 python3-pip
git clone https://github.com/sli/sensed
cd sensed
sudo pip3 install -r requirements.txt
