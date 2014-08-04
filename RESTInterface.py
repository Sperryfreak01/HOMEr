__author__ = 'matt'

from bottle import *
import MySQLdb
import collections
import json
import urllib
import re
import threading
import HomerHelper
import Notifications
import DeviceComunication


#t = threading.Thread(target=Notifications.sparkAlarm, args=("53ff73065075535133081687", "064,000,255", "e8a5241dee80316554e4f72c516ecf3ff26e15f6"))
#t.start()

con = MySQLdb.connect('192.168.2.1', 'HOMEr', 'HOMEr', 'HOMEr');
IMP_API = "https://agent.electricimp.com/"
SPARK_API = "https://api.spark.io/v1/"

@get('/getdevices')  # returns all devices registered in teh system
def getDevices():
    with con:
        cur = con.cursor(MySQLdb.cursors.DictCursor)  # open connection to DB
        cur.execute("SELECT * FROM Devices ")

        row = cur.fetchall()

        objects_list = []  # parser for the information returned
        for col in row:
            d = collections.OrderedDict()
            d['name'] = col["name"]
            d['type'] = col["type"]
            d['function'] = col["function"]
            d['id'] = col["id"]
            objects_list.append(d)
            j = json.dumps(objects_list)

    return (j)

@delete('/removedevice')  # returns all devices registered in teh system
def removeDevice():
    cur = con.cursor(MySQLdb.cursors.DictCursor)  # open connection to DB
    device_id = request.forms.get('id')

    if HomerHelper.idCheck(con, 'Devices', device_id):  #validate the device ID
        device_name = HomerHelper.getDeviceName(con, device_id)
        with con:
            try:
                cur.execute("DELETE FROM Devices WHERE id = %s", (device_id))
                con.commit()
                HomerHelper.insert_history(con, device_name, device_id, "device removed")
            except MySQLdb.IntegrityError:
                #logging.warn("failed to insert values %d, %s", id, filename)
                abort(400, "Doh! Unable to remove device. ")
        return("OK")
    else:
        abort(400,"Doh! That request was no bueno. " + device_id + " is not a valid ID or it is not enrolled in HOMEr")

@post('/adddevice')  # used to add a new device to the system
def addDevice():
    cur = con.cursor(MySQLdb.cursors.DictCursor)

    device_name = request.forms.get('name')
    device_type = request.forms.get('type')
    device_function = request.forms.get('function')
    device_id = request.forms.get('id')

    if re.match(r"\w+$", device_name) is None: # check that the device name is alphanumeric
        abort(400, "Doh! That request was no bueno.  The name is invalid")
    if re.match(r"\w+$", device_type) is None: # check that device type is alphanumeric
        abort(400,"Doh! That request was no bueno.  The type is invalid")
    if re.match(r"[a-zA-Z0-9]{0,128}$", device_id) is None: # check that id only has letters and numbers
        abort(400, "Doh! That request was no bueno.  The id is invalid." + device_id)
    else:
        with con:
            try:
                sql_insert = "INSERT INTO `Devices`(`name`, `type`, `function`, `id`) VALUES (%s,%s,%s,%s)"
                cur.execute(sql_insert, (device_name,device_type,device_function,device_id))
                con.commit()
                HomerHelper.insert_history(con,device_name, device_id, "device added")
                #logging.warn("%d", affected_count)
                #logging.info("inserted values %d, %s", id, filename)
            except MySQLdb.IntegrityError:
                #logging.warn("failed to insert values %d, %s", id, filename)
                abort(400, "Doh! Device exsists")

        cur.execute("SELECT * FROM Devices WHERE id = %s", device_id)
        rows = cur.fetchall()

        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['name'] = row["name"]
            d['type'] = row["type"]
            d['function'] = row["function"]
            d['id'] = row["id"]
            objects_list.append(d)
            j = json.dumps(objects_list)
            print(j)
        return(j)

