__author__ = 'matt'

from bottle import *
import MySQLdb
import collections
import json
import urllib
import urllib2
import re
import threading
import HomerHelper
import Notifications
import DeviceComunication


con = MySQLdb.connect('192.168.2.1', 'HOMEr', 'HOMEr', 'HOMEr')

IMP_API = "https://agent.electricimp.com/"
SPARK_API = "https://api.spark.io/v1/"
con.close()


db = HomerHelper.DB()


@get('/getdevices')  # returns all devices registered in teh system
def getDevices():
    cur = db.query("SELECT * FROM `Devices`", None)
    row = cur.fetchall()
    #print row
    objects_list = []  # parser for the information returned
    for col in row:
        d = collections.OrderedDict()
        d['name'] = col["name"]
        d['type'] = col["type"]
        d['function'] = col["function"]
        d['id'] = col["id"]
        objects_list.append(d)
    j = json.dumps(objects_list)
    return j

@get('/getdevice')  # returns all devices registered in teh system
def getDevice():

    device_id = request.params.get('id')
    if HomerHelper.idCheck('Devices', device_id):  #validate the device ID
        sql_query = "SELECT * FROM `Devices` WHERE `id` = %s "
        cur = db.query(sql_query, device_id)
        row = cur.fetchone()

        objects_list = []  # parser for the information returned

        d = collections.OrderedDict()
        d['name'] = row["name"]
        d['type'] = row["type"]
        d['function'] = row["function"]
        d['id'] = row["id"]
        objects_list.append(d)

        return json.dumps(objects_list)
    else:
        abort(400, "Doh! " + device_id + " is not a valid ID or it is not enrolled in HOMEr")




@get('/gethistory')  # used to add a new device to the system
def getHistory():
    history_index = request.params.get('index')
    entry_count = request.params.get('count')

    #if HomerHelper.idCheck(con, 'Devices', device_id):
    try:
        sql_query = ("SELECT * FROM `History` ORDER BY `timestamp` DESC LIMIT %s;" % entry_count)
        #print sql_query
        cur = db.query(sql_query, None)

        row = cur.fetchall()  # device IDs unique so just get one record
        objects_list = []  # parser for the information returned
        print row
        for col in row:
            d = collections.OrderedDict()
            d['name'] = col['name']
            d['timestamp'] = col["timestamp"].strftime("%B %d, %Y")
            d['event'] = col["event"]
            d['id'] = col["id"]
            objects_list.append(d)

        return json.dumps(objects_list)
    except MySQLdb.IntegrityError:
        abort(400, "Doh! Device doesnt exist")
    #else:
    #    abort(400, "Doh! Device ID was not found")


@delete('/removedevice')  # returns all devices registered in teh system
def removeDevice():
    device_id = request.forms.get('id')

    if HomerHelper.idCheck('Devices', device_id):  #validate the device ID
        device_name = HomerHelper.getDeviceName(con, device_id)
        try:
            db.query("DELETE FROM Devices WHERE id = %s", device_id)
            HomerHelper.insert_history(con, device_name, device_id, "device removed")
            return "OK"
        except MySQLdb.IntegrityError:
            abort(400, "Doh! Unable to remove device. ")
    else:
        abort(400,"Doh! " + device_id + " is not a valid ID or it is not enrolled in HOMEr")

@post('/adddevice')  # used to add a new device to the system
def addDevice():
    device_name = request.forms.get('name')
    device_type = request.forms.get('type')
    device_function = request.forms.get('function')
    device_id = request.forms.get('id')

    if re.match(r"\w+\s\w+", device_name) is not None: # check that the device name is alphanumeric
        if re.match(r"\w+$", device_type) is not None: # check that device type is alphanumeric
            if re.match(r"[a-zA-Z0-9]{0,128}$", device_id) is not None: # check that id only has letters and numbers
                try:
                    sql_insert = "INSERT INTO `Devices`(`name`, `type`, `function`, `id`) VALUES (%s,%s,%s,%s)"
                    db.query(sql_insert, (device_name, device_type, device_function, device_id))

                    HomerHelper.insert_history(con,device_name, device_id, "device added")

                except MySQLdb.IntegrityError:
                    abort(400, "Doh! Device exsists")

                try:
                    cur = db.query("SELECT * FROM Devices WHERE id = %s", device_id)
                    rows = cur.fetchall()

                    objects_list = []
                    for row in rows:
                        d = collections.OrderedDict()
                        d['name'] = row["name"]
                        d['type'] = row["type"]
                        d['function'] = row["function"]
                        d['id'] = row["id"]
                        objects_list.append(d)

                    return json.dumps(objects_list)

                except MySQLdb.IntegrityError:
                    abort(400, "Doh! Adding user failed")
            else:
                abort(400, "Doh! That request was no bueno.  The id is invalid." + device_id)
        else:
             abort(400,"Doh! That request was no bueno.  The type is invalid")
    else:
        abort(400, "Doh! That request was no bueno.  The name is invalid")

