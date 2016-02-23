import twitter
"""
	Exemple of twitter credentials used to initialize the twitter APP
	# @jacintavaliente
"""

class TwitterAPIFactory:

	"""
		Default credentials if none are specified. @jacintavaliente
	"""
	TWITTER_API_KEY = '823HTWjuQJ9cL4uSX2ffR2sF5'
	TWITTER_API_SECRET = 'PtKYljMNHjlTcKtf4j5WfLb6MJSDDh6VyTM1lMPKxfFhLoRgj7'
	TWITTER_ACCESS_TOKEN = '2984322627-lSHzM70os2QNwucyKbQ3gqMZpSsPuo68wfdyb14'
	TWITTER_ACCESS_TOKEN_SECRET = 'DC9sh5d1r7bD0WLnc2Pd0dRd167FucH6ZoDUUZcKlogqi'

	def __init__(self,consumer_key=TWITTER_API_KEY,consumer_secret=TWITTER_API_SECRET,access_token_key=TWITTER_ACCESS_TOKEN,access_token_secret=TWITTER_ACCESS_TOKEN_SECRET):
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self.access_token_key = access_token_key
		self.access_token_secret = access_token_secret

	def getAPI(self):
		return twitter.Api(self.consumer_key, self.consumer_secret,
                  		self.access_token_key,self.access_token_secret)
