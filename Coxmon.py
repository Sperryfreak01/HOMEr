__author__ = 'matt'


import urllib2
from bs4 import BeautifulSoup
from requests import session
import sys
import codecs
import time
from datetime import date
import Notifications
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

app_token = 'apCenpnQGuLrVmL2tsTYfyZhiokBGZ'
user_token = 'upTA78BinTDeivWZxLQnorhCijPnHE'
limit = ''
usage = ''
remain = ''
d0 = date.today()
delta = ''

payload = {
    'onsuccess'   : 'myaccount.cox.net/internettools/datausage/usage.cox',
    'onfailure'   : 'ww2.cox.com/resaccount/sign-in.cox',
    'targetFN'    : 'COX.net',
    'emaildomain' : '@cox.net',
    'username'    : 'Sperryfreak01',
    'password'    : 'Matthdl13',
    'rememberme'  : 'true'
}

with session() as web:
    web.post('https://idm.east.cox.net/idm/coxnetlogin', data=payload)
    request = web.get('https://myaccount.cox.net/internettools/datausage/usage.cox')
#    print request.headers
#    print request.text

    soup = BeautifulSoup(request.text, 'html5lib')

#    for table in soup.findAll('tbody'):
#        for rows in table.findAll('tr'):
    x = 0
    for cols in soup.findAll('td'):
        for cell in cols:
            if "GB" in cell:
                x = x + 1

                if x == 1:
                   limit = cell.strip()
                   #print ('Monthly limit is ' + limit)
                elif x == 2:
                   usage = cell.strip()
                   #print ('Current usage is ' +usage)
                elif x == 3:
                    remain = cell.strip()
                    #print ('Remaining bandwidth is ' + remain)

    d1 = d0.replace(month = d0.month + 1, day = 04)
   #print (d1)
    delta = d1 - d0
    #print delta.days
    Notifications.pushover(message=usage +' of the ' + limit + ' month limit has been used. ' + remain + ' remains for the next ' + str(delta.days) + ' days', token = app_token, user = user_token)