###
@get('/getusers')  # returns all devices registered in teh system
def getUsers():
    cur = db.query("SELECT * FROM Users", None)
    row = cur.fetchall()
    objects_list = []  # parser for the information returned
    for col in row:
        d = collections.OrderedDict()
        d['id'] = col["id"]
        d['name'] = col["name"]
        d['location'] = col["location"]
        objects_list.append(d)
        j = json.dumps(objects_list)

    return (j)

@delete('/removeuser')  # returns all devices registered in teh system
def removeUser():
    user_id = request.forms.get('id')

    if HomerHelper.idCheck('Users', user_id):  #validate the device ID
        user_name = HomerHelper.getUserName(con, user_id)
        try:
            db.query("DELETE FROM Users WHERE id = %s", user_id)
            #con.commit()
            HomerHelper.insert_history(con, user_name, user_id, "user removed")

            return("OK")

        except MySQLdb.IntegrityError:
            abort(400, "Doh! Unable to remove device. ")
    else:
        err_msg = "Doh! That request was no bueno. %s is not a valid ID or it is not enrolled in HOMEr" % user_id
        abort(400, err_msg)

@post('/adduser')  # used to add a new device to the system
def addUser():
    user_name = request.forms.get('name')
    user_id = request.forms.get('id')

    if re.match(r"\w+$", user_name) is not None: # check that the device name is alphanumeric
        if re.match(r"[a-zA-Z0-9]{0,128}$", user_id) is not None: # check that id only has letters & numbers
            try:
                sql_insert = "INSERT INTO `Users`(`name`, `id`) VALUES (%s,%s)"
                db.query(sql_insert, (user_name, user_id))
                HomerHelper.insert_history(con, user_name, user_id, "device added")

                cur = db.query("SELECT * FROM Users WHERE id = %s", user_id)
                row = cur.fetchone()

                objects_list = []
                d = collections.OrderedDict()
                d['name'] = row["name"]
                d['id'] = row["id"]
                objects_list.append(d)

                return json.dumps(objects_list)

            except MySQLdb.IntegrityError:
                abort(400, "Doh! Device exsists")
        else:
            abort(400, "Doh! That request was no bueno.  The id is invalid.")
    else:
        abort(400, "Doh! That request was no bueno.  The name is invalid")
###

@post('/setbrightness')  # used to add a new device to the system
def setBrightness():
    #MANDATORY FIELDS FROM REQUEST
    #DEVICE ID AS id
    #STATE TO ASSIGN TO DEVICE AS state

    device_id = request.params.get('id')
    brightness = request.params.get('brightness')

    if HomerHelper.idCheck('Devices', device_id):  # validate the ID
        device_function = HomerHelper.getDeviceFunction(con, device_id)
        brightness_location = HomerHelper.lookupDeviceAttribute(con, device_function, 'Brightness')
        if brightness_location is not None:
            try:
                sql_update = "UPDATE `Devices` SET %s " % brightness_location  # write it the same column in devices
                sql_update += "= %s  WHERE id = %s"
                db.query(sql_update, (brightness, device_id))
                #con.commit()


                device_name = HomerHelper.getDeviceName(con, device_id)
                device_type = HomerHelper.getDeviceType(con, device_id)
                DeviceComunication.sendDeviceBrightness(device_id, device_type, brightness)
                history_event = "set brightness to: " + brightness
                HomerHelper.insert_history(con, device_name, device_id, history_event)


                d = collections.OrderedDict()
                d['name'] = device_name
                d['brightness'] = brightness

                return json.dumps(d)



            except MySQLdb.IntegrityError:
                abort(400, "Doh! Device doesnt exist")
        else:
            abort(400, "Device does not have brightness attribute")
    else:
        abort(400, "Doh! Device ID was not found")


@get('/getbrightness')  # used to add a new device to the system
def getBrightness():
    device_id = request.params.get('id')

    if HomerHelper.idCheck('Devices', device_id):
        device_function = HomerHelper.getDeviceFunction(con, device_id)
        brightness_location = HomerHelper.lookupDeviceAttribute(con, device_function, 'Brightness')
        if brightness_location is not None:   #"SELECT `value1` FROM Devices WHERE id = %s"
            try:
                sql_query = "SELECT %s FROM Devices " % brightness_location  # write it the same column in devices
                sql_query += "WHERE id = %s"
                cur = db.query(sql_query, device_id)

                row = cur.fetchone()  # device IDs unique so just get one record
                device_brightness = 'brightness', row[brightness_location]
                return json.dumps(device_brightness)
            except MySQLdb.IntegrityError:
                abort(400, "Doh! Device doesnt exist")
        else:
            abort(400, "device does not have brightness attribute")
    else:
        abort(400, "Doh! Device ID was not found")

