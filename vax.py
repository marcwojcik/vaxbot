import os
import time
import datetime
import boto3
import tweepy
import yaml

import Counties


with open('config.yaml', 'r') as config_yaml:
    try:
        vax_bot = yaml.safe_load(config_yaml)["vax_bot"]
        if vax_bot:
            consumer_key = vax_bot['tw_consumer_key']
            consumer_secret = vax_bot['tw_consumer_secret']
            access_token = vax_bot['tw_access_token']
            secret_access_token = vax_bot['tw_secret_access_token']
            hudson_username = vax_bot['hudson_username']
            hudson_password = vax_bot['hudson_password']
    except yaml.YAMLError as e:
        print(e)
        exit(0)
    except KeyError as e:
        print("Error in Config File.")
        exit(0)

# set up tweepy credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, secret_access_token)

# Create Twitter API object
twitter_api = tweepy.API(auth)

while(True):
    try:
        # Hudson County -------------------------
        hudson = Counties.HudsonCounty(hudson_username, hudson_password)
        if hudson.check_vaccines():
            try:
                twitter_api.update_status(" Appointments may be available on Hudson County Website https://www.hudsoncovidvax.org/login")
                sns = boto3.client('sns')
                response = sns.publish(TopicArn='arn:aws:sns:us-east-1:936321854814:vaxbot', Message='Appointments may be available on Hudson County Website https://www.hudsoncovidvax.org/login',)
            except Exception as e:
                print('error publishing')
                print('error - {}'.format(str(e)))

        else:
            print('No Vaccines - Hudson County')
        # Union County ----------------------------------------------
        union = Counties.UnionCounty()
        if union.check_vaccines():
            try:
                twitter_api.update_status(" Appointments may be available on Union County Website https://ucnjvaccine.org/index.php/vaccine/vaccine_availability")
                sns = boto3.client('sns')
                response = sns.publish(TopicArn='arn:aws:sns:us-east-1:936321854814:vaxbot', Message='Appointments may be available on Union County Website https://ucnjvaccine.org/index.php/vaccine/vaccine_availability',)
            except Exception as e:
                print('error publishing')
                print('error - {}'.format(str(e)))
        else:
            print('No Vaccines - Union County')
        # Next Site here
    except Exception as e:
        print("{} - Exception!!".format(datetime.datetime.now()))
        print(str(e))
    finally:
        time.sleep(60)