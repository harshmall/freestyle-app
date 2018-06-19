from __future__ import unicode_literals
import tweepy
from tweepy import Stream
from dotenv import load_dotenv
import os
import pdb

load_dotenv()

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

#print(consumer_key)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

for follower in tweepy.Cursor(api.followers).items():
    follower.follow()
    print ("Followed everyone that is following " + user.name)

user = api.me()
print (user.name)
queries = ["#WorldCup", "#WorldCup2018"]
tweets_per_query = 50

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


#FOLLOW ACCOUNTS
        if "#WorldCup" in text or "#WorldCup2018":
            try:
                to_follow = [tweet.retweeted_status.user.screen_name] + [i['screen_name'] for i in tweet.entities['user_mentions']]
            except:
                to_follow = [user] + [i['screen_name'] for i in tweet.entities['user_mentions']]

            try:
                for screen_name in list(set(to_follow)):
                    api.create_friendship(screen_name)
                    print('\t' + "Followed: " + screen_name)
            except tweepy.error.TweepError:
                pass


print("New Tweets: " + str(new_tweets))
