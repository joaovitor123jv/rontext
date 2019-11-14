#!/bin/bash

sudo apt install -y ruby ri ruby-bundler ruby-dev python3-pip

sudo apt install -y make build-essential libssl-dev zlib1g-dev
sudo apt install -y libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm
sudo apt install -y libncurses5-dev libncursesw5-dev xz-utils tk-dev

# echo "deb http://ftp.de.debian.org/debian testing main" | sudo tee -a /etc/apt/sources.list

# echo 'APT::Default-Release "stable";' | sudo tee -a /etc/apt/apt.conf.d/00local
# sudo apt-get update
# sudo apt-get -t testing install python3.6

python3 --version


sudo pip3 install pyyaml
sudo pip3 install inotify
sudo gem install icalendar
