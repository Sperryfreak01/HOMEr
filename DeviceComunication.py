__author__ = 'matt'

import urllib
import urllib2
import urlparse

IMP_API = "https://agent.electricimp.com/"
SPARK_API = "https://api.spark.io/v1/"
spark_token = 'e8a5241dee80316554e4f72c516ecf3ff26e15f6'

def sendDeviceBrightness(device_id, device_type, brightness):
    if device_type == "imp":
        url = IMP_API
        urllib.urlopen(IMP_API + device_id + "?setbrightness= " + brightness)
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

def sparkAlarm(device_ID, color, spark_token):
    payload = {
        'access_token' : spark_token,
        'args' : color
    }
    device_path = "devices/" + device_ID + "/alarm"
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