__author__ = 'matt'
#!/usr/bin/python
# -*- coding: utf-8 -*-

from bottle import *
import MySQLdb
import collections
import json
import HOMEr_history
import urllib

con = MySQLdb.connect('192.168.2.1', 'HOMEr', 'HOMEr', 'HOMEr');
impapi = "https://agent.electricimp.com/"

########################################################################

@get('/getdevices')  # returns all devices registered in teh system
def get_devices():
    with con:
        cur = con.cursor(MySQLdb.cursors.DictCursor)  # open connection to DB
        cur.execute("SELECT * FROM Devices ")

        rows = cur.fetchall()

        objects_list = []  # parser for the information returned
        for row in rows:
            d = collections.OrderedDict()
            d['name'] = row["name"]
            d['type'] = row["type"]
            d['function'] = row["function"]
            d['id'] = row["id"]
            objects_list.append(d)
            j = json.dumps(objects_list)
    return (j)


@delete('/removedevice')  # returns all devices registered in teh system
def remove_device():
    cur = con.cursor(MySQLdb.cursors.DictCursor)  # open connection to DB
    device_id = request.forms.get('id')

    if re.match(r"[a-zA-Z0-9]{0,128}$", device_id) is None: # check that id only has letters and numbers
        abort(400, "Doh! That request was no bueno.  The id is invalid." + device_id)
    if HOMEr_history.device_exsists(con, device_id) is True:
        device_name = HOMEr_history.getdevicename(con, device_id)
        with con:
            try:
                cur.execute("DELETE FROM Devices WHERE id = %s", (device_id))
                con.commit()
                HOMEr_history.insert_history(con, device_name, device_id, "device removed")
            except MySQLdb.IntegrityError:
                #logging.warn("failed to insert values %d, %s", id, filename)
                abort(400, "Doh! That request was no bueno. No such device")
        return("OK")
    else:
        abort(400,"Doh! That request was no bueno.  The id is invalid." + device_id)

@post('/adddevice')  # used to add a new device to the system
def add_device():
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
                HOMEr_history.insert_history(con,device_name, device_id, "device added")
                #logging.warn("%d", affected_count)
                #logging.info("inserted values %d, %s", id, filename)
            except MySQLdb.IntegrityError:
                #logging.warn("failed to insert values %d, %s", id, filename)
                abort(400, "Doh! Device exsists")

        cur.execute("SELECT * from Devices where name = '" + device_name + "'")
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

@post('/setbrightness')  # used to add a new device to the system
def set_brightness():
    cur = con.cursor(MySQLdb.cursors.DictCursor)

    device_id = request.forms.get('id')
    brightness = request.forms.get('brightness')

    if re.match(r"[a-zA-Z0-9]{0,128}$", device_id) is None: # check that id only has letters and numbers
        abort(400, "Doh! That request was no bueno.  The id is invalid." + device_id)
    else:
        cur.execute("SELECT * from Devices where id = %s", device_id)
        row = cur.fetchall()
        if not row:
            abort(400, "Doh! Device ID was not found")
        else:
            for col in row:
                device_type = col["type"]
                device_name = col["name"]
                if device_type == "imp":
                    url = impapi
                elif device_typer == "spark":
                    url = "something!!!!"
        urllib.urlopen(impapi + device_id + "?setbrightness= " + brightness)
        history_event = "set brightness to: " + brightness
        HOMEr_history.insert_history(con,device_name, device_id, history_event)

        return("OK")


run(reloader=True, host='0.0.0.0', port=8080, debug=True)