###
@get('/getusers')  # returns all devices registered in teh system
def getUsers():
    with con:
        cur = con.cursor(MySQLdb.cursors.DictCursor)  # open connection to DB
        cur.execute("SELECT * FROM Users")

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
    cur = con.cursor(MySQLdb.cursors.DictCursor)  # open connection to DB
    user_id = request.forms.get('id')

    if HomerHelper.idCheck(con, 'Users', user_id):  #validate the device ID
        user_name = HomerHelper.getUserName(con, user_id)
        with con:
            try:
                cur.execute("DELETE FROM Users WHERE id = %s", (user_id))
                con.commit()
                HomerHelper.insert_history(con, user_name, user_id, "device removed")
            except MySQLdb.IntegrityError:
                #logging.warn("failed to insert values %d, %s", id, filename)
                abort(400, "Doh! Unable to remove device. ")
        return("OK")
    else:
        err_msg = "Doh! That request was no bueno. %s is not a valid ID or it is not enrolled in HOMEr" % user_id
        abort(400, err_msg)

@post('/adduser')  # used to add a new device to the system
def addUser():
    cur = con.cursor(MySQLdb.cursors.DictCursor)

    user_name = request.forms.get('name')
    user_id = request.forms.get('id')

    if re.match(r"\w+$", user_name) is None: # check that the device name is alphanumeric
        abort(400, "Doh! That request was no bueno.  The name is invalid")
    if re.match(r"[a-zA-Z0-9]{0,128}$", user_id) is None: # check that id only has letters and numbers
        abort(400, "Doh! That request was no bueno.  The id is invalid." + user_id)
    else:
        with con:
            try:
                sql_insert = "INSERT INTO `Users`(`name`, `id`) VALUES (%s,%s)"
                cur.execute(sql_insert, (user_name,user_id))
                con.commit()
                HomerHelper.insert_history(con, user_name, user_id, "device added")
                #logging.warn("%d", affected_count)
                #logging.info("inserted values %d, %s", id, filename)
            except MySQLdb.IntegrityError:
                #logging.warn("failed to insert values %d, %s", id, filename)
                abort(400, "Doh! Device exsists")

        cur.execute("SELECT * FROM Users WHERE id = %s", user_id)
        row = cur.fetchone()

        objects_list = []
        d = collections.OrderedDict()

        d['name'] = row["name"]
        d['id'] = row["id"]
        objects_list.append(d)

        return json.dumps(objects_list)
###

@post('/setbrightness')  # used to add a new device to the system
def setBrightness():
    cur = con.cursor(MySQLdb.cursors.DictCursor)
    #MANDATORY FIELDS FROM REQUEST
    #DEVICE ID AS id
    #STATE TO ASSIGN TO DEVICE AS state

    device_id = request.params.get('id')
    brightness = request.params.get('brightness')

    if HomerHelper.idCheck(con, 'Devices', device_id):  # validate the ID
        device_function = HomerHelper.getDeviceFunction(con, device_id)
        state_location = HomerHelper.lookupAttribute(con, device_function, 'Brightness')
        if state_location is not None:
            try:
                sql_update = "UPDATE `Devices` SET %s " % state_location  # write it the same column in devices
                sql_update += "= %s  WHERE id = %s"
                cur.execute(sql_update, (brightness, device_id))
                con.commit()

                device_name = HomerHelper.getDeviceName(con, device_id)
                device_type = HomerHelper.getDeviceType(con, device_id)
                DeviceComunication.sendDeviceBrightness(device_id, device_type, brightness)
                history_event = "set brightness to: " + brightness
                HomerHelper.insert_history(con, device_name, device_id, history_event)

                return "OK"

            except MySQLdb.IntegrityError:
                abort(400, "Doh! Device doesnt exist")
        else:
            abort(400, "device does not have brightness attribute")
    else:
        abort(400, "Doh! Device ID was not found")

@get('/getbrightness')  # used to add a new device to the system
def getBrightness():
    cur = con.cursor(MySQLdb.cursors.DictCursor)

    device_id = request.params.get('id')

    if HomerHelper.idCheck(con, 'Devices', device_id):
        device_type = HomerHelper.getDeviceType(con, device_id)
        if device_type == "imp":
            url = IMP_API
        elif device_type == "spark":
            url = "something!!!!"
    else:
        abort(400, "Doh! Device ID was not found")

    with con:
        cur.execute("SELECT `value1` FROM Devices WHERE id = %s", device_id)

        row = cur.fetchall()
        objects_list = []
        for col in row:
            d = collections.OrderedDict()
            d['brightness'] = col["value1"]
            objects_list.append(d)
            j = json.dumps(objects_list)
            print(j)
        return(j)

