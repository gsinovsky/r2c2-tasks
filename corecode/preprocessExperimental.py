# -*- coding: utf-8 -*-
import re, unicodedata
from nltk.stem.snowball import SpanishStemmer
from unidecode import unidecode

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
    #return unicodedata.normalize('NFKD', tweet)
    return unidecode(tweet) 
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
    regexp = r'#'
    tweet = re.sub(regexp, '', tweet)
    return tweet

def remove_words(tweet):
    words = set(['via', 'RT', 'rt'])
    split_tweet = [word for word in tweet.lower().split(' ') if word.strip()]
    return ' '.join([word.strip()
                     for word in split_tweet
                     if word not in words and not word.isdigit()])


def delete_stop_words(tweet, dict):
    tweet_words = [word for word in tweet.split()]
    #Si la palabra está en el diccionario de StopWords no se incluye
    tweet_synonyms = [word for word in tweet_words if not word in dict] 
    fixed_tweet = ' '.join(tweet_synonyms)
    return fixed_tweet

# Diccionario
def grammar_fix(tweet, dict, dict1):
    #primero acomodo palabras en los tweets   
    tweet_words = [word for word in tweet.split()]
    #Si la palabra está en el diccionario de sinónimos, se reemplaza, si no, se deja la misma.
    tweet_synonyms = [word if not word in dict else dict[word] for word in tweet_words] 
    #fixed_tweet = ' '.join(tweet_synonyms)
    fixed_tweet = ' '.join(tweet_synonyms)
    #luego substituyo las palabras claves compuestas
    for key in sorted(dict1.iterkeys()):
                #para la correctitud del algoritmo, es importante el orden
                fixed_tweet = re.sub(key, dict1[key], fixed_tweet)
    return fixed_tweet
    
# Stemmer
def stemmer_all(tweet):
    stm = SpanishStemmer()
    split_tweet = [word for word in tweet.lower().split(' ') if word.strip()]
    return ' '.join([stm.stem(word.strip())
                     for word in split_tweet])


def process_tweet(tweet, dict, dict1, dict2, stop_words):
    #list of function that process a tweet
    pipeline = [remove_urls, remove_mentions, remove_safe_html,
                remove_accents, remove_hashtag, remove_punctuation,
                remove_words, delete_stop_words, grammar_fix,
                ]              

    if not isinstance(tweet, unicode):
        tweet = unicode(tweet, "utf-8")

    for func in pipeline:
        if func == grammar_fix:
            tweet_words = func(tweet, dict, dict1)
        elif func == delete_stop_words:
            tweet = func(tweet,stop_words)
        else:
            tweet = func(tweet)
    # print 'new %s' % tweet
    return tweet_words