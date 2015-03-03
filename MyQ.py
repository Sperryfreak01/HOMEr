__author__ = 'matt'

import urlparse
import requests
import json

MYQ_API = "http://myqexternal.myqdevice.com/"
application_id = "NWknvuBd7LoFHfXmKNMBcgajXtZEgKUh4V7WNzMidrpUUluDpVYVZx+xT4PCM5Kx"
DEVICEID = 251699265


def authenticate(user,password,):
    loginUrl = urlparse.urljoin(MYQ_API, "/Membership/ValidateUserWithCulture")
    payload = {
        'appId':application_id,
        'securityToken':'null',
        'username':'mattlovett@mattlovett.com',
        'password':'Matthdl13',
        'culture':'en'
    }
    r = requests.get(loginUrl, params=payload)
    jsonData = json.loads(r.text)
    errorMessage = str(jsonData['ErrorMessage'])

    if not errorMessage:
        return jsonData['SecurityToken']
    else:
        return None

def getDoorStatus(deviceId):
    systemInfoUrl = urlparse.urljoin(MYQ_API, "/Device/getDeviceAttribute")
    payload = {
        'appId': application_id,
        'devId': deviceId,
        'name': 'doorstate',
        'securityToken': securityToken}
    r = requests.get(systemInfoUrl, params=payload)

    if not r.json['ErrorMessage']:
        doorStatus = r.json['AttributeValue']
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




def setDoorStatus(deviceId, securityToken, doorState):
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
        'ApplicationId':application_id,
        'SecurityToken':securityToken,
        'DeviceId':deviceId,
        'AttributeName':'desireddoorstate',
        'AttributeValue':doorState
    }

    r = requests.put(deviceSetUrl, params=payload)


