from base import DataWrapper,ClassifierWrapper,Serializable

"""
	Serializable Class Test
"""
class myCustomSerializableObject(Serializable):
	def __init__(self,quota=None,expired=False,obj=None):
		self.quota = quota
		self.expired = expired
		self.obj = obj
"""	
serializableobj = myCustomSerializableObject(2)
otherserializableobj = myCustomSerializableObject(3)
print serializableobj
print serializableobj.toDict()
serializableobj.fromDict({'quota':6,'obj':otherserializableobj})
print serializableobj
"""

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