import tweepy
#THIS CODE GIVES YOU ACCESS KEY AND ACCESS SECRET KEY FOR OUATH AUTHENTICATION

CONSUMER_KEY = 'TWITTER APP KEY'
CONSUMER_SECRET = 'TWITTER APP SECRET KEY'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth_url = auth.get_authorization_url()
print 'Please authorize: ' + auth_url
verifier = raw_input('PIN: ').strip()
auth.get_access_token(verifier)
print "ACCESS_KEY = '%s'" % auth.access_token.key
print "ACCESS_SECRET = '%s'" % auth.access_token.secret