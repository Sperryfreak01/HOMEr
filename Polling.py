__author__ = 'matt'

import DeviceComunication
import HomerHelper
import time
import RESTInterface
import logging
import astral
from Scheduler import schedule

logger = logging.getLogger(__name__)

def PollingStart():
    schedule(DailyHouseKeeping, id="DailyRunTasks", trigger='cron', hour=03, misfire_grace_time=None)

    if HomerHelper.getSettingValue('hue_polling') == 'True':
        logger.info("They see me pollin they hating, Phillips hue polling enabled")
        polling_rate = int(HomerHelper.getSettingValue('hue_polling_rate'))
        schedule(HuePoll, id="HuePoll", trigger='interval', seconds=polling_rate)

    if HomerHelper.getSettingValue('myQ_polling') == 'True':
        logger.info("They see me pollin they hating, myQ Device polling enabled")
        polling_rate = int(HomerHelper.getSettingValue('myQ_polling_rate'))
        schedule(myQPoll, id="MyQ Poll", trigger='interval', seconds=polling_rate, misfire_grace_time=None)


def myQPoll():
    MyQ = DeviceComunication.MyQ()
    #MyQ.authenticate()
    myq_ids = HomerHelper.getIDofDeviceTypes("MyQ")
    for id in myq_ids:
        try:
            doorstatus = MyQ.getDoorStatus(id)
            HomerHelper.updateDeviceAttribute(id, doorstatus, 'State')
        except:
            MyQ.authenticate()
            MyQ.getDoorStatus(id)
            HomerHelper.updateDeviceAttribute(id, doorstatus, 'State')

def HuePoll():
        hue_ids = HomerHelper.getIDofDeviceTypes("hue")
        for id in hue_ids:
            hue_brightness = DeviceComunication.getHueBrightness(id)
            HomerHelper.updateDeviceAttribute(id, hue_brightness, 'Brightness')

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



