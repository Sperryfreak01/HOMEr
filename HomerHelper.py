### This file contains helper functions invoked by HOMEr

__author__ = 'matt'

import pymysql
import re
import logging
import gevent

logger = logging.getLogger(__name__)



class DB:
    def greenquerry(self, sql, options):
        g_querry = gevent.spawn(self.query, (sql, options))
        while g_querry.ready():
            gevent.sleep(0)
        return g_querry.value()


    def query(self, sql, options):
        try:
            conn = pymysql.connect('localhost', 'HOMEr', 'HOMEr', 'HOMEr')
            conn.autocommit(True)

            if options is not None:
                logging.debug(sql % options)
            else:
                logging.debug(sql)

            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, options )
            #self.conn.commit()

        except (AttributeError, pymysql.OperationalError):
            self.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, options)
            #self.conn.commit()

        conn.close()
        return cursor



db = DB()

def insert_history( device_name,device_id,event):
    try:
       # print device_name
        sql_insert = "INSERT INTO `History`(`name`, `id`, `event`) VALUES (%s,%s,%s)"
        cur = db.query(sql_insert, (device_name, device_id, event))
        #logger.warn("%d", affected_count)
        #logger.info("inserted values %d, %s", id, filename)
    except MySQLdb.IntegrityError:
        #logger.warn("failed to insert values %d, %s", id, filename)
        #abort(400, "Doh! History was forgotten")
        print ("log entry exception")
    cur = db.query("SELECT * from Devices where `name` = %s", device_name)
    rows = cur.fetchall()

    return()

def deviceExsists(id):
    device_id = ""
    with con:
        print(id)
        cur = db.query("SELECT * FROM Devices WHERE id = %s", id)

    row = cur.fetchall()
    for col in row:
        device_id = col["id"]

    if device_id is "":
        return (False)
    else:
        return (True)

def getDeviceName(id):
    cur = db.query("SELECT `name` FROM Devices WHERE id = %s", id)
    row = cur.fetchone()
    device_name = row["name"]
    if device_name is None:
        return ""
    else:
        return device_name

def getDeviceType(id):
    cur = db.query("SELECT `type` FROM Devices WHERE id = %s", id)
    row = cur.fetchall()
    for col in row:
        device_type = col["type"]
    if device_type is None:
        return ""
    else:
        return device_type

def getDeviceFunction(id):
    cur = db.query("SELECT `function` FROM Devices WHERE id = %s", id)
    row = cur.fetchall()
    for col in row:
        device_function = col["function"]
    if device_function is None:
        return ""
    else:
        return device_function

def deviceIdCheck(id):
    #if re.match(r"[a-zA-Z0-9]{0,128}$", id) is None: # check that id only has letters and numbers
    #    return False
    #else:
    cur =db.query("SELECT * FROM Devices WHERE id = %s", id)
    row = cur.fetchall()
    if row:
        return True
    else:
        return False

def deviceGroupCheck(group):
    #if re.match(r"[a-zA-Z0-9]{0,128}$", id) is None: # check that id only has letters and numbers
    #    return False
    #else:
    cur =db.query("SELECT * FROM Devices WHERE `group` = %s", group)
    row = cur.fetchone()
    if row:
        return True
    else:
        return False

def userIdCheck(con, id):
    if re.match(r"[a-zA-Z0-9]{0,128}$", id) is None: # check that id only has letters and numbers
        return False
    else:
        cur = db.query("SELECT * FROM Users WHERE id = %s", id)
        row = cur.fetchall()
        if row:
            return True
        else:
            return False

def idCheck(id_type, id):
    if re.match(r"[a-zA-Z0-9]{0,128}$", id) is None: # check that id only has letters and numbers
        return False
    else:
        sql_query = ("SELECT `id` FROM %s " % id_type)
        sql_query +=("WHERE id = %s")
        logger.debug(sql_query, id)
        cur = db.query(sql_query, id)
        row = cur.fetchall()
        if row:
            return True
        else:
            return False

def roomCheck(name):
    cur = db.query('SELECT * FROM Rooms WHERE `name` = %s', name)
    row = cur.fetchall()
    if row:
        return True
    else:
        return False


def getUserName(con, id):
    cur = db.query('SELECT `name` FROM Users WHERE id = %s', id)
    row = cur.fetchall()
    for col in row:
        device_name = col["name"]
    if device_name is None:
        return ""
    else:
        return device_name

def getSettingValue(SettingName):
    cur = db.query('SELECT `value` FROM Settings WHERE name = %s', SettingName)
    row = cur.fetchone()
    value = row['value']
    return value

def getIDofDeviceTypes(DeviceType):
    cur = db.query('SELECT `id` FROM Devices WHERE type = %s', DeviceType)
    rows = cur.fetchall()
    device_ids = []
    for row in rows:
        device_id = row["id"]
        device_ids.append(device_id)
    return device_ids

def lookupDeviceAttribute(function, attr_name):
    try:
        sql_querry = "SELECT * FROM `Device_Types` WHERE type = %s"
        cur = db.query(sql_querry, function)
        rows = cur.fetchall()
        for row in rows:
            for x in xrange(1, 10):
                col_name = "value%d" % x  # iterate through attribute field looking for the column we need
                if row[col_name] == attr_name:
                    logger.debug("Device Type: %s col name: %s  row[]: %s  attr name: %s " % (function, col_name, row[col_name], attr_name))
                    return col_name
            else:
                logger.debug("Unable to find attribute for Device Type: %s" % function)
                return None
    except pymysql.IntegrityError:
            return None

def updateDeviceAttribute(device_id, value, value_name):

    try:
        sql_querry = "SELECT * from `Devices` where `id` = %s"
        cur = db.query(sql_querry, device_id)
        details = cur.fetchone()

        device_name = details['name']
        device_function = details['function']
        device_type = details['type']

        value_location = lookupDeviceAttribute(device_function,value_name)

        sql_update = "UPDATE `Devices` SET %s " % value_location  # write it the same column in devices
        sql_update += "= %s  WHERE id = %s"
        db.query(sql_update, (value, device_id))

        history_event = "set %s to: %s" % (value_name, value)
        insert_history(device_name, device_id, history_event)

    except pymysql.IntegrityError:
        logger.warn("Unable to update device id's %s, %s attribute to %s" % (device_id, value_name, value))

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

def buildNav():
    webroot = getSettingValue('webroot')

    cur = db.query("SELECT * FROM `Rooms`",None)
    row = cur.fetchall()

    rooms = []  # parser for the information returned
    for col in row:
        roomname = col['name']
        roomname = roomname.replace(" ", "%20")
        roomlist = (col['name'], roomname)
        rooms.append(roomlist)

    cur = db.query("SELECT * FROM `Device_Types`",None)
    row = cur.fetchall()

    functions = []  # parser for the information returned
    for col in row:
        functionname = col['type']
        functionname = functionname.replace(" ", "%20")
        functionlist = (col['type'], functionname)
        functions.append(functionlist)

    cur = db.query("SELECT * FROM `Settingslist`",None)
    row = cur.fetchall()

    settings = []  # parser for the information returned
    for col in row:
        settingsname = col['name']
        settingsname = settingsname.replace(" ", "%20")
        settingslist = (col['name'], settingsname)
        settings.append(settingslist)

    return {'webroot': webroot, 'rooms': rooms, 'functions': functions, 'settings': settings}



