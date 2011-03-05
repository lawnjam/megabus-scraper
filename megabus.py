#!/usr/bin/env python
# -*- coding: utf-8 -*-
# megabus scraper
# 2011-03-05 john@lawnjam.com

from BeautifulSoup import BeautifulSoup
import urllib, urllib2, cookielib

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-gb,en;q=0.8,en-us;q=0.5,gd;q=0.3',
    'Accept-Encoding': 'gzip,deflate',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'}

req = urllib2.Request('http://uk.megabus.com/default.aspx', None, headers)
response = urllib2.urlopen(req)
#print response.read()

megaSoup = BeautifulSoup(response.read())
viewstate = megaSoup.find(name='input', attrs={'name': '__VIEWSTATE'})
eventvalidation = megaSoup.find(name='input', attrs={'name': '__EVENTVALIDATION'})
#print viewstate['value']
#print eventvalidation['value']

# 1st POST: set leaving from
values = {
    'Welcome1_ScriptManager1_HiddenField': '',
    'Welcome1$ScriptManager1': 'SearchAndBuy1$upSearchAndBuy|SearchAndBuy1$ddlLeavingFrom',
    '__EVENTTARGET': 'SearchAndBuy1$ddlLeavingFrom',
    '__EVENTARGUMENT': '',
    '__EVENTVALIDATION': eventvalidation['value'],
    '__VIEWSTATE': viewstate['value'],
    'Welcome1$hdnBasketItemCount': '0',
    'Language1$ddlLanguage': 'en',
    'SearchAndBuy1$txtPassengers': '1',
    'SearchAndBuy1$txtConcessions': '0',
    'SearchAndBuy1$txtNUSExtra': '0',
    'SearchAndBuy1$ddlLeavingFrom': '1', #1 is Aberdeen
    'SearchAndBuy1$txtOutboundDate': '',
    'SearchAndBuy1$txtReturnDate': '',
    'SearchAndBuy1$txtPromotionalCode': '',
    '__ASYNCPOST': 'true'
    }
data = urllib.urlencode(values)
headers['X-MicrosoftAjax'] = 'Delta=true'
req = urllib2.Request('http://uk.megabus.com/default.aspx', data, headers)

# store the received (pipe-separated) data in a list
L = urllib2.urlopen(req).read().split('|')

for position, item in enumerate(L):
    if item == '__VIEWSTATE':
        viewstate = L[position + 1]
    if item == '__EVENTVALIDATION':
        eventvalidation = L[position + 1]


# 2nd POST: set travelling to
values['__EVENTVALIDATION'] = eventvalidation
values['__VIEWSTATE'] = viewstate
values['Welcome1$ScriptManager1'] = 'SearchAndBuy1$upSearchAndBuy|SearchAndBuy1$ddlTravellingTo'
values['__EVENTTARGET'] = 'SearchAndBuy1$ddlTravellingTo'
values['__LASTFOCUS'] = ''
values['SearchAndBuy1$ddlTravellingTo'] = '10' # 10 is Birmingham
data = urllib.urlencode(values)

req = urllib2.Request('http://uk.megabus.com/default.aspx', data, headers)

# store the received (pipe-separated) data in a list
L = urllib2.urlopen(req).read().split('|')

for position, item in enumerate(L):
    if item == '__VIEWSTATE':
        viewstate = L[position + 1]
    if item == '__EVENTVALIDATION':
        eventvalidation = L[position + 1]

# 3rd POST: set date
values['__EVENTVALIDATION'] = eventvalidation
values['__VIEWSTATE'] = viewstate
values['Welcome1$ScriptManager1'] = 'SearchAndBuy1$upSearchAndBuy|SearchAndBuy1$calendarOutboundDate'
values['__EVENTTARGET'] = 'SearchAndBuy1$calendarOutboundDate'
values['__EVENTARGUMENT'] = '4087' ###### FIXME map these values to actual dates - 4087 is 11/03/2011
values['SearchAndBuy1$ddlTravellingBy'] = '0'

data = urllib.urlencode(values)

req = urllib2.Request('http://uk.megabus.com/default.aspx', data, headers)
urllib2.urlopen(req)


# GET the results
req = urllib2.Request('http://uk.megabus.com/JourneyResults.aspx', None, headers)

print urllib2.urlopen(req).read()

