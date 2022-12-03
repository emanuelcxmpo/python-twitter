import tweepy
import pandas as pd
import json
from pymongo import MongoClient
import credentials

# Autenticación para usar API Twitter
auth = tweepy.OAuthHandler(credentials.API_KEY, credentials.API_KEY_SECRET)
auth.set_access_token(credentials.ACCESS_TOKEN,
                      credentials.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

user = input("Digite el usuario: ")

print("Digite el número de tweets que se van a extraer: ")
numtweet = int(input())

tweets = api.user_timeline(screen_name=user,
                           count=numtweet,
                           include_rts=False,
                           tweet_mode='extended')

# print(tweets)

tweet_list = []

for tweet in tweets:

    refined_tweet = {
        ' Usuario': tweet.user.screen_name,
        ' Texto': tweet.full_text,
        ' Likes': tweet.favorite_count,
        ' Retweets': tweet.retweet_count,
        ' Ubicacion': tweet.user.location,
        ' Creado': tweet.created_at
    }
    tweet_list.append(refined_tweet)


df = pd.DataFrame(tweet_list)
df.to_csv(user+".csv")


df = pd.read_csv(user+".csv")
data = df.to_dict(orient="record")
print(data)


def connect_db():
    client = MongoClient("localhost", 27017)
    return client


client = connect_db()
db = client.Data_extraction
print(db)
db.user.insert_many(data)
