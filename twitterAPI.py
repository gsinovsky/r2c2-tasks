import twitter
"""
	Exemple of twitter credentials used to initialize the twitter APP
	# @jacintavaliente
	TWITTER_API_KEY = '823HTWjuQJ9cL4uSX2ffR2sF5'
	TWITTER_API_SECRET = 'PtKYljMNHjlTcKtf4j5WfLb6MJSDDh6VyTM1lMPKxfFhLoRgj7'
	TWITTER_ACCESS_TOKEN = '2984322627-lSHzM70os2QNwucyKbQ3gqMZpSsPuo68wfdyb14'
	TWITTER_ACCESS_TOKEN_SECRET = 'DC9sh5d1r7bD0WLnc2Pd0dRd167FucH6ZoDUUZcKlogqi'
"""

class TwitterAPIFactory:

	def __init__(self,consumer_key=None,consumer_secret=None,access_token_key=None,access_token_secret=None):
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self.access_token_key = access_token_key
		self.access_token_secret = access_token_secret

	def getAPI(self):
		return twitter.Api(self.consumer_key, self.consumer_secret,
                  		self.access_token_key,self.access_token_secret)
