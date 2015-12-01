from base import DataWrapper,ClassifierWrapper

"""
	DataWrapper Class Test
"""
dataWrapper = DataWrapper()
dataWrapper.fromDict({'dataset':1})
print dataWrapper


"""
	ClassifierWrapper Class Test
"""
classifierWrapper = ClassifierWrapper()
classifierWrapper.fromDict({'plot':True})
print classifierWrapper