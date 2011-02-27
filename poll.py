#imports ****
from types import *
import os
import datetime
import MySQLdb as mdb
import sys
from twython import Twython
from dateutil import zoneinfo 
import pytz
#*************

twitter = Twython()

tweetusers = []
tweetmemories = []
tweettimes = []
tweetids = []

query_str = 'YOUR QUERY STRING'


yesterday = datetime.datetime.now() - datetime.timedelta(1)
yesterday = str(yesterday)
yesterday = yesterday[:10]


utc = pytz.utc
est = pytz.timezone("EST")
		
def sql_run():
	try:
		conn = mdb.connect(host='LOCALHOST', db='MYSQLDB', user='MYSQL USER', passwd='MYSQL PASSWORD')
		conn.set_character_set('utf8')
		cursor = conn.cursor()
		cursor.execute('SET NAMES utf8;')
		cursor.execute('SET CHARACTER SET utf8;')
		cursor.execute('SET character_set_connection=utf8;')
		for i in reversed(range(len(tweetusers))):
                        fin_mem = os.popen('php PATH/tweetfilter.php "' + tweetmemories[i]  + '"').read() #tweetfilter.php is a swear filter, not included in this repo
			fin_mem = fin_mem[1:]
			#fin_mem = tweetmemories[i]
			badwordrep = 'ilovetouchtunnel' #our bad word replacment string
			if badwordrep not in fin_mem:
				sql = ("""INSERT INTO MYSQLTABLE(postinfo,formortweet,new,name,memory,tweetid) VALUES("%s","%s",%d,"%s","%s","%s")""" % (tweettimes[i],"tweet",1,tweetusers[i],fin_mem,tweetids[i]))
				cursor.execute(sql)
			else:
				sql = ("""INSERT INTO MYSQLTABLE(postinfo,formortweet,new,name,memory,tweetid) VALUES("%s","%s",%d,"%s","%s","%s")""" % (tweettimes[i],"tweet",-1,tweetusers[i],fin_mem,tweetids[i]))
				cursor.execute(sql)
		conn.commit()
		cursor.close()
		conn.close()
	except mdb.Error as e:
		print ("Error %d: %s" % (e.args[0],e.args[1]))
		sys.exit(1)

def searchFeed(last_id):	
	tweettimes_weird = []
	s_memories = twitter.searchTwitter(q='YOUR QUERY HERE', rpp='15',since=yesterday,since_id=last_id)
	#print s_memories['results']
	if 'error' in s_memories:
		pass

	else:
		for tweet in s_memories['results']:
			tweetright = ""
			for word in tweet['text'].split():
				checkword = word.lower()
				if (checkword == query_str) or (checkword=='#ttmemory'):
					continue
				else:
				    tweetright += (word + ' ')
				
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
