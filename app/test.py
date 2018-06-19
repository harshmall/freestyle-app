import tweepy
from tweepy import Stream
import json
import logging
import pdb

consumer_key = 'N3S8Iqxs15M4PNL8RSBUNYRvw'
consumer_secret = 'ViqFj6AliUTcae2Tms9rmdafKDGjpUj7Q11AVzRkvvpWAnvrQ3'
access_token = '1008836471908962304-bj3p94LDbUnfuGbYVM5tf9FGLYulmm'
access_token_secret = 'G26ZeLhT6ofba216yxFR6K2GRDulRNHrer4dxQjbrdXsw'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

user = api.me()
print (user.name)
queries = ["#WorldCup", "#WorldCup2018"]
tweets_per_query = 50

#new_tweets = 0
#for query in queries:
#    print ("Starting new query: " + query)
#    for tweet in tweepy.Cursor(api.search, q=query, tweet_mode="extended").items(tweets_per_query):
#
#        user = tweet.user.screen_name
#        id = tweet.id
#        url = 'http://twitter.com' + user + '/status/' + str(id)
#        print(url)
new_tweets = 0
for query in queries:
    print ("Starting new query: " + query)
    for tweet in tweepy.Cursor(api.search, q=query, tweet_mode="extended").items(tweets_per_query):

        user = tweet.user.screen_name
        id = tweet.id
        url = 'http://twitter.com' + user + '/status/' + str(id)
        print(url)

        try:
            text = tweet.retweeted_status.full_text.lower()
        except:
            text = tweet.full_text.lower()

        #pdb.set_trace()
#RETWEET AND LIKE TWEETS
        if "#worldcup" in text or "#worldcup2018" in text:
            if not tweet.retweeted:
                try:
                    tweet.retweet()
                    print('\t' + 'Retweeted')
                    new_tweets += 1
                except tweepy.TweepError as e:
                    print('\t' + 'Already Retweeted')

        if "#worldcup" in text or "#worldcup2018" in text:
                try:
                    tweet.favorite()
                    print('\t' + 'Liked')
                    new_tweets += 1
                except tweepy.TweepError as e:
                    print('\t' + 'Already Liked')

        if "#WorldCup" in text or "#WorldCup2018":
            try:
                to_follow = [tweet.retweeted_status.user.screen_name] + [i['screen_name'] for i in tweet.entities['user_mentions']]
            except:
                to_follow = [user] + [i['screen_name'] for i in tweet.entities['user_mentions']]

            for screen_name in list(set(to_follow)):
                api.create_friendship(screen_name)
                print('\t' + "Followed: " + screen_name)

print("New Tweets: " + str(new_tweets))
