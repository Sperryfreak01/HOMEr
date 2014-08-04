### This file contains helper functions invoked by HOMEr

__author__ = 'matt'

import MySQLdb
import re

def insert_history(con, device_name,device_id,event):
    cur = con.cursor(MySQLdb.cursors.DictCursor)

    with con:
        try:
           # print device_name
            sql_insert = "INSERT INTO `History`(`name`, `id`, `event`) VALUES (%s,%s,%s)"
            cur.execute(sql_insert, (device_name, device_id, event))
            con.commit()
            #logging.warn("%d", affected_count)
            #logging.info("inserted values %d, %s", id, filename)
        except MySQLdb.IntegrityError:
            #logging.warn("failed to insert values %d, %s", id, filename)
            #abort(400, "Doh! History was forgotten")
            print ("log entry exception")

        cur.execute("SELECT * from Devices where name = '" + device_name + "'")
        rows = cur.fetchall()

    return()

def deviceExsists(con, id):
    cur = con.cursor(MySQLdb.cursors.DictCursor)  # open connection to DB
    device_id = ""
    with con:
        print(id)
        cur.execute("SELECT * FROM Devices WHERE id = %s", id)

    row = cur.fetchall()
    for col in row:
        device_id = col["id"]

    if device_id is "":
        return (False)
    else:
        return (True)

def getDeviceName(con, id):
    cur = con.cursor(MySQLdb.cursors.DictCursor)  # open connection to DB
    with con:
        cur.execute("SELECT `name` FROM Devices WHERE id = %s", id)

    row = cur.fetchall()
    for col in row:
        device_name = col["name"]
    if device_name is None:
        return ""
    else:
        return device_name

def getDeviceType(con, id):
    cur = con.cursor(MySQLdb.cursors.DictCursor)  # open connection to DB
    with con:
        cur.execute("SELECT `type` FROM Devices WHERE id = %s", id)

    row = cur.fetchall()
    for col in row:
        device_type = col["type"]
    if device_type is None:
        return ""
    else:
        return device_type

def getDeviceFunction(con, id):
    cur = con.cursor(MySQLdb.cursors.DictCursor)  # open connection to DB
    with con:
        cur.execute("SELECT `function` FROM Devices WHERE id = %s", id)

    row = cur.fetchall()
    for col in row:
        device_function = col["function"]
    if device_function is None:
        return ""
    else:
        return device_function

def deviceIdCheck(con, id):
    cur = con.cursor(MySQLdb.cursors.DictCursor)  # open connection to DB

    if re.match(r"[a-zA-Z0-9]{0,128}$", id) is None: # check that id only has letters and numbers
        return False
    else:
        cur.execute("SELECT * FROM Devices WHERE id = %s", id)
        row = cur.fetchall()
        if row:
            return True
        else:
            return False

def userIdCheck(con, id):
    cur = con.cursor(MySQLdb.cursors.DictCursor)  # open connection to DB

    if re.match(r"[a-zA-Z0-9]{0,128}$", id) is None: # check that id only has letters and numbers
        return False
    else:
        cur.execute("SELECT * FROM Users WHERE id = %s", id)
        row = cur.fetchall()
        if row:
            return True
        else:
            return False

def idCheck(con, id_type, id):
    cur = con.cursor(MySQLdb.cursors.DictCursor)  # open connection to DB

    if re.match(r"[a-zA-Z0-9]{0,128}$", id) is None: # check that id only has letters and numbers
        return False
    else:
        sql_query = ("SELECT `id` FROM %s " % id_type)
        sql_query +=("WHERE id = %s")
        cur.execute(sql_query, (id))
        row = cur.fetchall()
        if row:
            return True
        else:
            return False

def getUserName(con, id):
    cur = con.cursor(MySQLdb.cursors.DictCursor)  # open connection to DB
    with con:
        cur.execute("SELECT `name` FROM Users WHERE id = %s", id)

    row = cur.fetchall()
    for col in row:
        device_name = col["name"]
    if device_name is None:
        return ""
    else:
        return device_name

def lookupAttribute(con, function, attr_name):
    cur = con.cursor(MySQLdb.cursors.DictCursor)

    try:
        sql_querry = "SELECT * FROM `Device_Types` WHERE type = %s"
        cur.execute(sql_querry, function)
        row = cur.fetchone()
        for x in xrange(1, 10):
            col_name = "value%d" % x  # iterate through attribute field looking for the column we need
            if row[col_name] == attr_name:
                return col_name
            else:
                return None
    except MySQLdb.IntegrityError:
            return None