@post('/setstate')  # set the state for devices that support the attribute
def setState():
    cur = con.cursor(MySQLdb.cursors.DictCursor)
    #MANDATORY FIELDS FROM REQUEST
    #DEVICE ID AS id
    #STATE TO ASSIGN TO DEVICE AS state

    device_id = request.params.get('id')  # get device ID from request
    device_state = request.params.get('state')  # get state to assign

    if HomerHelper.idCheck(con, 'Devices', device_id):  # validate the ID
        device_function = HomerHelper.getDeviceFunction(con, device_id)
        state_location = HomerHelper.lookupAttribute(con, device_function, 'State')
        if state_location is not None:
            try:
                sql_update = "UPDATE `Devices` SET %s " % state_location  # write it the same column in devices
                sql_update += "= %s  WHERE id = %s"
                cur.execute(sql_update, (device_state, device_id))
                con.commit()
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
    cur = con.cursor(MySQLdb.cursors.DictCursor)

    device_id = request.params.get('id')

    if HomerHelper.idCheck(con,'Devices', device_id):
        device_type = HomerHelper.getDeviceType(con, device_id)
        if device_type == "imp":
            url = IMP_API
        elif device_type == "spark":
            url = "something!!!!"
    else:
        abort(400, "Doh! Device ID was not found")

    with con:
        cur.execute("SELECT `value1` FROM Devices WHERE id = %s", device_id)

        row = cur.fetchall()
        objects_list = []
        for col in row:
            d = collections.OrderedDict()
            d['brightness'] = col["value1"]
            objects_list.append(d)
            j = json.dumps(objects_list)
            print(j)
        return(j)

@post('/savepicture')
def savePicture():
    cur = con.cursor(MySQLdb.cursors.DictCursor)

    picture_location = request.params.get('pictureURL')

    try:
        file = urllib.urlopen(picture_location).read()
        #image = Image.open(file)
    except:
        print "Unable to load image"

    #sql = 'INSERT INTO img(images) VALUES(%s)'
    sql_insert = 'INSERT INTO `Images`(`id`, `image`) VALUES (%s,%s)'
    cur.execute(sql_insert, ("test", file))
    con.commit()

    return "OK"

@get('/getpicture')
def getPicture():
    cur = con.cursor(MySQLdb.cursors.DictCursor)

    image_id = request.params.get('id')
    if HomerHelper.idCheck(con, 'Images', image_id):
        with con:
            cur.execute("SELECT `image` FROM `Images` WHERE id = %s", image_id)

            row = cur.fetchone()  # image IDs unique so just get one record
            response.content_type = 'image/jpg'
            return row['image']

    else:
        abort(400, "Doh! Image ID was not found")



@get('/getlocation')  # used to add a new device to the system
def getlocation():
    cur = con.cursor(MySQLdb.cursors.DictCursor)

    user_id = request.params.get('id')

    if HomerHelper.idCheck(con, 'Users', user_id):
        with con:
            cur.execute("SELECT `location` FROM `Users` WHERE id = %s", user_id)

            row = cur.fetchone()  # User IDs unique so just get one record

            user_location = 'location', row['location']
            print user_location
            return json.dumps(user_location)

    else:
        abort(400, "Doh! User ID was not found")



@post('/setlocation')  # used to add a new device to the system
def setLocation():
    cur = con.cursor(MySQLdb.cursors.DictCursor)

    user_id = request.params.get('id')
    user_location = request.params.get('location')


    if HomerHelper.userIdCheck(con, user_id):
        user_name = HomerHelper.getUserName(con, user_id)
        with con:
            try:
                sql_update = "UPDATE `Users` SET `Location`= %s  WHERE ID = %s"
                cur.execute(sql_update, (user_location, user_id))
                history_event = "set user location to: " + user_location
                HomerHelper.insert_history(con, user_name, user_id, history_event)
            except MySQLdb.IntegrityError:
                abort(400, "Doh! Device exsists")
        return "OK"
    else:
        abort(400, "Doh! User ID was not found")