@post('/setstate')  # set the state for devices that support the attribute
def setState():
    #MANDATORY FIELDS FROM REQUEST
    #DEVICE ID AS id
    #STATE TO ASSIGN TO DEVICE AS state

    device_id = request.params.get('id')  # get device ID from request
    device_state = request.params.get('state')  # get state to assign

    if HomerHelper.idCheck('Devices', device_id):  # validate the ID
        device_function = HomerHelper.getDeviceFunction(con, device_id)
        state_location = HomerHelper.lookupDeviceAttribute(con, device_function, 'State')
        if state_location is not None:
            try:
                sql_update = "UPDATE `Devices` SET %s " % state_location  # write it the same column in devices
                sql_update += "= %s  WHERE id = %s"
                db.query(sql_update, (device_state, device_id))

                #call state.action or scene here.  TBD
                device_name = HomerHelper.getDeviceName(con, device_id)  # lookup the name, needed for history
                device_type = HomerHelper.getDeviceType(con, device_id)  # lookup the device type needed for history
                history_event = "set state to: " + device_state
                HomerHelper.insert_history(con, device_name, device_id, history_event)
                return "OK"

            except MySQLdb.IntegrityError:
                abort(400, "Doh! Device doesnt exist")
        else:
            abort(400, "device does not have state attribute")
    else:
        abort(400, "Doh! Device ID was not found") # lookup the device function




@get('/getstate')  # used to add a new device to the system
def getState():
    device_id = request.params.get('id')

    if HomerHelper.idCheck('Devices', device_id):
        device_function = HomerHelper.getDeviceFunction(con, device_id)
        state_location = HomerHelper.lookupDeviceAttribute(con, device_function, 'State')
        if state_location is not None:   #"SELECT `value1` FROM Devices WHERE id = %s"
            try:
                sql_query = "SELECT %s FROM Devices " % state_location  # write it the same column in devices
                sql_query += "WHERE id = %s"
                cur = db.query(sql_query, device_id)

                row = cur.fetchone()  # device IDs unique so just get one record
                device_state = 'state', row[state_location]
                return json.dumps(device_state)

            except MySQLdb.IntegrityError:
                abort(400, "Doh! Device doesnt exist")
        else:
            abort(400, "device does not have state attribute")
    else:
        abort(400, "Doh! Device ID was not found")


@post('/savepicture')
def savePicture():
    device_id = request.params.get('id')  # get device ID from request
    picture_location = request.params.get('pictureURL')

    if HomerHelper.idCheck('Devices', device_id):  # validate the ID
        try:
            file = urllib.urlopen(picture_location).read()
            sql_insert = 'INSERT INTO `Images`(`device_id`, `image`) VALUES (%s, %s)'
            db.query(sql_insert, (device_id, file))

            device_name = HomerHelper.getDeviceName(con, device_id)  # lookup the name, needed for history
            history_event = "stored picture from  " + picture_location
            HomerHelper.insert_history(con, device_name, device_id, history_event)

            return "OK"
        except MySQLdb.IntegrityError:
            abort(400, "Doh! Device doesnt exist")
        except urllib2.URLError:
            abort(400, "failed to store image from source, check the url")
    else:
        abort(400, "Doh! Device ID was not found") # lookup the device function


@get('/getpicture')
def getPicture():
    image_id = request.params.get('id')

    if HomerHelper.idCheck('Images', image_id):  # images IDs are unique so return only one image
        try:
            cur = db.query("SELECT `image` FROM `Images` WHERE id = %s", image_id)

            row = cur.fetchone()  # image IDs unique so just get one record
            response.content_type = 'image/jpg'
            return row['image']

        except MySQLdb.IntegrityError:
            abort(400, "Doh! Device doesnt exist")
    else:
        abort(400, "Doh! Image ID was not found")


@get('/getlocation') # used to add a new device to the system
def getlocation():
    user_id = request.params.get('id')

    if HomerHelper.idCheck('Users', user_id):
        try:
            cur = db.query("SELECT `location` FROM `Users` WHERE id = %s", user_id)

            row = cur.fetchone()  # User IDs unique so just get one record

            user_location = 'location', row['location']
            return json.dumps(user_location)

        except MySQLdb.IntegrityError:
            abort(400, "Doh! User doesnt exist")

    else:
        abort(400, "Doh! User ID was not found")

