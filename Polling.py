__author__ = 'matt'

import DeviceComunication
import HomerHelper
import time
import RESTInterface
import logging
import gevent
import astral


logger = logging.getLogger(__name__)

def PollingStart():
    gevent.spawn(DailyHouseKeeping())
    if HomerHelper.getSettingValue('hue_polling') == 'True':
        gevent.spawn(HuePoll)
    if HomerHelper.getSettingValue('myQ_polling') == 'True':
        gevent.spawn(myQPoll())

def myQPoll():
    logger.info("They see me pollin they hating, myQ Device polling enabled")
    polling_rate = int(HomerHelper.getSettingValue('myQ_polling_rate'))
    MyQ = DeviceComunication.MyQ()
    MyQ.authenticate()
    while True:
        myq_ids = HomerHelper.getIDofDeviceTypes("MyQ")
        for id in myq_ids:
            try:
                doorstatus = MyQ.getDoorStatus(id)
                HomerHelper.updateDeviceAttribute(id, doorstatus, 'State')
            except:
                MyQ.authenticate()
                MyQ.getDoorStatus(id)
                HomerHelper.updateDeviceAttribute(id, doorstatus, 'State')
        time.sleep(polling_rate)


def HuePoll():
    logger.info("They see me pollin they hating, Phillips hue polling enabled")
    polling_rate = int(HomerHelper.getSettingValue('hue_polling_rate'))
    while True:
        hue_ids = HomerHelper.getIDofDeviceTypes("hue")
        for id in hue_ids:
            hue_brightness = DeviceComunication.getHueBrightness(id)
            HomerHelper.updateDeviceAttribute(id, hue_brightness, 'Brightness')
        time.sleep(polling_rate)

def AlarmCheck():
    pass

def DailyHouseKeeping():
    street = HomerHelper.getSettingValue('StreetAddress')
    city = HomerHelper.getSettingValue('City')
    state = HomerHelper.getSettingValue('State')
    while True:
        logging.debug("performing daily housekeeping actions")
        sun = HomerHelper.calcSunPosition(street, city, state)
        HomerHelper.updateSettingValue('sunrise',sun['sunrise'])
        HomerHelper.updateSettingValue('sunset',sun['sunset'])
        time.sleep(3600*24)
    pass


