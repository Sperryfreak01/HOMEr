__author__ = 'matt'
#!/usr/bin/python
# -*- coding: utf-8 -*-

from bottle import *
import MySQLdb
import collections
import json

con = MySQLdb.connect('192.168.2.1', 'HOMEr', 'HOMEr', 'HOMEr');


########################################################################

@get('/getdevices')
def get_devices():
    with con:
        cur = con.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Devices ")

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
    return(j)


@post('/adddevice')
def add_device():
    cur = con.cursor(MySQLdb.cursors.DictCursor)

    device_name = request.forms.get('name')
    device_type = request.forms.get('type')
    device_function = request.forms.get('function')
    device_id = request.forms.get('id')

    if device_name == "":
        abort(400, "Doh! That request was no bueno")
    elif device_type == "":
        abort(400, "Doh! That request was no bueno")
    elif device_function == "":
        abort(400, "Doh! That request was no bueno")
    elif device_id == "":
        abort(400, "Doh! That request was no bueno")
    else:
        sql_insert = "INSERT INTO `Devices`(`name`, `type`, `function`, `id`) VALUES (%s,%s,%s,%s)"

        try:
            cur.execute(sql_insert, (device_name,device_type,device_function,device_id))
            con.commit()
            #logging.warn("%d", affected_count)
            #logging.info("inserted values %d, %s", id, filename)
        except MySQLdb.IntegrityError:
            #logging.warn("failed to insert values %d, %s", id, filename)
            abort(400, "Doh! Device exsists")

        cur.execute("SELECT * from Devices where name = '" + device_name + "'")

        rows = cur.fetchall()
        print(rows)
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

run(reloader=True, host='0.0.0.0', port=8080, debug=True)
