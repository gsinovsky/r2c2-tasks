"""Utils for data generation"""

import random
import csv
from .models import Tweet
from .traffic import get_traffic, get_relevant
from .retriever import partition_historical
from .utils import load_file, load_tweets, write_file

def generate_file(filename, old_filename='new-tweets.csv', count=2000):
    """Creates a file with tweets with no overlapping with
    `old_filename`. Useful for generating data for human labeling.

    It saves each selected file as a row with:
    tweet text, relevant score, traffic score.
    """
    old_tweets = set(load_tweets(old_filename))
    tweets = [x.text for x in Tweet.query.all()]

    # classifiers
    traffic = get_traffic()
    relevant = get_relevant()

    # Randomize tweets, and classify them.
    random.shuffle(tweets)

    # What we are collecting here.
    selected = set()
    selected_set = []

    for tweet in tweets:
        if len(selected_set) >= count:
            break # done, don't pick more tweets.

        if tweet in old_tweets:
            continue # already selected before

        if relevant.predict1(tweet) == 1:
            traffic.predict1(traffic_tweets_features[i])
            selected_set.append([tweet.encode('utf-8'),
                                 relevant.predict1(tweet),
                                 traffic.predict1(tweet)])

    write_file(filename, selected_set)


def generate_histogram(via, outfile, window=60, since_date=None):
    scores = partition_historical(via, window=window, since_date=since_date)
    with open(outfile, 'w') as f:
        writer = csv.writer(f)
        for time_range in sorted(scores.keys()):
            writer.writerow([via, time_range[0], time_range[1]] + scores[time_range])
