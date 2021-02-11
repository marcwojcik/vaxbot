import os
import time
import datetime
import boto3
import yaml
import logging
import json

import Counties
import HealthcareSystems


def get_secret(name):
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(SecretId=name)
    if 'SecretString' in get_secret_value_response:
        return get_secret_value_response['SecretString']
    else:
        return ""


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
        logging.info(
            "Published message with attributes to topic %s.",
            topic)
    except Exception as e:
        logging.exception("Couldn't publish message to topic %s.", topic)
        raise


with open('config.yaml', 'r') as config_yaml:
    try:
        vax_bot = yaml.safe_load(config_yaml)["vax_bot"]
        if vax_bot:
            consumer_key = vax_bot['tw_consumer_key']
            consumer_secret = vax_bot['tw_consumer_secret']
            access_token = vax_bot['tw_access_token']
            secret_access_token = vax_bot['tw_secret_access_token']
            topic_arn = vax_bot['topic_arn']
            log_file = vax_bot['log_file']
            log_level = vax_bot['log_level']
            vax_sleeptime = vax_bot['vax_sleeptime']
            aws_hudson_secret = vax_bot['aws_hudson_secret']
    except yaml.YAMLError as e:
        logging.debug(e)
        exit(0)
    except KeyError as e:
        logging.exception("Error in Config File.")
        exit(0)

# logging.basicConfig(filename=log_file, level=log_level)
logging.root.handlers = []
logging.basicConfig(level=log_level, format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[logging.FileHandler(log_file), logging.StreamHandler()])

print(datetime.datetime.now())
print("VaxBot Starting - Logging to " + log_file + " - Log Level " + log_level)
while (True):
    try:
        # Essex --------------------------------------------------
        essex = Counties.EssexCounty()
        essex_number_vaccines = essex.check_vaccines()
        if essex_number_vaccines > 0:
            logging.info("Appointments available Essex County Website Currently - " + str(essex_number_vaccines) +
                         " https://www.essexcovid.org/vaccine/vaccine_availability")
            publish_message(topic_arn,
                            "Appointments available Essex County Website Currently - " + str(essex_number_vaccines) +
                            " https://www.essexcovid.org/vaccine/vaccine_availability")
        else:
            logging.info('No Vaccines - Essex')

        # Hudson County --------------------------------------------------------------
        secret = get_secret(aws_hudson_secret)
        secret_loads = json.loads(secret)
        hudson = Counties.HudsonCounty(secret_loads["username"], secret_loads["password"])
        if hudson.check_vaccines():
            logging.info("Appointments available on Hudson County Website https://www.hudsoncovidvax.org/login")
            publish_message(topic_arn,
                            "Appointments available on Hudson County Website "
                            "https://www.hudsoncovidvax.org/login")
        else:
            logging.info('No Vaccines - Hudson County')
        # Union County -----------------------------------------------------------------
        union = Counties.UnionCounty()
        union_number_vaccines = union.check_vaccines()

        if union_number_vaccines != "0":
            logging.info("Appointments available Union County Website Currently - " + union_number_vaccines +
                         " https://ucnjvaccine.org/index.php/vaccine/vaccine_availability")
            publish_message(topic_arn,
                            "Appointments available Union County Website Currently - " + union_number_vaccines +
                            " https://ucnjvaccine.org/index.php/vaccine/vaccine_availability")
        else:
            logging.info('No Vaccines - Union County')
        # Hackensack Meridian Health --------------------------------------------------
        hackensack = HealthcareSystems.Hackensack()
        if hackensack.check_vaccines():
            logging.info("Appointments may be available on Hackensack Meridian Health Website "
                         "https://www.hackensackmeridianhealth.org/covid19/")
            publish_message(topic_arn,
                            "Appointments may be available on Hackensack Meridian Health Website "
                            "https://www.hackensackmeridianhealth.org/covid19/")
        else:
            logging.info('No Vaccines - Hackensack Meridian Health')

        collier = Counties.CollierCounty()
        if collier.check_vaccines():
            logging.info("Appointments may be available at Collier "
                         "https://www.eventbrite.com/o/florida-department-of-health-in-collier-county-32165407705")
            publish_message(topic_arn,
                            "Appointments may be available at Collier "
                            "https://www.eventbrite.com/o/florida-department-of-health-in-collier-county-32165407705")
        else:
            logging.info('No Vaccines - Collier')

        # Bergen County -----------------------------------------------------------------
        bergen = Counties.BergenCounty()
        bergen_number_vaccines = bergen.check_vaccines()
        if bergen_number_vaccines != "0":
            logging.info("Appointments available Bergen County Website Currently - " + bergen_number_vaccines +
                         " https://www.bergencovidvaccine.com/index.php/vaccine/vaccine_availability")
            publish_message(topic_arn,
                            "Appointments available Bergen County Website Currently - " + bergen_number_vaccines +
                            " https://www.bergencovidvaccine.com/index.php/vaccine/vaccine_availability")
        else:
            logging.info('No Vaccines - Bergen County')


    except (Exception, RuntimeError) as e:
        logging.exception(str(e))
        publish_message(topic_arn, "Runtime EXCEPTION : " + str(e))


    finally:
        logging.info("Sleeping - " + vax_sleeptime + " seconds")
        time.sleep(int(vax_sleeptime))
