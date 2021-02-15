#!/bin/bash
mkdir /home/ec2-user/vaxbot
chown -R ec2-user:ec2-user /home/ec2-user/vaxbot
yum update -y
yum install git -y
git clone https://github.com/marcwojcik/vaxbot.git /home/ec2-user/vaxbot

yum install python3 -y

cd /tmp/
wget https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin/chromedriver

curl https://intoli.com/install-google-chrome.sh | bash
mv /usr/bin/google-chrome-stable /usr/bin/google-chrome

chown -R ec2-user:ec2-user /home/ec2-user/vaxbot
