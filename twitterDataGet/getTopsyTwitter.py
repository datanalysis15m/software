__author__ = '@oscarmarinmiro'

# -*- coding: utf-8 -*-

import time
import sys
import codecs
import re
import traceback
import urllib
import urllib2
import json
import csv
import pprint
import datetime

# This example script shows how to query topsy for results in a given date interval
# Output is written to json files, one per day
# In order to not abuse topsy server, a delay is introduced between pages and between days. PLEASE USE THEM!!
# For more info visit https://code.google.com/p/otterapi/
# To get an API KEY (needed), visit: http://manage.topsy.com

TIME_TWEEN_PAGES = 20
TIME_TWEEN_DAYS = 30
API_KEY = "<INSERT_YOUR_API_KEY_HERE from http://manage.topsy.com>"

# Talk with topsy server to get 'query' results from 'initTime' to 'endTime'
# If you want other media than tweets you can change the 'type' parameter according to https://code.google.com/p/otterapi/ docs

def getTopsyTwitter(query,initTime,endTime):

	tweetData = []

	for i in range(0,10):

		dataDict = {}

		dataDict['q'] = query.encode("utf-8")
		dataDict['mintime'] = initTime
		dataDict['maxtime'] = endTime
		dataDict['page'] = i+1
		dataDict['perpage'] = 100
		dataDict['type'] = 'tweet'
		dataDict['apikey'] = API_KEY
		
		url_values = urllib.urlencode(dataDict)

		full_url = 'http://otter.topsy.com/search.json'+"?"+url_values

		print "Full url is %s" % (full_url)

		req = urllib2.Request(full_url)

		response = urllib2.urlopen(req)

		the_page = response.read()

		# print JSON object

		data = json.loads(the_page)

		for entry in data['response']['list']:
			tweetData.append(entry)

		print "Answer is: %d" % len(data['response']['list'])

		# If last page

		if len(data['response']['list'])<80:
			break

		time.sleep(TIME_TWEEN_PAGES)

	return(tweetData)


def main():

	# Example query

	query = "#15m OR #15mayo"

	# init date 

	initDate = datetime.datetime(2011,05,01)

	initTime = int(time.mktime(initDate.timetuple()))

	# Query for 100 days

	for i in range(0,100):

		date = datetime.datetime.fromtimestamp(initTime)

		dateString = date.strftime("%Y%m%d%H%M%S")

		print(dateString)

		data = getTopsyTwitter(query,initTime,initTime+86400)

		print "Number of registers: %d" % (len(data))

		pprint.pprint(data)

		# Write to json and add a day to initTime

		fOut = open("data."+str(dateString)+".json","wb")

		json.dump(data,fOut,indent=4)

		fOut.close()

		initTime+=86400

		time.sleep(TIME_TWEEN_DAYS)


if (__name__=="__main__"):
	main()
