#!/bin/bash
mkdir /home/ec2-user/vaxbot
cd vaxbot
yum update -y
yum install git -y
git clone https://github.com/marcwojcik/vaxbot.git

yum install python3 -y

cd /tmp/
wget https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver

curl https://intoli.com/install-google-chrome.sh | bash
sudo mv /usr/bin/google-chrome-stable /usr/bin/google-chrome
