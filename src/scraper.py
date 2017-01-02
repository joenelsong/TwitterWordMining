'''
Author: Joey Nelson
Dev Env: Python 2.7.12

Requirments:
> database.py  --> This is used to create and manage the sqlite3 database
> pip install tweepy  --> twitter api wrapper used to mine twitter data

Purpose:
This program mines data from twitter for the vendors/terms identified in the class Listener
Data is stored in an sqlite3 database with the following tables: Vendors, Tweets, Vendors_Tweets
On first launch the program will create a database relative to current working directory
subsequent launches from the same working directory will connect to the existing database
'''

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import time
import re

import database as db
import os


from textblob import TextBlob


#consumer key, consumer secret, access token, access secret.
A_TOKEN ="586260872-Lh8eCmrgTmPTqsGLyBU4z79c3xIHvKf1BmzHfJqf"
A_SECRET ="4ZsungQNjyYulw8jBFYTA44UQm52iuBD1ZBU01uybT2xN"
C_TOKEN = "oXCCQCWYWHXRNUH3PZz469pNI"
C_SECRET = "rb9dPqm1jNEZzk2Mfns4Wh93xRdo51sAdYgLiTRfyL8TycGm9b"

FILTER_LEVEL = "low"

class Listener(StreamListener):
    # Vendors/Terms
    CISCO = ["cisco", "ccna"] # CCNA contains Cisco search term
    AWS =["aws", "amazon web services"]
    MICROSOFT = ["microsoft sharepoint"]
    LINUX = ["linux", "debian", "ubuntu", "red hat enterprise", "opensuse", "centos", "kubuntu"]
    POWERSHELL = ["powershell"]
    ITIL = ["itil", "it infrastructure library", "information technology infrastructure library"]
    SQL =["sql", "structured query language"]
    AZURE = ["azure"]
    CEH = ["ceh", "certified ethical hacker"]
    
    VENDOR_TERMS_LIST = [CISCO,AWS,MICROSOFT,LINUX,POWERSHELL,ITIL,SQL,AZURE,CEH]
    VENDOR_TERMS = CISCO + AWS + MICROSOFT + LINUX + POWERSHELL + ITIL + SQL + AZURE + CEH
        
    def on_data(self, raw_data):
        tweet = json.loads(raw_data)
        add_for_vendors = [] # vendors for which tweet is relevant to
        will_add_to_db = False # Flag to determine if tweet will be added to database
        #print(tweet['user']['id'])
        
        # Invalid Tweet Error Handling 
        if (raw_data == None): # Skip if tweet is None
            print("!Skipping tweet - null object")
            return True
        kz = tweet.keys()
        if ('lang' not in kz or 'id' not in kz or 'text' not in kz or 'user' not in kz or 'timestamp_ms' not in kz): # Skip if tweet is missing attributes of interest
            print("!Skipping tweet - missing attributes")
            return True
            
        # Filter out non-english tweets -- e.g. cisco is a spanish word
        if (tweet['lang'] == "en"):
            for i in range( len(Listener.VENDOR_TERMS_LIST) ): # Iterate through all Vendor's terms
                match = self.vendor_in_tweet(Listener.VENDOR_TERMS_LIST[i], tweet['text'])
                if ( match ):
                    add_for_vendors.append(i+1)
                    will_add_to_db = True
            if (will_add_to_db):
                # Sentiment Analysis
                tweet_tblob = TextBlob(tweet['text'])
                # Add to database
                db.db_add_records( add_for_vendors, tweet['id'], tweet['text'], tweet['user']['id'], db.db_datetime(tweet['timestamp_ms']), tweet_tblob.sentiment.polarity, tweet_tblob.sentiment.subjectivity )

        return True

    def on_error(self, status):
        if status == 420:
            #returning False in on_data disconnects the streamit
            print("Status = 420: connecting too fast or multiple connections")
            return False
        print(status)
        
    def vendor_in_tweet(self, arr, tweet):
        if (tweet != None): # Read this could happen and cause issues, necessity undetermined
            for i in range ( len (arr) ):
                term = arr[i]
                if ( re.search(term, tweet, re.IGNORECASE) ): # use RegEx matching
                    return True # will return on first match
        return False # Return false if no matches
            
if __name__ == "__main__":

    #Create Database
    db.create_db()

    # Setup Twitter Mining Stream
    auth = OAuthHandler(C_TOKEN, C_SECRET)
    auth.set_access_token(A_TOKEN, A_SECRET)

    l = Stream(auth, Listener())
    l.filter(track=Listener.VENDOR_TERMS, stall_warnings=True, filter_level = FILTER_LEVEL) 
    
    # Close Database, code will never reach this without error
    db.db_close()