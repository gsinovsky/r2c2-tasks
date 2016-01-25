# coding: utf-8
from retriever import related_tweets_window, related_tweets_time
from utils import load_file, load_synonyms, load_words
from sklearn.linear_model import LogisticRegression
from base import ClassifierWrapper, DataWrapper
from graph import get_graph, get_TravelTime
from networkx.readwrite import json_graph
from datetime import datetime, timedelta
from utils import color_code_text
from models import Tweet, Route, HistoricScore
import heapq
import time
import json
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
    @procedure exponential_smoothing Returns the exponential smoothing of
    the given scores.
    @param scores Scores to be exponentially smoothed.
    @param alpha Alpha to be used in exponential smoothing.
"""
def exponential_smoothing(scores,alpha):

    smoothedScore = scores[0]
    
    if isinstance(smoothedScore,HistoricScore):
        
        smoothedScore = smoothedScore.score

        for score in scores[1:]:
            smoothedScore = alpha*score.score + (1-alpha)*smoothedScore
    else:
        
        for score in scores[1:]:
            smoothedScore = alpha*score + (1-alpha)*smoothedScore

    return smoothedScore

"""
    @procedure get_stored_historic_score Returns the historic score that was 
    stored in a JSON file. If it doesn't exist, it calculates it and stores it.
"""

def get_stored_historic_score(origin,destination,startTime,endTime,sinceDate,beforeDate,alpha):

    score = None
    scores = None
    calculatedScore = -1
    today = datetime.now()
    today = datetime(2015,05,07,15,00)

    # If the route already exists, get from database, else save new instance.
    route = Route.get_or_none(origin=origin,destination=destination)
    if route is None:
        route = Route(origin=origin,destination=destination)
        route.save()

    # If both extremes of the date range are not none, then the scores of
    # the tweets from that time range are retrived.
    if sinceDate is not None and beforeDate is not None:
        scores = HistoricScore.get_scores_between_dates(route_id=route.id,
                    lower_timestamp=sinceDate,higher_timestamp=beforeDate)
    else:
        if sinceDate is None:
            scores = HistoricScore.get_scores_until_date(route_id=route.id,timestamp=beforeDate)

        if beforeDate is None:
            scores = HistoricScore.get_scores_from_date(route_id=route.id,timestamp=sinceDate)
    
    #If previous scores don't exist, then a score is calculated and saved to the database.
    if scores is None or not scores:

        # Verifies if a score was already calculated for the route with today's date.
        score = HistoricScore.get_or_none(route_id=route.id,timestamp=today)
        if score is None:
            calculatedScore = get_score(related_tweets_time(origin, destination, startTime, endTime,
                                        sinceDate, beforeDate))

            score = HistoricScore(route_id=route.id,timestamp=today,score=calculatedScore)
            score.save()
        else:
            calculatedScore = score.score
    
    else:
        calculatedScore = exponential_smoothing(scores,alpha)   
    
    return calculatedScore


def get_historic_score(origin, destination, startTime, endTime, alpha=0.3):
    
    '''Return the historic ocurring at time [startTime, endTime]. '''
    
    today = datetime.now()
    today = datetime(2015,05,07,15,00)

    #Ranges of dates of old tweets to be processed    
    dateRanges = [
        (today-timedelta(days=1), None), #One day ago
        (today-timedelta(days=7), None), #This week
        (today-timedelta(days=14), today-timedelta(days=8)), #Last week
        (today-timedelta(days=30), today-timedelta(days=15)), #The rest of the current month 
        (today-timedelta(days=31), None), #One month ago 
        (today-timedelta(days=60), today-timedelta(days=31)),
        (today-timedelta(days=90), today-timedelta(days=61)), #2 months ago
        (None, today-timedelta(days=91)), #The rest of related tweets
    ]

    scores = []

    #Tweets from one week ago
    sinceDate, beforeDate = dateRanges[1]

    score = get_score(related_tweets_time(origin,destination,startTime,endTime,sinceDate,beforeDate))
    scores.append(score)

    #Study case: Tweets from two weeks ago
    sinceDate, beforeDate = dateRanges[3] 
    score = get_stored_historic_score(origin,destination,startTime,endTime,sinceDate,beforeDate,alpha)
    scores.append(score)
    
    #Study case: Tweets from a month ago
    sinceDate, beforeDate = dateRanges[4] 
    score = get_stored_historic_score(origin,destination,startTime,endTime,sinceDate,beforeDate,alpha)
    scores.append(score)

    #Exponential smoothing of the score
    smoothedScore = exponential_smoothing(scores,alpha)

    return smoothedScore

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
    print "Current Date: %s\n" %(now)

    while queue:
        #Tuple: node = (cost, current sector)
        node = accumulatedCost, currentNode = heapq.heappop(queue) 
       
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
            print 'ACTUAL SCORE: %.2f' %(actualScore)
            
            before = accumulatedTime + timedelta(minutes=-10)
            after = accumulatedTime + timedelta(minutes=10)
            
            historicScore = get_historic_score(currentNode, successor,
                                     before.strftime('%H:%M:00'),
                                     after.strftime('%H:%M:00'))

            print 'HISTORIC SCORE: %.2f' %(historicScore)

            estimatedScore = (1-phi(accumulatedCost))*actualScore + phi(accumulatedCost)*historicScore

            #TODO change so that each node has a different traffic penalty function
            congestionValue = get_TravelTime(graph,currentNode,successor)*estimatedScore

            cost = accumulatedCost + get_TravelTime(graph,currentNode,successor) + congestionValue 
            
            path[(cost, successor)] = node
            print "ARC: %s -> %s ***** SCORE: %.2f, COST: %.2f\n" %(currentNode, successor, estimatedScore, cost)
            heapq.heappush(queue, (cost, successor))

