# -*- coding: utf-8 -*-
from twitterAPI import TwitterAPIFactory
from models import User, Tweet
from db import session
import json

"""
    PRECONDITINO: jsonfile contains a list of tweets as dictionaries
    @procedure tweet_from_json_to_db :  Given a json file containing a list of dictionaries, 
                                        constructs a tweet model object from dictionaries and 
                                        store its content into the database related to the model
"""
def tweet_from_json_to_db(jsonfilename):
    parsedTweets = parseJSON(jsonfilename=jsonfilename)
    for parsedTweet in parsedTweets:
        tweet = Tweet.from_dictionary(parsedTweet)
        print "Parsed Tweet: %s" %(tweet)
        print "Storing Tweet into DB..."
        tweet.submit() # SAVES INTO DATABASE


def tweet_from_jso_to_DB_test():
    """TODO
    #open json file
    #parse json files using json library
    #use dictionaries to store Tweet models (Tweet from dictionary already implemented)

    """

    twitterAPIfactory = TwitterAPIFactory()
    api = twitterAPIfactory.getAPI()

    last_tweet_recorded = Tweet.query.first()
    print last_tweet_recorded
    kw = {}
    if last_tweet_recorded:
        tweet_id = int(last_tweet_recorded.tweet_id)
        kw['since_id'] = tweet_id
    results = api.GetHomeTimeline(count=10, **kw)
    tweets = results
    #tweets[0].id = 9598979 reference in DB 

    jsonfilename='tweet.json'

    tweetsJsonContent = [tweet.AsDict() for tweet in tweets]

    saveAsJSON(JSONSerializableObject=tweetsJsonContent,jsonfilename=jsonfilename,indent=4)
    parsedTweets = parseJSON(jsonfilename=jsonfilename)
    for parsedTweet in parsedTweets:
        my_tweet = Tweet.from_dictionary(parsedTweet)
        print "Parsed Tweet: %s" %(my_tweet)
        #my_tweet.submit() # SAVES INTO DATABASE
"""
    PRECONDITION: JSONserializableObject is json serializable
"""
def saveAsJSON(JSONSerializableObject,jsonfilename,indent=0):
    #appends json content in the specified file 
    with open(jsonfilename,'a') as jsonfile:
        json.dump(JSONSerializableObject,jsonfile,indent=indent)

def parseJSON(jsonfilename):
    with open(jsonfilename,'r+') as jsonfile:
        return json.load(jsonfile)

if __name__ == '__main__':
    jsonToDBTest()

