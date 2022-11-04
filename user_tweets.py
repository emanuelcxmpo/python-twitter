import tweepy
import pandas as pd
import json
from datetime import datetime
# import s3fs
import pymongo
import credentials

#Autenticación para usar API Twitter
auth = tweepy.OAuthHandler(credentials.API_KEY, credentials.API_KEY_SECRET)
auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

api= tweepy.API(auth)


user = input("Digite el usuario: ")

tweets = api.user_timeline(screen_name=user,
                          count=200,
                          include_rts = False ,
                          tweet_mode = 'extended')

print(tweets)

tweet_list = []

for tweet in tweets:

    text= tweet._json["full_text"]

    refined_tweet = {'Usuario': tweet.user.screen_name,
                  ' Texto' : text,
                  ' Likes' : tweet.favorite_count,
                  ' Retweets' : tweet.retweet_count,
                  ' Creado' : tweet.created_at}
    tweet_list.append(refined_tweet)


df = pd.DataFrame(tweet_list)
df.to_csv("user.csv")



# cliente = pymongo.MongoClient("mongodb://locathost:27017")
# df = pd.read_csv("user.csv")
# data = df.to_dict(orient= "record")
# print(data)

# db = cliente("Data_extraction")
# print(db)

# db.ElonMusk = twitter.insert_many(data)