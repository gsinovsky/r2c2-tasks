# coding: utf-8
import heapq
from datetime import datetime, timedelta
from datetime import datetime, timedelta
from sklearn.linear_model import LogisticRegression
from models import Tweet
from base import ClassifierWrapper,DataWrapper
from retriever import related_tweets_window, related_tweets_time
from utils import color_code_text
from graph import get_graph
import time
import json
from networkx.readwrite import json_graph
from utils import load_file,load_synonyms, load_words
import copy

TRAFFIC_WRAPPER = None
RELEVANT_WRAPPER = None

def get_relevant(**kwargs):
    global RELEVANT_WRAPPER
    # t0 = time.time()
    if RELEVANT_WRAPPER is None:
        synonyms = load_synonyms('./datasets/sinonimos.csv')
        words = load_words()

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
        with open('relevant_wrapper.json', 'w') as rw_json:
            json.dump(RELEVANT_WRAPPER.toDict(), rw_json)
        # with open('relevant_wrapper.json','r+') as rwjson:
        #     classifierwrapper = json.load(rwjson)
        #     print ClassifierWrapper(classifierwrapper['clf'],'./datasets/relevant.csv')
    return RELEVANT_WRAPPER

def get_traffic(**kwargs):
    global TRAFFIC_WRAPPER
    # t0 = time.time()
    if TRAFFIC_WRAPPER is None:
        synonyms = load_synonyms('./datasets/sinonimos.csv')
        words = load_words()

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
        with open('traffic_wrapper.json', 'w') as rw_json:
            json.dump(TRAFFIC_WRAPPER.toDict(), rw_json)
        # with open('traffic_wrapper.json','r+') as rwjson:
        #     classifierwrapper = json.load(rwjson)
        #     print ClassifierWrapper(classifierwrapper['clf'],'./datasets/relevant.csv')
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

def get_historic_score(source, dest, start, end, alpha=0.3):
    '''Return the historic ocurring at time [start, end]. '''
    today = datetime.now()
    today = datetime(2015,05,07,15,00)
    partitions = [
        # this week
        (today-timedelta(days=7), None),
        # last week
        (today-timedelta(days=14), today-timedelta(days=8)),
        # the rest of the current month
        (today-timedelta(days=30), today-timedelta(days=15)),
        # # one month ago
        (None, today-timedelta(days=31)),
        # (today-timedelta(days=60), today-timedelta(days=31)),
        # # 2 months ago
        # (today-timedelta(days=90), today-timedelta(days=61)),
        # # the rest of related tweets
        # (None, today-timedelta(days=91)),
    ]

    scores = []
    for (since_date, before_date) in reversed(partitions):
        scores.append(get_score(related_tweets_time(source, dest, start, end,
                                                    since_date, before_date)))

    # exponential smoothing
    t = scores[0]
    for score in scores[1:]:
        print "Initial score %f in (%s,%s)" % (score, source, dest)
        t = alpha*score + (1-alpha)*t
        print "Smoothed score %f with alpha = %f" % (t, alpha)

    # t = 0

    return t

def phi(t):
    return min(0.6, 0.2 + (0.4 * t)/120)

def build_path(p, node):
    while node != -1:
        yield node
        node = p[node]

def find_path(source, dest):
    q = [(0, source)]
    p = {}
    p[(0, source)] = -1
    visit = set()
    g = get_graph()

    with open("sectorGraph/sectorGraphProcessed.json") as data_file:
        data = json.load(data_file)

   # sectorGraph = json_graph.adjacency_graph(data)
    #g = sectorGraph

    # now = datetime.now() - timedelta(days=10)
    now = datetime(2015,05,07,15,00)
    print now
    while q:
        node = t, cur = heapq.heappop(q)
        print '****', cur
        if cur == dest:
            path = list(build_path(p, node))
            path.reverse()
            yield path
            continue

        if cur in visit:
            continue

        visit.add(cur)

        currently = now + timedelta(minutes=t)
        for succ in g[cur]:
            print 'ACTUAL'
            ACTUAL = get_stream_score(cur, succ, now=now, spoof=True)
            before = currently + timedelta(minutes=-10)
            after = currently + timedelta(minutes=10)
            print 'HISTORICO'
            """ HIST = get_historic_score(cur, succ,
                                     before.strftime('%H:%M:00'),
                                     after.strftime('%H:%M:00'))
            """
            estimado = (1-phi(t))*ACTUAL + phi(t)*0.6#HIST
            congestionValue = g[cur][succ]['travelTime']*0.03#g[cur][succ]['p'](estimado)#g[cur][succ]['travelTime']*0.03 #TODO change so that each node has a different traffic function
            cost = t + g[cur][succ]['travelTime'] + congestionValue 
            p[(cost, succ)] = node
            print cur, '->', succ, estimado
            print cur, '->', succ, cost
            heapq.heappush(q, (cost, succ))

print find_path("El Cafetal","Los Ruices").next()
