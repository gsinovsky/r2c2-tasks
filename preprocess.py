# -*- coding: utf-8 -*-

import re, unicodedata
from nltk.stem.snowball import SpanishStemmer
from spelling import correct, words, train

def remove_urls(tweet):
    # remove urls
    regexp = r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))'
    return re.sub(regexp, '', tweet)

def remove_mentions(tweet):
    regexp = r'@[A-Za-z0-9-_]+'
    return re.sub(regexp, '', tweet)

def remove_punctuation(tweet):
    to_be_removed = ".,:!?()-"
    for c in to_be_removed:
        tweet = tweet.replace(c, ' ')
    return tweet

def remove_safe_html(tweet):
    regexp = r'(&gt;)+'
    return re.sub(regexp, '', tweet)

def remove_accents(tweet):
    # tweet = unicode(tweet, "utf-8")
    return unicodedata.normalize('NFKD', tweet)
    # return tweet

def remove_hashtag(tweet):
    regexp = r'#donatusmedicamentos'
    tweet = re.sub(regexp, '', tweet)
    regexp = r'#prioridadtransito'
    tweet = re.sub(regexp, '', tweet)
    regexp = r'#usbve'
    tweet = re.sub(regexp, '', tweet)
    regexp = r'#trafficcenter'
    tweet = re.sub(regexp, '', tweet)
    regexp = r'#cosasdeusbistas'
    tweet = re.sub(regexp, '', tweet)
    regexp = r'#reportanos'
    tweet = re.sub(regexp, '', tweet)
    return tweet

def remove_words(tweet):
    words = set(['via', 'RT', 'rt'])
    split_tweet = [word for word in tweet.lower().split(' ') if word.strip()]
    return ' '.join([word.strip()
                     for word in split_tweet
                     if word not in words and not word.isdigit()])

# Corrector ortografico
def fix_errors(tweet, dict):
    split_tweet = [word for word in tweet.lower().split(' ') if word.strip()]
    for w in split_tweet:
        if not (w in dict):
            # print "corrigiendo %s" % w
            w = correct(w)
    return ' '.join([word.strip()
                     for word in split_tweet])

# Diccionario
def grammar_fix(tweet, dict):
    for key, value in dict.iteritems():
        re.sub(key, value, tweet)
    return tweet

# Stemmer
def stemmer_all(tweet):
    stm = SpanishStemmer()
    split_tweet = [word for word in tweet.lower().split(' ') if word.strip()]
    return ' '.join([stm.stem(word.strip())
                     for word in split_tweet])


def process_tweet(tweet, dict, dict1):
    pipeline = [remove_urls, remove_mentions, remove_safe_html,
                remove_accents, remove_hashtag, remove_punctuation,
                grammar_fix,
                remove_words,
                # fix_errors,
                stemmer_all,]              

    # pipeline = []
    # print 'old %s' % tweet

    if not isinstance(tweet, unicode):
        tweet = unicode(tweet, "utf-8")

    for func in pipeline:
        if func == grammar_fix:
            tweet = func(tweet, dict)
        elif func == fix_errors:
            tweet = func(tweet, dict1)
        else:
            tweet = func(tweet)
    # print 'new %s' % tweet
    return tweet
