import json
import heapq
from datetime import datetime, timedelta
from sqlalchemy import or_, and_, Time, DateTime, Date, cast
from models import Tweet
from utils import color_code_text
from graph import get_graph

def related_tweets(source, dest, since_date=None, before_date=None):
    '''Returns all related tweets for `via`.'''
    graph = get_graph()
    if not graph.has_edge(source, dest):
        return
    keywords = graph[source][dest]['keywords']
    print keywords
    filters = or_(*[Tweet.text.ilike('%%%s%%' % x) for x in keywords])
    qs = Tweet.query.filter(filters)
    if since_date is not None:
        qs = qs.filter(cast(Tweet.created_at, Date) >= since_date)

    if before_date is not None:
        qs = qs.filter(cast(Tweet.created_at, Date) <= before_date)

    return qs

def related_tweets_window(source, dest, window=15, now=None):
    '''Returns a window of tweets for `via`.'''
    if now is None:
        now = datetime.now()
    window_ago = now - timedelta(minutes=window)
    return related_tweets(source, dest).filter(Tweet.created_at >= window_ago)

def related_tweets_time(source, dest, start, end, since_date=None, before_date=None):
    '''Returns all tweets that have appened around [start, end] hours for
    `via`.'''
    qs = related_tweets(source, dest, since_date=since_date,
                        before_date=before_date)
    qs = qs.filter(cast(Tweet.created_at, Time) >= start)
    qs = qs.filter(cast(Tweet.created_at, Time) <= end)
    return qs

# def partition_historical(via, window=30, since_date=None):
#     relevant = get_relevant()
#     traffic = get_traffic()

#     # window debe dividir a 60 minutos (1 hora)
#     scores = defaultdict(lambda: [0, 0, 0])
#     for hour in range(24):
#         for minutes in range(0, 60, window):
#             start = '%02d:%02d:00' % (hour, minutes)
#             end = '%02d:%02d:59' % (hour, (minutes + window - 1) % 60)
#             print start, end
#             for tweet in relevant_tweets_time(via, start, end, since_date):
#                 if relevant.predict1(tweet.text) == 1:
#                     predicted_score = traffic.predict1(tweet.text)
#                     # color_code_text(tweet.text.encode('utf-8'), predicted_score)
#                     scores[(start, end)][predicted_score] += 1
#     return scores
