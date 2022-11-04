import json
import tweepy
import os
import credentials

# Funcion para imprimir las diferentes entidades de un tweet
def printtweetdata(n, ith_tweet,scraped_data):
    d = {"# tweet extraido": n, "usuario": ith_tweet[0], "descripcion": ith_tweet[1], "ubicacion": ith_tweet[2],
         "total tweet": ith_tweet[3], "hashtags usados": ith_tweet[4], "texto tweet": ith_tweet[5]}
    print(f"tweet extraido {n}:")
    print(f"usuario: {ith_tweet[0]}")
    print(f"description: {ith_tweet[1]}")
    print(f"ubicacion: {ith_tweet[2]}")
    print(f"total tweet: {ith_tweet[3]}")
    print(f"hashtags usados: {ith_tweet[4]}")
    print(f"texto tweet: {ith_tweet[5]}")
    scraped_data.append(d)

#Almacenamiento en un archivo Json

    if not os.path.isdir('output'):
        os.mkdir('output')
    with open(f'output/scraped_data.json', 'w') as outfile:
        json.dump(scraped_data, outfile, indent=4)


# Función para extraer diferentes entidades de un tweet
def scrape(words, numtweet, scraped_data):
    tweets = tweepy.Cursor(api.search_tweets, q=words, lang="en", tweet_mode='extended').items(numtweet)
    list_tweets = [tweet for tweet in tweets]
    i = 1
    for tweet in list_tweets:
        usuario = tweet.user.screen_name
        description = tweet.user.description
        ubicacion = tweet.user.location
        totaltweet = tweet.user.statuses_count
        hashtags = tweet.entities['hashtags']

        try:
            text = tweet.retweeted_status.text
        except AttributeError:
            text = tweet.full_text
        hashtext = list()
        for j in range(0, len(hashtags)):
            hashtext.append(hashtags[j]['text'])
        ith_tweet = [usuario, description, ubicacion, totaltweet, hashtext,text]

        printtweetdata(i, ith_tweet, scraped_data)
        i = i + 1


if __name__ == '__main__':

    #Autenticación para usar API Twitter
    auth = tweepy.OAuthHandler(credentials.API_KEY, credentials.API_KEY_SECRET)
    auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)


    # Inicia ejecución del programa
    print("Digite el Hashtag: ")
    words = input()

    print("Digite el número de tweets que se van a extraer: ")
    numtweet = int(input())
    scraped_data = []

    print("Buscando twits...")
    scrape(words, numtweet, scraped_data)

    print('La extracción se ha completado.')