# -*- coding: utf-8 -*-
from twitterAPI import TwitterAPIFactory
from models import User, Tweet
from db import session

def get_timeline():
    """TODO
    #open json file
    #parse json files using json library
    #use dictionaries to store Tweet models (Tweet from dictionary already implemented)

    """


    TWITTER_API_KEY = 'rOYPSNueekDLveKkpIgdU7HpH'
    TWITTER_API_SECRET = 'LJyqgkeY8CeVd78fc2SsaUGFlVHRLSEiftTmBPxChIwQLsfhw9'
    TWITTER_ACCESS_TOKEN = '4165949542-AGCBrmIYkiw7JiKeDeI0trMwbALFzwgHUo9GI5r'
    TWITTER_ACCESS_TOKEN_SECRET = 'evnTf5U53VBpkLqpdaUTuFYY89ZwsSBasTMa0u0oclIuB'

    twitterAPIfactory = TwitterAPIFactory(consumer_key=TWITTER_API_KEY,
                                            consumer_secret=TWITTER_API_SECRET,
                                            access_token_key=TWITTER_ACCESS_TOKEN,
                                            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET)
    api = twitterAPIfactory.getAPI()

    last_tweet_recorded = Tweet.query.first()
    print last_tweet_recorded
    kw = {}
    if last_tweet_recorded:
        tweet_id = int(last_tweet_recorded.tweet_id)
        kw['since_id'] = tweet_id
    results = api.GetHomeTimeline(count=150, **kw)
    for tweet in results:
        print Tweet.from_dictionary(tweet.AsDict())

if __name__ == '__main__':
    get_timeline()

