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
    if HomerHelper.getSettingValue('wifi_polling') == 'True':
        gevent.spawn(WifiPoll)

def WifiPoll():
    logger.info("They see me pollin they hating, Wifi Device polling enabled")
    polling_rate = int(HomerHelper.getSettingValue('hue_polling_rate'))
    while True:
        

        time.sleep(polling_rate)




def HuePoll():
    logger.info("They see me pollin they hating, Phillips hue polling enabled")
    polling_rate = int(HomerHelper.getSettingValue('hue_polling_rate'))
    while True:
        hue_ids = HomerHelper.getIDofDeviceTypes("hue")
        for id in hue_ids:
            hue_brightness = DeviceComunication.getHueBrightness(id)
            brightness_location = HomerHelper.lookupDeviceAttribute("lamp", 'Brightness')

            if brightness_location is not None:
                #try:
                sql_querry = "SELECT `%s`" % brightness_location
                sql_querry += " FROM `Devices` WHERE id = %s"   # write it the same column in devices
                cur = HomerHelper.db.query(sql_querry, id)
                db_brightness = cur.fetchone()

                for key in db_brightness.keys():
                    db_brightness = db_brightness[key]

                if int(hue_brightness) != int(db_brightness):
                    HomerHelper.updateDeviceAttribute(id, hue_brightness, 'Brightness')

                #except:
                #    logger.warn("while trying to fetch hue brightness error occured")
            else:
                logger.warn("while looking up brightness attribute for hue device db returned none")
        time.sleep(polling_rate)


