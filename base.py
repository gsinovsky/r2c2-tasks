# coding: utf-8

from sklearn import cross_validation
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.externals import joblib
from utils import load_file
from preprocess import process_tweet
import matplotlib.pyplot as plt
from plots import plot_learning_curve, plot_confusion_matrix
from utils import load_synonyms, load_words
import pickle
import cPickle

def word_matrix(corpus, vectorizer=None):
    if vectorizer is None:
        # Bag of words
        vectorizer = TfidfVectorizer(min_df=1) 
        # n-grama
        # vectorizer = CountVectorizer(ngram_range=(1, 2), token_pattern=r'\b\w+\b', min_df=1)

    X = vectorizer.fit_transform(corpus)
    vocab = vectorizer.get_feature_names()

    return vectorizer, X, vocab

class DataWrapper(object):
    '''A helper class to wrap our data files and make them easier to
    use.'''

    def __init__(self, filename, vectorizer=None):
        self.dataset = list(load_file(filename))
        self.dict = load_synonyms('./datasets/sinonimos.csv')
        self.dict1 = load_words()

        if vectorizer is not None:
            self.vectorizer = vectorizer
            self.matrix = self.vectorizer.transform(self.processed_tweets)
            self.vocab = vectorizer.get_feature_names()

        else:
            vectorizer, X, vocab = word_matrix(self.processed_tweets)
            self.vectorizer = vectorizer
            self.matrix = self.X = X
            self.vocab = vocab

    def __init__(self,filename=None,vectorizer=None,_dict=load_synonyms('./datasets/sinonimos.csv'),dict1=load_words(),matrix=None,vocab=None):
        self.dataset = filename
        self.vectorizer = vectorizer
        self.dict = _dict
        self.dict1 = dict1
        self.matrix = matrix
        self.vocab = vocab

    def fromDict(self,wrapperDict):
        if 'matrix' in wrapperDict:
            self.matrix = wrapperDict['matrix']
        if 'vocab' in wrapperDict:
            self.vocab = wrapperDict['vocab']


    """
        dataset,dict y dict son atributos estaticos.
        Los atributos matrix y vocab son producto del procesamiento de los tweets
        en consecuencia solo nos interesa guardar estos datos
    """
    def toDict(self):
        return {'matrix':cPickle.dumps(self.matrix),'vocab':self.vocab}

    @property
    def tweets(self):
        if not hasattr(self, '_tweets'):
            self._tweets = [x[0] for x in self.dataset]

        return self._tweets

    @property
    def processed_tweets(self):
        if not hasattr(self, '_processed_tweets'):
            self._processed_tweets = [process_tweet(x, self.dict, self.dict1) for x in self.tweets]

        return self._processed_tweets

    @property
    def labels(self):
        if not hasattr(self, '_labels'):
            self._labels = [int(x[1]) for x in self.dataset]

        return self._labels


class ClassifierWrapper(object):
    '''A helper class to wrap all the stuff we are doing. This expects
    that the file that is passed each row is in the form [tweet, label]'''


    # def __init__(self, clf, filename, plot=False):
    #     self.clf = clf
    #     self.dataset = DataWrapper(filename)
    #     self.plot = plot
    #     self.dict = load_synonyms('./datasets/sinonimos.csv')
    #     self.dict1 = load_words()

    def __init__(self,clf=None,dataset=None,plot=False,_dict=load_synonyms('./datasets/sinonimos.csv'),dict1=load_words()):
        self.clf = clf
        self.dataset = dataset
        self.plot = plot
        self.dict = _dict
        self.dict1 = load_words()

    def fromDict(self,wrapperDict):
        if 'clf' in wrapperDict:
            self.clf = wrapperDict['clf']
        if 'dataset' in wrapperDict:
            dataWrapper = DataWrapper()
            self.dataset = dataWrapper.fromDict(wrapperDict['dataset'])
        if 'plot' in wrapperDict:
            self.plot = wrapperDict['plot']


    def toDict(self):
        return {'clf':pickle.dumps(self.clf),'dataset':self.dataset.toDict(),'plot':self.plot}

    def vtransform(self, tweets):
        return self.dataset.vectorizer.transform([process_tweet(x, self.dict, self.dict1) for x in tweets])

    def train(self, test_size=0.2, random_state=None):
        # Split dataset into training and validation.
        X_train, X_test, y_train, y_test = cross_validation\
            .train_test_split(self.dataset.matrix,
                              self.dataset.labels,
                              test_size=test_size,
                              random_state=random_state)
        self.clf.fit(X_train, y_train)
        y_pred = self.clf.predict(X_test)
        print 'accuracy on testing set', self.clf.score(X_test, y_test)
        cm = confusion_matrix(y_test, y_pred)
        print cm
        print classification_report(y_test, y_pred,
                                    target_names=['verde', 'amarillo', 'rojo'])
        
        # plot_confusion_matrix(cm)

        return cm

    def validate(self, filename):
        validation_dataset = DataWrapper(filename, self.dataset.vectorizer)
        print 'accuracy on validation set', self.clf.score(validation_dataset.matrix,
                                                           validation_dataset.labels)


    def cross_validate(self, test_size=0.25, n_iter=100):
        cv = cross_validation.ShuffleSplit(self.dataset.matrix.shape[0],
                                           n_iter=n_iter, test_size=test_size)

        # title = "Learning Curves (Logistic Regression)"
        # plot_learning_curve(self.clf, title,
        #                 self.dataset.matrix, self.dataset.labels,
        #                 cv=cv, n_jobs=4)        

        scores = cross_validation.cross_val_score(self.clf,
                                                  self.dataset.matrix,
                                                  self.dataset.labels,
                                                  cv=cv)
        print scores
        print 'Accuracy: %0.2f (+/- %0.2f)' % (scores.mean(), scores.std()*2)

    def predict(self, values):
        vvalues = self.vtransform(values)
        return self.clf.predict(vvalues)

    def predict1(self, value):
        return self.predict([value])[0]
