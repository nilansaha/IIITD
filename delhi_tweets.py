import tweepy
from tweepy import OAuthHandler
import json
import sys
from pymongo import MongoClient

# Step 1 - Authenticate
ckey="2kTgljp9S2D8O1d0BppoXyRbU"
csecret="QAt50djwAB2Xzixh2IRBlOyG2G6Fx76BttETRb3eOP3OiHDxcX"
atoken="798916088108969985-rAHUm70XhOdNwTSGK8q7lMzqgSgbxs4"
asecret="v2WJUDPNysxT1GZcUuEZLZSZxShDiCywfdb4ZX5cOsXmi"


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = tweepy.API(auth)

client = MongoClient('localhost:27017')
db = client.IIITD

#Step 3 - Retrieve Tweets
public_tweets = tweepy.Cursor(api.search, q = 'CropBurning',since='2017-12-09',until='2017-12-10', result_type ='recent', lang = 'en').items(2000)



#CHALLENGE - Instead of printing out each tweet, save each Tweet to a CSV file
#and label each one as either 'positive' or 'negative', depending on the sentiment
#You can decide the sentiment polarity threshold yourself

#if len(public_tweets) == 0:
#    print "Sexy"

#print len(list(public_tweets))

i = 0
for tweet in public_tweets:
    all_data = tweet._json
    #tweetx = all_data["text"]
    # username = all_data["user"]["screen_name"]
    date = all_data["created_at"]
    print date
    #print tweetx
    # print date
    # print tweetx
    # print ""
    #print type(all_data)
    #print tweetx
    db.delhi.insert(all_data)
    i = i + 1
print i
#print len(public_tweets)
