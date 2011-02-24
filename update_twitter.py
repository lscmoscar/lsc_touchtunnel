#!/usr/bin/python
#*****Imports***********
import os
import tweepy
from BeautifulSoup import BeautifulStoneSoup as BSS
import sys
import time
import urllib2
import urllib
import json
import re
from StringIO import StringIO
#************************
tweet_max = 140
#************

tt_hash = 'YOUR HASH RETURN'
site = 'http://touchtunnel.org' #our touchtunnel weblink
tt_account = 'TWITTER ACCOUNT NAME' #witter account name
bad_replace = 'ilovetouchtunnel' #our bad word replacment string

GOOGLE_API_KEY = "YOUR GOOGLE API KEY"
USERNAME = "GOOGLE CLIENT USER NAME" 
PASSWORD = "GOOGLE CLIENT PASSWORD"

#Authentication Needs-->ACCESS_KEY and ACCESS_SECRET generated from python_oauth_test.py and Twitter UserName Acceptance
CONSUMER_KEY = 'TWITTER APP KEY'
CONSUMER_SECRET = 'TWITTER APPSECRET KEY'
ACCESS_KEY = 'OAUTH ACCESS KEY FOR TWITTER ACCOUNT USING APP --> FROM python_oauth_test.py'
ACCESS_SECRET = 'OAUTH ACCESS SECRET KEY FOR TWITTER ACCOUNT --> FROM python_oauth_test.py'
#We created our own account for the project (so, the only oauth handshake occurs with Liberty Science Center official memories account --> @touchtunnelmems
#*****************************

#*****XML Work and String Concatenation****************

xml_file = open('PATH/output_new.xml').read()
xml_soup = BSS(xml_file);
print xml_soup.prettify() 

#Google ClientLogin --> to use urlShorten and retrieve unique API, code snippet attributed to Josh B. 
#http://www.excession.org.uk/blog/using-googles-url-shortener-api-from-python.html
def getTokenFromGoogle (username, password):
    url = "https://www.google.com/accounts/ClientLogin"
    params = {
            "accountType" : 'GOOGLE',
            "Email" : username,
            'Passwd' : password,
            'service' : 'urlshortener',
            'source' : 'ExcessiveDevelopment-UrlShortner-vs1'
            } 
    data = urllib.urlencode(params)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    dataFromGoogle = response.read()
    authTokenRe = re.compile(r"Auth=(.+?)$")
    match = authTokenRe.search (dataFromGoogle)
    if(match):
        return match.group (1)   
    raise Exception, "could not authToken for user : %s" % username

def shorternUrlWithAuthToken (authToken, urlShortern):
	values = json.dumps({'longUrl' : urlShortern})
	requestUrl = "https://www.googleapis.com/urlshortener/v1/url?key=" + GOOGLE_API_KEY
	googleAuthTokenHeader = "GoogleLogin auth=" + authToken
	#print googleAuthTokenHeader
	headers = {'Content-Type' : 'application/json','Authorization' : googleAuthTokenHeader}
	req = urllib2.Request (requestUrl, values, headers)
	response = urllib2.urlopen (req)
	the_page = response.read()
	io = StringIO(the_page)
	jsonReturned = json.load(io)
	return jsonReturned ["id"]

authToken = getTokenFromGoogle (USERNAME, PASSWORD)
#print "authToken : %s" % (authToken)
url = shorternUrlWithAuthToken (authToken, site)
#********************************************************
def encode(text):
    text = text.replace("&amp;", "&")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&apos;", "'")
    text = text.replace("&quot;", '"')
    return text

#make sure the entire string doesn't go over 140 chars (Twitter's max)
def memcheck(thestring,memory):
	nomem_count = len(thestring) - len(memory)
	tweet_count = tweet_max - nomem_count
	
	if len(thestring) > tweet_max:
                fulltweet = memory
		memory = memory[:((tweet_count) - 3)]
		memory = memory + '...'
                next_mem = fulltweet[((tweet_count)-3):((tweet_count)-3)+tweet_max]
		return memory,next_mem
	else:
                next_mem = None #used to separate longer memories into 2 separate posts
		return memory,next_mem

#***********Authorization of Twitter OAuth and Tweepy Init**************
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
#*********************************

#if it's a tweet, recognize the user with a @ symbol
entries = xml_soup.findAll('entry')
for entry_tag in entries:
	name = entry_tag['name']  
	memory = entry_tag['memory']
	formortweet = entry_tag['formortweet']
	yearofvisit = entry_tag['yearofvisit']

        name = encode(name)
        memory = encode(memory)

	if formortweet == 'tweet':
		name = '@' + name
		printit = tt_hash + ' by ' + name + ':' + memory + ',' + url
		memory,next_mem = memcheck(printit,memory)
                name = name.rstrip()
                memory = memory.rstrip()
                final_tweet = tt_hash + ' by ' + name + ':' + memory + ',' + url
        	if (not api.exists_friendship(tt_account, name)) and memory.find(bad_replace) == -1:
        		api.create_friendship(name)
        	elif api.exists_friendship(tt_account, name) and memory.find(bad_replace) != -1:
        		api.destroy_friendship(name)
                                    
	else:
		printit = tt_hash + ' by ' + name + ':' + memory + '(' + yearofvisit + ')' + ',' + url
		memory,next_mem = memcheck(printit,memory)
                name = name.rstrip()
                memory = memory.rstrip()
		final_tweet = tt_hash + ' by ' + name + ':' + memory + '(' + yearofvisit + ')' + ',' + url
#*****Update Status Code******
	api.update_status(status=final_tweet,lat=40.707980,long=-74.055719)
        if (next_mem is not None):
            api.update_status(status=next_mem,lat=40.707980,long=-74.055719) 
        time.sleep(30)
#*****************************