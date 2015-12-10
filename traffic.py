# coding: utf-8
import heapq
from datetime import datetime, timedelta
from datetime import datetime, timedelta
from sklearn.linear_model import LogisticRegression
from models import Tweet
from base import ClassifierWrapper,DataWrapper
from retriever import related_tweets_window, related_tweets_time
from utils import color_code_text
from graph import get_graph, get_TravelTime
import time
import json
from networkx.readwrite import json_graph
from utils import load_file,load_synonyms, load_words
import copy
import os

TRAFFIC_WRAPPER = None
RELEVANT_WRAPPER = None

def get_relevant(**kwargs):
    global RELEVANT_WRAPPER
    # t0 = time.time()
    if RELEVANT_WRAPPER is None:
        wrapperFile = 'wrappers/relevant_wrapper.json'
        synonyms = load_synonyms('./datasets/sinonimos.csv')
        words = load_words()
        if os.path.isfile(wrapperFile):
            with open(wrapperFile,'r+') as rwjson:
                RELEVANT_WRAPPER = ClassifierWrapper()
                RELEVANT_WRAPPER.jsonLoads(rwjson.read())
                RELEVANT_WRAPPER.synonyms = copy.deepcopy(synonyms)
                RELEVANT_WRAPPER.words = copy.deepcopy(words)
                RELEVANT_WRAPPER.dataset.dataset = list(load_file('./datasets/relevant.csv'))
                RELEVANT_WRAPPER.dataset.synonyms = copy.deepcopy(synonyms)

                RELEVANT_WRAPPER.dataset.words = copy.deepcopy(words)

                return RELEVANT_WRAPPER

        clf = kwargs.pop('clf', LogisticRegression(C=10))
        dataWrapperDataset = list(load_file('./datasets/relevant.csv'))
        dataWrapper = DataWrapper(dataset=dataWrapperDataset,synonyms=copy.deepcopy(synonyms),words=copy.deepcopy(words))
        dataWrapper.resolveMatrix()

        wrapper = ClassifierWrapper(clf=clf,dataset=dataWrapper,synonyms=copy.deepcopy(synonyms),words=copy.deepcopy(words))

        cross_validate = kwargs.pop('cross_validate', False)
        if cross_validate:
            wrapper.cross_validate()
        wrapper.train()
        # print time.time() - t0, "seconds from relevant classifier"
        RELEVANT_WRAPPER = wrapper
        with open(wrapperFile, 'w') as rw_json:
            json.dump(RELEVANT_WRAPPER.toDict(), rw_json)
    return RELEVANT_WRAPPER

def get_traffic(**kwargs):
    global TRAFFIC_WRAPPER
    # t0 = time.time()
    if TRAFFIC_WRAPPER is None:
        wrapperFile = 'wrappers/traffic_wrapper.json'
        synonyms = load_synonyms('./datasets/sinonimos.csv')
        words = load_words()

        if os.path.isfile(wrapperFile):
            with open(wrapperFile,'r+') as rwjson:
                TRAFFIC_WRAPPER = ClassifierWrapper()
                TRAFFIC_WRAPPER.jsonLoads(rwjson.read())
                TRAFFIC_WRAPPER.dataset.dataset = list(load_file('./datasets/traffic2.csv'))
                TRAFFIC_WRAPPER.synonyms = copy.deepcopy(synonyms)
                TRAFFIC_WRAPPER.words = copy.deepcopy(words)
                TRAFFIC_WRAPPER.dataset.synonyms = copy.deepcopy(synonyms)
                TRAFFIC_WRAPPER.dataset.words = copy.deepcopy(words)
                return TRAFFIC_WRAPPER

        clf = kwargs.pop('clf', LogisticRegression(C=8.5))
        dataWrapperDataset = list(load_file('./datasets/traffic2.csv'))
        dataWrapper = DataWrapper(dataset=dataWrapperDataset,synonyms=copy.deepcopy(synonyms),words=copy.deepcopy(words))
        dataWrapper.resolveMatrix()

        wrapper = ClassifierWrapper(clf=clf,dataset=dataWrapper,synonyms=copy.deepcopy(synonyms),words=copy.deepcopy(words))
        cross_validate = kwargs.pop('cross_validate', True)
        if cross_validate:
            wrapper.cross_validate()
        wrapper.train()
        # print time.time() - t0, "seconds from the multiclass classifier"
        TRAFFIC_WRAPPER = wrapper
        with open(wrapperFile, 'w') as rw_json:
            json.dump(TRAFFIC_WRAPPER.toDict(), rw_json)
    return TRAFFIC_WRAPPER

