#!/bin/bash
apt-get install curl
curl --silent --location http://deb.nodesource.com/setup_0.12 | sudo bash -
apt-get install nodejs
npm install
npm install forever -g
