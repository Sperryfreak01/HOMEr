__author__ = 'matt'

import urllib
import urllib2
import urlparse
import json
from phue import Bridge


IMP_API = "https://agent.electricimp.com/"
SPARK_API = "https://api.spark.io/v1/"
spark_token = 'e8a5241dee80316554e4f72c516ecf3ff26e15f6'


b = Bridge(Philips-hue.mattlovett.com)

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
        b.set_light(device_id, 'bri', brightness)

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

def hex2rgb(hex):
    if hex is not None:
        red = str(int(hex[0:2],16))    # grabs the chars that are for each color and splits them
        red = red.zfill(3)             # converts from hex to int and then to a string, then
        green = str(int(hex[2:4],16))  # fills them to 3 digits always. rinse and repeat for other
        green = green.zfill(3)         # colors.  String all three together comma separated list.
        blue = str(int(hex[4:6],16))
        blue = blue.zfill(3)
        rgb = ','
        rgb = rgb.join((red, green, blue))
        return rgb
    else:
        rgb = "000,000,000"
        return rgb


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

