__author__ = 'matt'

import bottle
import pymysql
import HomerHelper
import logging


db = HomerHelper.DB()
logger = logging.getLogger(__name__)
WebApp = bottle.Bottle()


@WebApp.route('/')
@bottle.view('index')
def index():
    nav = HomerHelper.buildNav()
    cur = db.query("SELECT * FROM `Users`", None)
    row = cur.fetchall()
    users = []
    for col in row:
        userdata = (col['name'], col['location'])
        users.append(userdata)
    return bottle.template('default', nav, users= users)

@WebApp.route('/static/:path#.+#', name='static')
def static(path):
    return bottle.static_file(path, root='static')

@WebApp.get('/favicon.ico')
def get_favicon():
    return bottle.static_file('favicon.ico', root='./static/')

@WebApp.get('/viewLamp')
def viewBrightness():
    nav = HomerHelper.buildNav()
    cur = db.query("SELECT * FROM `Devices` WHERE function = %s", 'lamp')
    row = cur.fetchall()
    brightness_location = HomerHelper.lookupDeviceAttribute('lamp', 'Brightness')
    html = []  # parser for the information returned
    for col in row:
        devicename = col['name']
        devicename = devicename.replace(" ", "_")
        lampdevices = (col['name'], devicename, str((int(col[brightness_location])*100 )/255),col['id'])
        html.append(lampdevices)
    return bottle.template('brightness', nav, devices=html)

@WebApp.get('/room/<roomname>')
def viewRooms(roomname):
    nav = HomerHelper.buildNav()
    cur = db.query("SELECT * FROM `Device_Types`", None)  # Lookup all the device types to lookup devices in groups
    deviceTypes = cur.fetchall()
    html = {}

    for deviceType in deviceTypes:  # step through device types building dict of device status values
        functiontype = deviceType['type']
        cur = db.query("SELECT * FROM `Devices` WHERE `function` = %s AND `location` = %s",  (functiontype, roomname))
        rows = cur.fetchall()

        d = []
        for row in rows:
            devicename = row['name']
            devicename = devicename.replace(" ", "_")
            devices = (row['name'], devicename, row['function'], row['id'])
            d.append(devices)
        html[functiontype] = d
    print 'html'
    print html

    return bottle.template('rooms', nav, lamps=html['Lamp'])

@WebApp.get('/viewhistory')
def viewHistory():
    nav = HomerHelper.buildNav()
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
        return bottle.template('history', entries=history, webroot=nav['webroot'], rooms=nav['rooms'], functions=nav['functions'])
    except MySQLdb.IntegrityError:
        abort(400, "Doh! Device doesnt exist")

@WebApp.get('/setup/adddevice')
def viewaddDevice():
    nav = HomerHelper.buildNav()
    cur = db.query("SELECT * FROM `Devices` WHERE function = %s", 'lamp')
    row = cur.fetchall()
    brightness_location = HomerHelper.lookupDeviceAttribute(con, 'lamp', 'Brightness')
    html = []  # parser for the information returned
    for col in row:
        devicename = col['name']
        devicename = devicename.replace(" ", "_")
        lampdevices = (col['name'], devicename, str((int(col[brightness_location])*100 )/255),col['id'])
        print "viewbrightness"
        print lampdevices
        html.append(lampdevices)
    return bottle.template('brightness', devices=html, webroot=nav['webroot'], rooms=nav['rooms'], functions=nav['functions'])