@post('/setlocation')  # used to add a new device to the system
def setLocation():
    user_id = request.params.get('id')
    user_location = request.params.get('location')

    if HomerHelper.userIdCheck(con, user_id):
        user_name = HomerHelper.getUserName(con, user_id)

        try:
            sql_update = "UPDATE `Users` SET `Location`= %s  WHERE ID = %s"
            db.query(sql_update, (user_location, user_id))
            history_event = "set user location to: " + user_location
            HomerHelper.insert_history(con, user_name, user_id, history_event)
            return "OK"

        except MySQLdb.IntegrityError:
            abort(400, "Doh! User doesn't exist")
    else:
        abort(400, "Doh! User ID was not found")


@post('/setcolor')  # used to add a new device to the system
def setColor():
    device_id = request.params.get('id')
    device_color = request.params.get('color')
    device_state = request.params.get('mode')

    if HomerHelper.idCheck('Devices', device_id):  # validate the ID
        device_name = HomerHelper.getDeviceName(con, device_id)
        device_type = HomerHelper.getDeviceType(con, device_id)
        device_function = HomerHelper.getDeviceFunction(con, device_id)
        state_location = HomerHelper.lookupDeviceAttribute(con, device_function, 'State')
        if state_location is not None:
            try:
                sql_update = "UPDATE `Devices` SET %s " % state_location  # write it the same column in devices
                sql_update += "= %s  WHERE id = %s"
                db.query(sql_update, (device_state, device_id))
            except MySQLdb.IntegrityError:
                abort(400, "Doh! Device doesnt exist")

            color_location = HomerHelper.lookupDeviceAttribute(con, device_function, 'Color')
            if color_location is not None:
                try:
                    sql_update = "UPDATE `Devices` SET %s " % color_location  # write it the same column in devices
                    sql_update += "= %s  WHERE id = %s"
                    db.query(sql_update, (device_color, device_id))
                except MySQLdb.IntegrityError:
                    abort(400, "Doh! Device doesnt exist")
            else:
                abort(400, "Device does not have color attribute")
        else:
            abort(400, "Device does not have mode attribute")

        t = threading.Thread(target=DeviceComunication.sendDeviceColor, args=(device_id, device_color, device_state))
        t.start()
        history_event = "set color to: " + device_color + "set mode to " + device_state
        HomerHelper.insert_history(con, device_name, device_id, history_event)
        return "OK"
    else:
        abort(400, "Doh! Device ID was not found")

@get('/getcolor')  # used to add a new device to the system
def getColor():
    device_id = request.params.get('id')

    if HomerHelper.idCheck('Devices', device_id):
        device_function = HomerHelper.getDeviceFunction(con, device_id)
        state_location = HomerHelper.lookupDeviceAttribute(con, device_function, 'State')
        color_location = HomerHelper.lookupDeviceAttribute(con, device_function, 'Color')
        if state_location is not None:
            if color_location is not None:
                try:
                    sql_query = "SELECT id, %s, %s FROM Devices " % (state_location, color_location)
                    sql_query += "WHERE id = %s"
                    cur = db.query(sql_query, device_id)

                    row = cur.fetchone()  # device IDs unique so just get one record

                    objects_list = []
                    d = collections.OrderedDict()
                    d['id'] = row['id']
                    d['mode'] = row[state_location]
                    d['color'] = row[color_location]
                    objects_list.append(d)

                    return json.dumps(objects_list)

                except MySQLdb.IntegrityError:
                    abort(400, "Doh! Device doesnt exist")
            else:
                abort(400, "Device does not have color attribute")
        else:
            abort(400, "Device does not have mode attribute")
    else:
        abort(400, "Doh! Device ID was not found")


@route('/')
@view('index')
def index():
    return template('default')

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

@get('/viewbrightness')
def viewBrightness():
    cur = db.query("SELECT * FROM `Devices` WHERE function = %s", 'lamp')
    row = cur.fetchall()
    brightness_location = HomerHelper.lookupDeviceAttribute(con, 'lamp', 'Brightness')
    html = []  # parser for the information returned
    for col in row:
        lampdevices = (col['name'], str((int(col[brightness_location])*100 )/255),col['id'])
        print lampdevices
        html.append(lampdevices)
    return template('brightness', devices=html)


@get('/viewhistory')
def viewHistory():
    #history_index = request.params.get('index')
    entry_count = '25'
    try:
        sql_query = ("SELECT * FROM `History` ORDER BY `timestamp` DESC LIMIT %s;" % entry_count)
        cur = db.query(sql_query, None)
        row = cur.fetchall()  # device IDs unique so just get one record
        history = []  # parser for the information returned
        i = 0
        for col in row:
            i += 1
            historyEntry = (
                i ,
                col['name'],
                col["timestamp"].strftime("%c"),
                col["event"],
                col["id"],
                )
            history.append(historyEntry)
        return template('history', entries=history)
    except MySQLdb.IntegrityError:
        abort(400, "Doh! Device doesnt exist")

