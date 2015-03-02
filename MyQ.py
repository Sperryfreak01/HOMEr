__author__ = 'matt'

MYQ_API = "http://myqexternal.myqdevice.com/"
application_id = "NWknvuBd7LoFHfXmKNMBcgajXtZEgKUh4V7WNzMidrpUUluDpVYVZx+xT4PCM5Kx"


import urlparse
import requests
import json


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
    securityToken = jsonData['SecurityToken']
    print securityToken
    systemInfoUrl = urlparse.urljoin(MYQ_API, "/api/UserDeviceDetails")
    payload = {'appId':application_id, 'securityToken':securityToken}
    r = requests.get(systemInfoUrl, params=payload)
    systemInfoResult = json.loads(r.text)
    for item in systemInfoResult:
        print item + ' : '
        #for device in systemInfoResult['Devices']:
            #print device

else:
    print "error Message:" + jsonData['ErrorMessage']



def setDoorStatus(deviceId,securityToken,doorState)
 payload = {
            'ApplicationId':application_id,
            'SecurityToken':securityToken,
            'DeviceId':'251699265',
            'AttributeName':'desireddoorstate',
            'AttributeValue':doorState
 }

