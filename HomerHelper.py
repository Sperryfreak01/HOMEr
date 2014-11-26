### This file contains helper functions invoked by HOMEr

__author__ = 'matt'

import MySQLdb
import re


class DB:
  conn = None

  def connect(self):
    self.conn = MySQLdb.connect('192.168.2.1', 'HOMEr', 'HOMEr', 'HOMEr')
    self.conn.autocommit(True)

  def query(self, sql, options):
    try:
        print (sql, options)
        cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql, options)
        #self.conn.commit()
    except (AttributeError, MySQLdb.OperationalError):
        self.connect()
        cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql, options)
        #self.conn.commit()
    return cursor

db = DB()

def insert_history(con, device_name,device_id,event):
    try:
       # print device_name
        sql_insert = "INSERT INTO `History`(`name`, `id`, `event`) VALUES (%s,%s,%s)"
        cur = db.query(sql_insert, (device_name, device_id, event))
        #logging.warn("%d", affected_count)
        #logging.info("inserted values %d, %s", id, filename)
    except MySQLdb.IntegrityError:
        #logging.warn("failed to insert values %d, %s", id, filename)
        #abort(400, "Doh! History was forgotten")
        print ("log entry exception")
    cur = db.query("SELECT * from Devices where name = '" + device_name + "'", None)
    rows = cur.fetchall()

    return()

def deviceExsists(con, id):
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

def getDeviceName(con, id):
    cur = db.query("SELECT `name` FROM Devices WHERE id = %s", id)

    row = cur.fetchall()
    for col in row:
        device_name = col["name"]
    if device_name is None:
        return ""
    else:
        return device_name

def getDeviceType(con, id):
    cur = db.query("SELECT `type` FROM Devices WHERE id = %s", id)
    row = cur.fetchall()
    for col in row:
        device_type = col["type"]
    if device_type is None:
        return ""
    else:
        return device_type

def getDeviceFunction(con, id):
    cur = db.query("SELECT `function` FROM Devices WHERE id = %s", id)
    row = cur.fetchall()
    for col in row:
        device_function = col["function"]
    if device_function is None:
        return ""
    else:
        return device_function

def deviceIdCheck(id):
    if re.match(r"[a-zA-Z0-9]{0,128}$", id) is None: # check that id only has letters and numbers
        return False
    else:
        cur =db.query("SELECT * FROM Devices WHERE id = %s", id)
        row = cur.fetchall()
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
        #print (sql_query, id)
        cur = db.query(sql_query, id)
        row = cur.fetchall()
        if row:
            return True
        else:
            return False

def getUserName(con, id):
    cur = db.query("SELECT `name` FROM Users WHERE id = %s", id)
    row = cur.fetchall()
    for col in row:
        device_name = col["name"]
    if device_name is None:
        return ""
    else:
        return device_name

def lookupDeviceAttribute(con, function, attr_name):
    try:
        sql_querry = "SELECT * FROM `Device_Types` WHERE type = %s"
        cur = db.query(sql_querry, function)
        rows = cur.fetchall()
        for row in rows:
            for x in xrange(1, 10):
                col_name = "value%d" % x  # iterate through attribute field looking for the column we need
                if row[col_name] == attr_name:
                    print "col name: %s  row[]: %s  attr name: %s " % (col_name, row[col_name], attr_name)
                    return col_name
            else:
                return None
    except MySQLdb.IntegrityError:
            return None


