#!/bin/bash
apt-get install curl
curl --silent --location http://deb.nodesource.com/setup_0.12 | sudo bash -
apt-get install nodejs
cp ./config/config.sample.json config.json
npm install
npm install forever -g
echo 'Update config/config.json to reflect this installation.'
