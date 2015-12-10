from sklearn.linear_model import LogisticRegression
import pickle
from sklearn.externals import joblib
import json
from base import ClassifierWrapper

clf = LogisticRegression(C=8.5)

# s = pickle.dumps(clf)
# fileGraph = open('pickle', 'w+')
# fileGraph.write(s)
# fileGraph.close()

#pickle.dump(clf,'pickledumps')

with open('pickledumps', 'wb') as handle:
  pickle.dump(clf, handle)

with open('pickledumps') as data_file:
	#print data_file.read()
	print pickle.loads(data_file.read())


joblib.dump(clf, 'filename.pkl')
clf = joblib.load('filename.pkl') 
#print clf


#print type(s)


"""
	 DECODE CLASSIFIERWRAPPER
"""

with open('relevant_wrapper.json','r+') as rwjson:
	classifierwrapper = json.load(rwjson)
	for k in classifierwrapper:
		print k
	newclassifierobj = ClassifierWrapper()
	newclassifierobj.fromDict(classifierwrapper)