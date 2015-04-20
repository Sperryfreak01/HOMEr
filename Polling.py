__author__ = 'matt'

import DeviceComunication
import HomerHelper
import time
import RESTInterface
import logging
import gevent


logger = logging.getLogger(__name__)

def PollingStart():
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


