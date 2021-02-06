import os
import time
import datetime

import boto3
import tweepy
import yaml
import logging

import Counties
import HealthcareSystems

logger = logging.getLogger(__name__)


def publish_message(topic, message):
    """
    Publishes a message, with attributes, to a topic. Subscriptions can be filtered
    based on message attributes so that a subscription receives messages only
    when specified attributes are present.

    :param topic: The topic to publish to.
    :param message: The message to publish.
    :return: The ID of the message.
    """
    try:
        sns = boto3.client('sns')
        response = sns.publish(TopicArn=topic, Message=message)
        logger.info(
            "Published message with attributes to topic %s.",
            topic)
    except Exception as e:
        logger.exception("Couldn't publish message to topic %s.", topic)
        raise


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
            topic_arn = vax_bot['topic_arn']
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

while (True):
    try:
        print(datetime.datetime.now())
        # Hudson County --------------------------------------------------------------
        hudson = Counties.HudsonCounty(hudson_username, hudson_password)
        if hudson.check_vaccines():
            publish_message(topic_arn,
                            "Appointments available on Hudson County Website https://www.hudsoncovidvax.org/login")
        else:
            print('No Vaccines - Hudson County')
        # Union County -----------------------------------------------------------------
        union = Counties.UnionCounty()
        if union.check_vaccines():
                publish_message(topic_arn,
                                "Appointments available Union County Website "
                                "https://ucnjvaccine.org/index.php/vaccine/vaccine_availability")
        else:
            print('No Vaccines - Union County')
        # Hackensack Meridian Health --------------------------------------------------
        hackensack = HealthcareSystems.Hackensack()
        if hackensack.check_vaccines():
                publish_message(topic_arn,
                                "Appointments may be available on Hackensack Meridian Health Website "
                                "https://www.hackensackmeridianhealth.org/covid19/")
        else:
            print('No Vaccines - Hackensack Meridian Health')

        # Shoprite --------------------------------------------------
        shoprite = HealthcareSystems.Shoprite()
        if shoprite.check_vaccines():
            publish_message(topic_arn,
                            "Appointments may be available at Shoprite "
                            "http://sr.reportsonline.com/sr/shoprite/Immunizations")
        else:
            print('No Vaccines - Shoprite')



    except Exception as e:
        print("{} - Exception!!".format(datetime.datetime.now()))
        print(str(e))
    finally:
        time.sleep(60)

