import os
import MySQLdb as mdb
import sys

#CODE TO GET LAST TWEET ID IN THE DATABASE, FOR POLLING OF TWEETS WITH SET HASHTAG

def get_id():
	try:
		conn = mdb.connect(host='LOCALHOST', db='MYSQLDB', user='MYSQL USER', passwd='MYSQL PASSWORD')
		cursor = conn.cursor()
		col = "tweet"
		sql = ("""SELECT tweetid FROM MYSQLTABLE WHERE formortweet="%s" ORDER BY tweetid""" % (col))
		cursor.execute(sql)
		conn.commit()
		fetchlist = []
		for each_id in cursor.fetchall():
			fetchlist.append(each_id)
		cursor.close()
		conn.close()
		if len(fetchlist) > 0:
			fetch = str(fetchlist[-1]).replace(',','')
			return fetch[2:-2]
			
		else:
			return 0
		
	except mdb.Error as e:
		print ("Error %d: %s" % (e.args[0],e.args[1]))
		sys.exit(1)
		
last_id = get_id();
print last_id