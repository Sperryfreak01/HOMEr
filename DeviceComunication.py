__author__ = 'matt'

import urllib
import urllib2
import urlparse
import json
from phue import Bridge
import HomerHelper
import logging
import threading
import gevent
from gevent import Greenlet
import urlparse
import requests
import json
from Scheduler import schedule, KillJob, GetJob
import random



logger = logging.getLogger(__name__)

IMP_API = HomerHelper.getSettingValue('Imp_API_URL')
SPARK_API = HomerHelper.getSettingValue('Spark_API_URL')



spark_token = HomerHelper.getSettingValue('spark_token')



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
        name = HomerHelper.getDeviceName(device_id)
        logging.debug("HUE brightness being set to " + str(brightness))
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

def sendDeviceColor(device_id, color_hex, lighting_mode):
    if lighting_mode == '0':  # fade mode
        if GetJob('SparkRandom' is not None):
                killJob('SparkRandom')
        subject = 'fade'
        color = color_hex
        schedule(ParticlePublish, args=(subject, color))

    elif lighting_mode == '1':  # Solid color mode
        if GetJob('SparkRandom' is not None):
                killJob('SparkRandom')
        subject = 'hold'
        color = color_hex
        schedule(ParticlePublish, args=(subject, color))

    elif lighting_mode == '2':    # Alarm Mode
        if GetJob('SparkRandom' is not None):
                killJob('SparkRandom')
        subject = 'alert'
        color = color_hex
        schedule(ParticlePublish, args=(subject, color))

    elif lighting_mode == '3':    # Constant Random Mode
        schedule(RGBgen, trigger='interval', seconds=180, id="SparkRandom")
    else:
        print 'no match'

def RGBgen():
    red = random.randint(0, 8191)
    green = random.randint(0, 8191)
    blue = random.randint(0, 8191)

    RGB = str(red) + str(green) + str(blue) + str(0)
    subject = 'fade'
    print RGB
    ParticlePublish(subject, RGB)

def ParticlePublish(subject, msgdata):
    payload = {
        'access_token': spark_token,
        'name': subject,
        'data': msgdata,
        'private': 'false',
        'ttl': '60',
        }
    logger.debug("Particle publish: %s" % str(payload))

    r = requests.post(SPARK_API, data=payload)
    print r.text


def ParticleSubscribe():
    pass

def getHueBrightness(device_id):
    light_disabled = b.get_light(int(device_id), 'on')
    if light_disabled is False:
        light = 0
    else:
        light = b.get_light(int(device_id),'bri')
    logging.debug('HUE device id is ' + device_id)
    logging.debug('HUE brightneess is ' + str(light))
    return light

class MyQ(object):

    def __init__(self):
        self.MYQ_API = HomerHelper.getSettingValue('MyQ_API_URL')
        self.MyQ_App_ID = HomerHelper.getSettingValue('MyQ_App_ID')
        self.securityToken = self.authenticate()


    def authenticate(self):
        loginUrl = urlparse.urljoin(self.MYQ_API, "/Membership/ValidateUserWithCulture")
        payload = {
            'appId':self.MyQ_App_ID,
            'securityToken':'null',
            'username':HomerHelper.getSettingValue('MyQ_Username'),
            'password':HomerHelper.getSettingValue('MyQ_Password'),
            'culture':'en'
        }
        logging.debug('authenticating MyQ account')
        r = requests.get(loginUrl, params=payload)
        jsonData = json.loads(r.text)
        errorMessage = str(jsonData['ErrorMessage'])

        if not errorMessage:
            return jsonData['SecurityToken']
        else:
            return None

    def getDoorStatus(self, deviceId):
        systeminfourl = urlparse.urljoin(self.MYQ_API, "/Device/getDeviceAttribute")
        payload = {
            'appId': self.MyQ_App_ID,
            'devId': deviceId,
            'name': 'doorstate',
            'securityToken': self.securityToken}
        r = requests.get(systeminfourl, params=payload)

        if not r.json()['ErrorMessage']:
            doorStatus = r.json()['AttributeValue']
            if doorStatus == "1":
                return "open"
            elif doorStatus == "2":
                return "closed"
            elif doorStatus == "4":
                return "opening"
            elif doorStatus == "5":
                return "closing"
            else:
                return "unknown"




    def setDoorStatus(self, deviceId, doorState):
        if doorState == 'open':
            doorState = 1
        elif doorState == 'closed':
            doorState = 2
        elif doorState == 'opening':
            doorState = 4
        elif doorState == 'closing':
            doorState = 5
        else:
            raise ValueError('Invalid door state passed')

        deviceSetUrl = urlparse.urljoin(MYQ_API, "/Device/setDeviceAttribute")
        payload = {
            'ApplicationId':MyQ_App_ID,
            'SecurityToken':self.securityToken,
            'DeviceId':deviceId,
            'AttributeName':'desireddoorstate',
            'AttributeValue':doorState
        }

        r = requests.put(deviceSetUrl, params=payload)
        return 1


