#!/usr/bin/python
# -*- coding: ascii -*-

import tweepy
import csv
import sys
import time

ofile = open('updated_loc.csv', 'a+b')
writer = csv.writer(ofile)

access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

seeds = ['bully', 'bullied', 'bullying', 'retard', '#flame', '#flames', '#flaming', '#flamings', '#bully', '#bullying',
         '#retard', '#bullied', 'whore', 'loser', 'freak']

class MyStreamListener(tweepy.StreamListener):
    count=0
    def on_status(self, status):
        if status.place is not None and status.lang.lower() == 'en':
            writer.writerow([status.created_at, status.coordinates, status.text.encode('utf-8'), status.source,status.favorite_count, status.retweet_count, status.place, status.lang])
            print status.id_str, 'tweet added to the .csv file'
            testList.append(status.id_str)
            print "tweet count is",len(testList)
            if len(testList)==50000:
                sys.exit(0)

    def on_error(self, status_code):
        print status_code

testList=[]
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
while(True):
    try:
        myStream.filter(track=seeds).filter(locations=[-125, 25, -65, 48]).filter(languages=['en'])
    except:
        print 'Skipping the tweet'
        print 'time out for 5.0 seconds'
        time.sleep(5)
        if len(testList)==50000:
            break

print("write completed")
ofile.close()
