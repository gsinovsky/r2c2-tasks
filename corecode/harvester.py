# -*- coding: utf-8 -*-
from models import User, Tweet
from db import session
from twitterAPI import TwitterAPIFactory

def get_timeline():
    TWITTER_API_KEY = '823HTWjuQJ9cL4uSX2ffR2sF5'
    TWITTER_API_SECRET = 'PtKYljMNHjlTcKtf4j5WfLb6MJSDDh6VyTM1lMPKxfFhLoRgj7'
    TWITTER_ACCESS_TOKEN = '2984322627-lSHzM70os2QNwucyKbQ3gqMZpSsPuo68wfdyb14'
    TWITTER_ACCESS_TOKEN_SECRET = 'DC9sh5d1r7bD0WLnc2Pd0dRd167FucH6ZoDUUZcKlogqi'

    twitterAPIfactory = TwitterAPIFactory(consumer_key=TWITTER_API_KEY,
                                            consumer_secret=TWITTER_API_SECRET,
                                            access_token_key=TWITTER_ACCESS_TOKEN,
                                            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET)
    api = twitterAPIfactory.getAPI()

    last_tweet_recorded = Tweet.query.order_by(Tweet.created_at.desc()).first()
    kw = {}
    if last_tweet_recorded:
        tweet_id = int(last_tweet_recorded.tweet_id)
        kw['since_id'] = tweet_id
    results = api.GetHomeTimeline(count=150, **kw)
    for tweet in results:
        Tweet.create(tweet)

if __name__ == '__main__':
    get_timeline()

