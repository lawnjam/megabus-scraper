#!/usr/bin/env python
# -*- coding: utf-8 -*-
# currently takes 10 minutes to run
# scrape megatrain routes. outputs csv. 
# john@lawnjam.com

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

megaSoup = BeautifulSoup(response.read())
viewstate = megaSoup.find(name='input', attrs={'name': '__VIEWSTATE'})['value']
eventvalidation = megaSoup.find(name='input', attrs={'name': '__EVENTVALIDATION'})['value']
options = megaSoup.find(name='select', attrs={'name': 'SearchAndBuy1$ddlLeavingFrom'}).findAll('option')
startLocations = {}
for o in options:
    startLocations[int(o['value'])] = o.find(text=True)
del startLocations[0] # 0 is "Select"

# set other form values
values = {
    'Welcome1_ScriptManager1_HiddenField': '',
    'Welcome1$ScriptManager1': 'SearchAndBuy1$upSearchAndBuy|SearchAndBuy1$ddlLeavingFrom',
    '__EVENTTARGET': 'SearchAndBuy1$ddlLeavingFrom',
    '__EVENTARGUMENT': '',
    'Welcome1$hdnBasketItemCount': '0',
    'Language1$ddlLanguage': 'en',
    'SearchAndBuy1$txtPassengers': '1',
    'SearchAndBuy1$txtConcessions': '0',
    'SearchAndBuy1$txtNUSExtra': '0',
    'SearchAndBuy1$txtOutboundDate': '',
    'SearchAndBuy1$txtReturnDate': '',
    'SearchAndBuy1$txtPromotionalCode': '',
    '__ASYNCPOST': 'true'
    }
headers['X-MicrosoftAjax'] = 'Delta=true'

for startId, startLocation in startLocations.items():
    values['SearchAndBuy1$ddlLeavingFrom'] = startId
    values['__EVENTVALIDATION'] = eventvalidation
    values['__VIEWSTATE'] = viewstate
    data = urllib.urlencode(values)
    req = urllib2.Request('http://uk.megabus.com/default.aspx', data, headers)

    # store the received (pipe-separated) data in a list
    L = urllib2.urlopen(req).read().split('|')
    for position, item in enumerate(L):
        if item == 'SearchAndBuy1_upSearchAndBuy':
            html = L[position + 1]
        if item == '__VIEWSTATE':
            viewstate = L[position + 1] # save __VIEWSTATE for the next iteration
        if item == '__EVENTVALIDATION':
            eventvalidation = L[position + 1] # save __EVENTVALIDATION for the next iteration

    megaSoup = BeautifulSoup(html)
    options = megaSoup.find(name='select', attrs={'name': 'SearchAndBuy1$ddlTravellingTo'}).findAll('option')
    endLocations = {}
    for o in options:
        if int(o['value']) > 0:
            # 2nd POST: set travelling to
            values['__EVENTVALIDATION'] = eventvalidation
            values['__VIEWSTATE'] = viewstate
            values['Welcome1$ScriptManager1'] = 'SearchAndBuy1$upSearchAndBuy|SearchAndBuy1$ddlTravellingTo'
            values['__EVENTTARGET'] = 'SearchAndBuy1$ddlTravellingTo'
            values['__LASTFOCUS'] = ''
            values['SearchAndBuy1$ddlTravellingTo'] = o['value']
            data = urllib.urlencode(values)
            req = urllib2.Request('http://uk.megabus.com/default.aspx', data, headers)

            # store the received (pipe-separated) data in a list
            L = urllib2.urlopen(req).read().split('|')
            for position, item in enumerate(L):
                if item == 'SearchAndBuy1_upSearchAndBuy':
                    html = L[position + 1]
                if item == '__VIEWSTATE':
                    viewstate = L[position + 1]
                if item == '__EVENTVALIDATION':
                    eventvalidation = L[position + 1]
            megaSoup = BeautifulSoup(html)
            byOptions = megaSoup.find(name='select', attrs={'name': 'SearchAndBuy1$ddlTravellingBy'}).findAll('option')
            for by in byOptions:
                if by['value'] == '2': # 1: bus, 2: train
                    print '"' + startLocation + '","' + o.find(text=True) + '"'
