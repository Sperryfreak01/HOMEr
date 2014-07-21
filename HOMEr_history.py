__author__ = 'matt'

import datetime
import MySQLdb

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

def device_exsists(con, id):
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

def getdevicename(con, id):
    cur = con.cursor(MySQLdb.cursors.DictCursor)  # open connection to DB
    with con:
        print(id)
        cur.execute("SELECT `name` FROM Devices WHERE id = %s", id)

    row = cur.fetchall()
    for col in row:
        device_name = col["name"]
        print device_name
    if device_name is None:
        return ('')
    else:
        return (device_name)