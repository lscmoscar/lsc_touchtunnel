#imports ****
from types import *
import os
import datetime
import MySQLdb as mdb
import sys
from twython import Twython
from dateutil import zoneinfo 
import pytz

#from datetime import date, timedelta
#*************

twitter = Twython()

tweetusers = []
tweetmemories = []
tweettimes = []
tweetids = []

#default set
#hash_ = "%23"
#hash_='#'

#once received hashtag for tt
#query = 'touchtunnelmems'
query_str = 'HASH THAT PEOPLE TWEET IN ORDER TO GET POLLED/SEARCHED'


yesterday = datetime.datetime.now() - datetime.timedelta(1)
#today = datetime.datetime.now()
#today = str(today)
#today = today[:10]
yesterday = str(yesterday)
yesterday = yesterday[:10]
#print yesterday


utc = pytz.utc
est = pytz.timezone("EST")
		
def sql_run():
	try:
                conn = mdb.connect(host='LOCALHOST', db='MySQLDB', user='MySQL USER', passwd='MySQL USER PASSWORD')
		conn.set_character_set('utf8')
		cursor = conn.cursor()
		cursor.execute('SET NAMES utf8;')
		cursor.execute('SET CHARACTER SET utf8;')
		cursor.execute('SET character_set_connection=utf8;')
		for i in reversed(range(len(tweetusers))):
			fin_mem = os.popen("php tweetfilter.php '" + tweetmemories[i]  + "'").read() #file not included, but is just a badword filter php file/api call
			fin_mem = fin_mem[1:]
			badwordrep = 'ilovetouchtunnel' #BAD WORD REPLACEMENT STRING
			if badwordrep not in fin_mem:
				sql = ("""INSERT INTO MySQLDB(postinfo,formortweet,new,name,memory,tweetid) VALUES("%s","%s",%d,"%s","%s","%s")""" % (tweettimes[i],"tweet",1,tweetusers[i],fin_mem,tweetids[i]))
				cursor.execute(sql)
			else:
				sql = ("""INSERT INTO MySQLDB(postinfo,formortweet,new,name,memory,tweetid) VALUES("%s","%s",%d,"%s","%s","%s")""" % (tweettimes[i],"tweet",-1,tweetusers[i],fin_mem,tweetids[i]))
				cursor.execute(sql)
		conn.commit()
		cursor.close()
		conn.close()
	except mdb.Error as e:
		print ("Error %d: %s" % (e.args[0],e.args[1]))
		sys.exit(1)

def searchFeed(last_id):	
	tweettimes_weird = []
	s_memories = twitter.searchTwitter(q='SEARCH QUERY HERE', rpp='5',since=yesterday,since_id=last_id)
	#print s_memories['results']
	if 'error' in s_memories:
		pass
		
	# for tweet in s_memories['results']:
	# 	print tweet['text'] + ": " + tweet['from_user']
	else:
		for tweet in s_memories['results']:
			#print tweet['text']
			#print tweet
			tweetright = ""
			for word in tweet['text'].split():
				word = word.lower()
				if (word == query_str):
					continue
				else:
					tweetright += (word + ' ')
			#memstring = tweetright + ': ' + tweet['from_user']
			#memstring = memstring.lower()
			# if (memstring not in memories):
			tweetmemories.append(tweetright)	
			tweetusers.append(tweet['from_user'])
			tweettimes_weird.append(tweet['created_at'])
			tweetids.append(tweet['id'])
			for time in tweettimes_weird:
				long_time = time[5:-6]
				ctime_utc = datetime.datetime.strptime(long_time,'%d %b %Y %H:%M:%S')
				ctime_utc = ctime_utc.replace(tzinfo=utc)
				ctime = ctime_utc.astimezone(est)
				ctime = ctime.strftime("%Y-%m-%d %H:%M:%S")
				tweettimes.append(ctime)
	
		if len(tweetmemories) > 0:	
			sql_run()
			print(1)
		
		else:
			print(0)
			pass


def main(argv):
	if (len(argv) > 0):
		for a in argv:
			last_id = a
		searchFeed(last_id)
	else:
		pass
	

if __name__ == "__main__":
	main(sys.argv[1:])
