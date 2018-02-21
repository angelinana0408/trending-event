import tweepy
import json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

consumer_key = 'Y3RBNaFYVnorxxSjtenC5pVz9'
consumer_secret = 'SieIxRcrGWv4hEpEzQbR2uJnuIXXkP7YsRKhYIK2j1WRMS9sjf'
access_token = '918928531744219136-QtVj3y09R25DECNEDicYpXNifw2hw13'
access_secret = 'mE8HfEpvKqW91nVrrxXRXv7YV4kWNKDGBEgcWZboylxzy'
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# use tweepy stream API to crawl real-time tweets
class MyListener(StreamListener):
    def on_data(self, data):
        try:
            with open('test_tweets.json', 'a') as f:
                f.write(data)
                print data
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return True
    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(auth, MyListener())

# the longitude and latitude of LA
LA = [-119,33,-118,34]
# the final rules set we used to crawl sports-event-related tweets
rules = ['sport','football','basketball','soccer','baseball','Ice Hockey','volleyball','swimming','boxing','marathon','wrestling','bowling','tennis','fencing','hockey','gymnastics','golf','olympic','NBA','gymnast','players','champion','defeated','wins','coach','Fighting','finals']
try:
    twitter_stream.filter(track=rules,locations=LA)
except KeyboardInterrupt:
    twitter_stream.disconnect()

print "\n\nNow start parsing tweets"

