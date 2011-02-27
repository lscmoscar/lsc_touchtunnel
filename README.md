# Scripts for Liberty Science Center's Touch Tunnel Twitter App/Memories Project

# What is this repo?
This repository includes four python scripts:
 python_oauth.py uses the [tweepy](https://github.com/joshthecoder/tweepy) module and is set to authenticate with a specific account (for LSC, we used [@TouchTunnelmems](http://twitter.com/touchtunnelmems))

- poll.py and poll_top.py are used to for Twitter *hashtag* seraches. Once tweets with that *hashtag* is found, it is then placed into a mysql database. The [twython](https://github.com/ryanmcgrath/twython) module is used
`twitter.searchTwitter(q='YOUR QUERY HERE', rpp='15',since=yesterday,since_id=last_id)`

- update_twitter.py uses the tweepy module and oauth credentials to update the status of our designated Twitter profile
`api.update_status(status=final_tweet,lat=40.707980,long=-74.055719)
    if (next_mem is not None):
        api.update_status(status=next_mem,lat=40.707980,long=-74.055719) 
    time.sleep(30)`