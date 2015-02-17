__author__ = 'matt'

import urllib
import urllib2
import urlparse
import json
from phue import Bridge
from HomerHelper import getDeviceName
import logging
import threading
import gevent
from gevent import Greenlet

logger = logging.getLogger(__name__)

IMP_API = "https://agent.electricimp.com/"
SPARK_API = "https://api.spark.io/v1/"
spark_token = 'e8a5241dee80316554e4f72c516ecf3ff26e15f6'


b = Bridge("Philips-hue.mattlovett.com", config_file_path = "./HOMEr_hue")

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
b.connect()

# Get the bridge state (This returns the full dictionary that you can explore)
b.get_api()

lights = b.lights

def sendDeviceBrightness(device_id, device_type, brightness):
    if device_type == "imp":
        url = IMP_API
        urllib.urlopen(IMP_API + device_id + "?setbrightness= " + brightness)

    elif device_type == "hue":
        name = getDeviceName(None, device_id)
        logging.debug("HUE brightness being set to " + brightness)
        if int(brightness) == 0:
             Greenlet.spawn(b.set_light,name, 'on', False)

        else:
            Greenlet.spawn(b.set_light, name, 'on', True)
            Greenlet.spawn(b.set_light, name, 'bri', int(brightness))

    elif device_type == "spark":
        # url = SPARK_API
        #urllib.urlopen(SPARK_API + device_id + "/setbrightness " + brightness)
        payload = {
            'access_token' : spark_token,
            'args' : brightness
        }
        device_path = "devices/" + device_ID + "/setbrightness"
        url = urlparse.urljoin(SPARK_API, device_path)
        try:
            data = urllib.urlencode(payload)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            spark_response = response.read()
        except urllib2.HTTPError, httperror:
            raise SparkError(httperror)

        d = json.loads(spark_response)
        if d['return_value'] is not 1:
            #raise SparkError(spark_response)
            print "error"



class SparkError(Exception): pass


def sendDeviceColor(device_id, color_hex, lighting_mode):
    color_rgb = hex2rgb(color_hex)

    payload = {
        'access_token' : spark_token,
        'args' : color_rgb
        }
    print payload
    if lighting_mode == '0':  # fade mode
        device_path = "devices/" + device_id + "/fade"
        url = urlparse.urljoin(SPARK_API, device_path)
        sendSparkCommand(url, payload)
    elif lighting_mode == '1':  # Solid color mode
        device_path = "devices/" + device_id + "/hold"
        url = urlparse.urljoin(SPARK_API, device_path)
        sendSparkCommand(url, payload)
    elif lighting_mode == '2':    # Alarm Mode
        device_path = "devices/" + device_id + "/alarm"
        url = urlparse.urljoin(SPARK_API, device_path)  # build the URL to communicate with the Spark
        sendSparkCommand(url, payload)
    else:
        print 'no match'

def sendSparkCommand(url, payload):
    try:
        data = urllib.urlencode(payload)  # build the POST command to send to the Spark
        req = urllib2.Request(url, data)  # send request to Spark
        response = urllib2.urlopen(req)
        spark_response = response.read()
        d = json.loads(spark_response)
        if d['return_value'] is not 1:    # Spark returns 1 for success and 0 for failure
            raise SparkError(spark_response)

    except urllib2.HTTPError as e:
        raise SparkError(e)

def getHueBrightness(device_id):
    light = b.get_light(int(device_id),'bri')
    logging.debug('HUE device id is ' + device_id)
    logging.debug('HUE brightneess is ' + str(light))
    return light
