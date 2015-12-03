from base import DataWrapper,ClassifierWrapper,JSONSerializable
import cPickle

"""
	Serializable Class Test
"""
class myCustomSerializableObject(JSONSerializable):
	def __init__(self,quota=None,expired=False):
		self.quota = quota
		self.expired = expired

	def fromDict(self,attributesDictionary):
		self.__dict__.update(attributesDictionary)

	def toDict(self):
		return self.__dict__
	
serializableobj = myCustomSerializableObject(2)
print serializableobj
print "toDic: %s" %(serializableobj.toDict())
print "Json Dumps:%s" % (serializableobj.jsonDumps())

serializableobj.jsonLoads(serializableobj.jsonDumps())
print "JsonLoads:%s" %(serializableobj.toDict())


"""
	DataWrapper Class Test
"""
dataWrapper = DataWrapper()
dataWrapperDict = {'dataset':1}
dataWrapper.fromDict(dataWrapperDict)
print dataWrapper


"""
	ClassifierWrapper Class Test
"""
classifierWrapper = ClassifierWrapper()
classifierWrapperDict = {'plot':True}
classifierWrapper.fromDict(classifierWrapperDict)
print classifierWrapper

"""
	Testing Decoders
"""
with open('relevant_wrapper.json','r+') as rwjson:
    classifierWrapper = ClassifierWrapper()
    classifierWrapper.jsonLoads(rwjson.read())
    print len(cPickle.dumps(classifierWrapper.dataset.matrix))

with open('traffic_wrapper.json','r+') as rwjson:
	classifierWrapper = ClassifierWrapper()
	classifierWrapper.jsonLoads(rwjson.read())