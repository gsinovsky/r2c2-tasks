# coding: utf-8
import json
import twitter
import collections
import __main__
from utils import load_file, load_stop_words, load_routes, file_is_empty
from collections import Counter
from preprocessExperimental import process_tweet, remove_accents
from utils import load_synonyms, load_words
import cPickle as pickle
import os
import re
from graph import get_graph

def retrieve_tweets():
    TWITTER_API_KEY = 'rOYPSNueekDLveKkpIgdU7HpH'
    TWITTER_API_SECRET = 'LJyqgkeY8CeVd78fc2SsaUGFlVHRLSEiftTmBPxChIwQLsfhw9'
    TWITTER_ACCESS_TOKEN = '4165949542-AGCBrmIYkiw7JiKeDeI0trMwbALFzwgHUo9GI5r'
    TWITTER_ACCESS_TOKEN_SECRET = 'evnTf5U53VBpkLqpdaUTuFYY89ZwsSBasTMa0u0oclIuB'

    kw = {}
    api = twitter.Api(consumer_key=TWITTER_API_KEY,
                      consumer_secret=TWITTER_API_SECRET,
                      access_token_key=TWITTER_ACCESS_TOKEN,
                      access_token_secret=TWITTER_ACCESS_TOKEN_SECRET)
    return api.GetHomeTimeline(count=200, **kw)
    #return api.GetUserTimeline(screen_name="traffictracker5",count=1)
       

def count_routes():
    synonyms = load_synonyms('./datasets/sinonimos.csv')
    synonyms1 = load_synonyms('./datasets/sinonimos2.csv')
    dictionary = load_words()
    stop_words = load_stop_words('./datasets/stop-words.txt')
    routes = load_routes('./datasets/routes.txt')
    Tweets = retrieve_tweets();
    counter = Counter()
    
    if not file_is_empty('./datasets/counter.txt'):
        with open('./datasets/counter.txt') as fp:
            counter = pickle.load(fp)
    
    for tweet in Tweets:
        Tweet_words = process_tweet(tweet.text, synonyms, synonyms1, dictionary, stop_words)
        for route in routes:
            #busca el nombre de las rutas en un tweet para contarlas
            if re.search(route,Tweet_words):
                counter[route]+=1
                
    print counter
    with open('counter.txt', 'wb') as fp:
        pickle.dump(counter, fp)
        fp.close()

def get_top_sectors():
    
    synonyms = load_synonyms('./datasets/sinonimos.csv')
    synonyms1 = load_synonyms('./datasets/sinonimos2.csv')
    dictionary = load_words()
    stop_words = load_stop_words('./datasets/stop-words.txt')
    routes = load_routes('./datasets/routes.txt')

    counter = Counter()

    with open('counter.txt') as fp:
        counter = pickle.load(fp)

    topRoutes = set(counter.elements())

    sectorGraph = get_graph()

    listRoutes = list(topRoutes)

    topSectors = []
    counter = 0

    for avenue in listRoutes:
        for (x, y) in sectorGraph.edges():
            routesEdge = sectorGraph.edge[x][y]['routes']
            for route in routesEdge:
                processedRoute = process_tweet(route, synonyms, synonyms1, dictionary, stop_words)

                if (processedRoute.find(avenue) > -1):
                    topSectors.append({'from': x, 'to': y})

    return json.dumps(topSectors)

if __name__ == '__main__':
    count_routes()
