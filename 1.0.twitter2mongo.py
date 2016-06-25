import json
from pymongo import MongoClient
from pymongo import Connection
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import API

consumer_key = 'h7yKYXXsSwr3JGZyaRIGV1qsm'
consumer_secret = 'lZqXNtVnkZuONdAPmXMPD6AAXzw4N1YUKSsyxZ7CjMbg59dTbD'
access_key = '2231647664-uBmD2AFfOkfZ4VORvqU8Dn3JtE7ofjCU3Yu56Mb'
access_secret = 'vnrlY9nAykeRx9iHCZrJbSV608BwljROzoTciUPwwxGkK'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = API(auth)

class CustomStreamListener(StreamListener):
    def __init__(self,api):
        self.api = api
        super(StreamListener, self).__init__()
        self.db = MongoClient().GMUCampus

    def on_data(self, data):
        print json.loads(data)
        self.db.GMUCampus.insert(json.loads(data))

    def on_error(self, status):
        print status
        return True # Don't kill the stream

    def on_timeout(self):
        print 'waiting...'
        return True # Don't kill the stream

tw_listener = CustomStreamListener(api)

stream = Stream(auth, tw_listener)

#db.GMUCampus.find({text:{$regex:/mason/i}}).limit() search by key words, command line
#stream.filter(track=['hongkong','Occupy Central'])
#stream.filter(locations=[-77.3362,38.8120,-77.2850,38.8531])
stream.filter(locations=[-77.33984726850588,38.80382953366614,-77.28294152204592,38.86360187983721])

