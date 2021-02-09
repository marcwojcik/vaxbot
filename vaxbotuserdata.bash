#!/bin/bash
mkdir /home/ec2-user/projects
cd projects
yum update -y
yum install git -y
git clone https://github.com/marcwojcik/vaxbot.git

sudo yum install python3 -y
exit
python3 -m pip install --user boto3
python3 -m pip install --user bs4
python3 -m pip install --user tweepy
python3 -m pip install --user pyyaml

cd /tmp/
wget https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver

curl https://intoli.com/install-google-chrome.sh | bash
sudo mv /usr/bin/google-chrome-stable /usr/bin/google-chrome

python3 -m pip install --user selenium
