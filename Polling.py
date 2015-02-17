__author__ = 'matt'

import DeviceComunication
import HomerHelper
import time
import RESTInterface
import logging
from gevent import Greenlet


logger = logging.getLogger(__name__)

def PollingStart():
    if HomerHelper.getSettingValue('hue_polling') == 'True':
        Greenlet.spawn(HuePoll)

def HuePoll():
    logger.info("They see me pollin they hating, Phillips hue polling enabled")
    polling_rate = int(HomerHelper.getSettingValue('hue_polling_rate'))
    while True:
        hue_ids = HomerHelper.getIDofDeviceTypes("hue")
        for id in hue_ids:
            hue_brightness = DeviceComunication.getHueBrightness(id)
            brightness_location = HomerHelper.lookupDeviceAttribute("lamp", 'Brightness')
            if brightness_location is not None:
                try:
                    sql_querry = "SELECT `%s`" % brightness_location
                    sql_querry += " FROM `Devices` WHERE id = %s"   # write it the same column in devices
                    cur = HomerHelper.db.query(sql_querry, ( id))
                    db_brightness = cur.fetchone()
                    if hue_brightness is not db_brightness:
                        RESTInterface.setBrightness(True,id,hue_brightness)
                except Exception as e:
                    logger.warn("while trying to fetch hue brightness error occured: " + str(e))
            else:
                logger.warn("while looking up brightness attribute for hue device db returned none")
        time.sleep(polling_rate)