def get_score(tweets):
    '''Score tweets'''
    relevant = get_relevant()
    traffic = get_traffic()
    total_tweets = 0
    sum_scores = 0
    hist = [0,0,0]
    # PROMEDIO
    for tweet in tweets:
        if relevant.predict1(tweet.text) == 1:
            # color_code_text(tweet.text, traffic.predict1(tweet.text))
            sum_scores += traffic.predict1(tweet.text)
            hist[traffic.predict1(tweet.text)] += 1
            total_tweets += 1
    # print hist
    return sum_scores / float(total_tweets) if total_tweets > 0 else 0


def get_stream_score(source, dest, window=45, now=None, spoof=False):
    '''Get the window of tweets'''
    qs = related_tweets_window(source, dest, window, now)
    if spoof:
        qs = qs.filter(Tweet.created_at <= now)
    return get_score(qs)

"""
    @procedure get_stored_historic_score Returns the historic score that was 
    stored in a JSON file. If it doesn't exist, it calculates it and stores it.
"""

def get_stored_historic_score(source,dest,start,end,since_date,before_date):

    key = str((source,dest))

    scoresFile = 'scores/scores.json'
    scores = {}
    score = None

    if os.path.isfile(scoresFile):
        with open(scoresFile,'r') as scoresJson:
            try:
                scores = json.load(scoresJson)
            except ValueError:
                pass

        try:
            score = scores[key]
        except KeyError:       
            pass

    if score is None:
        score = get_score(related_tweets_time(source, dest, start, end,
                                              since_date, before_date))
        scores[key] = score 

        with open(scoresFile, 'w') as scoresJson:
            json.dump(scores,scoresJson,indent=4)

    return score


def get_historic_score(origin, destination, startTime, endTime, alpha=0.3):
    '''Return the historic ocurring at time [startTime, endTime]. '''
    today = datetime.now()
    today = datetime(2015,05,07,15,00)
    partitions = [
        # this week
        (today-timedelta(days=1), None),
        
        # # last week
        # (today-timedelta(days=14), today-timedelta(days=8)),
        # # the rest of the current month
        # (today-timedelta(days=30), today-timedelta(days=15)),
        # # # one month ago
        # (None, today-timedelta(days=31)),


        # (today-timedelta(days=60), today-timedelta(days=31)),
        # # 2 months ago
        # (today-timedelta(days=90), today-timedelta(days=61)),
        # # the rest of related tweets
        # (None, today-timedelta(days=91)),
    ]

    scores = []

    score = get_stored_historic_score(origin,destination,startTime,endTime,today-timedelta(days=1),None)
    scores.append(score)
    
    # for (since_date, before_date) in reversed(partitions):
    #     scores.append(get_score(related_tweets_time(origin, destination, startTime, endTime,
    #                                                 since_date, before_date)))

    # exponential smoothing
    t = scores[0]
    for score in scores[1:]:
        print "Initial score %f in (%s,%s)" % (score, origin, destination)
        t = alpha*score + (1-alpha)*t
        print "Smoothed score %f with alpha = %f" % (t, alpha)

    # t = 0

    return t

def phi(t):
    return min(0.6, 0.2 + (0.4 * t)/120)

def build_path(path, node):
    while node != -1:
        yield node
        node = path[node]

def find_path(origin, destination):

    queue = [(0, origin)]
   
    path = {}
    path[(0, origin)] = -1
   
    visitedNodes = set()
    graph = get_graph()

    now = datetime(2015,05,07,15,00)
    print now
    while queue:
        node = accumulatedCost, currentNode = heapq.heappop(queue) #Tuple: node = (cost, current sector)
       
        
        print '----- Current Node: %s -----\n' %(currentNode)
        if currentNode == destination:
            path = list(build_path(path, node))
            path.reverse()
            yield path
            continue

        if currentNode in visitedNodes:
            continue

        visitedNodes.add(currentNode)

        accumulatedTime = now + timedelta(minutes=accumulatedCost)

        for successor in graph[currentNode]:
        
            actualScore = get_stream_score(currentNode, successor, now=now, spoof=True)
            print 'ACTUAL SCORE: %s' %(actualScore)
            
            before = accumulatedTime + timedelta(minutes=-10)
            after = accumulatedTime + timedelta(minutes=10)
            
            historicScore = get_historic_score(currentNode, successor,
                                     before.strftime('%H:%M:00'),
                                     after.strftime('%H:%M:00'))

            print 'HISTORIC SCORE: %s' %(historicScore)

            estimatedScore = (1-phi(accumulatedCost))*actualScore + phi(accumulatedCost)*historicScore

            #TODO change so that each node has a different traffic penalty function
            congestionValue = get_TravelTime(graph,currentNode,successor)*estimatedScore

            cost = accumulatedCost + get_TravelTime(graph,currentNode,successor) + congestionValue 
            
            path[(cost, successor)] = node
            print "ARC: %s -> %s ***** SCORE: %s, COST: %s\n" %(currentNode, successor, estimatedScore, cost)
            heapq.heappush(queue, (cost, successor))

print find_path("El Cafetal","Los Ruices").next()
