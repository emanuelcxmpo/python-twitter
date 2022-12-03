import json
import tweepy
import os
import credentials

# Funcion para imprimir las diferentes entidades de un tweet
def printtweetdata(n, in_tweet, extracted_data):
    d = {"# tweet extraido": n, "usuario": in_tweet[0], "descripcion": in_tweet[1], "ubicacion": in_tweet[2],
         "total tweet": in_tweet[3], "hashtags usados": in_tweet[4], "texto tweet": in_tweet[5]}
    print(f"tweet extraido {n}:")
    print(f"usuario: {in_tweet[0]}")
    print(f"description: {in_tweet[1]}")
    print(f"ubicacion: {in_tweet[2]}")
    print(f"total tweet: {in_tweet[3]}")
    print(f"hashtags usados: {in_tweet[4]}")
    print(f"texto tweet: {in_tweet[5]}")
    extracted_data.append(d)

#Almacenamiento en un archivo Json
    if not os.path.isdir('datos'):
        os.mkdir('datos')
    with open(f'datos/datos_extraidos.json', 'w') as outfile:
        json.dump(extracted_data, outfile, indent=4)


# Función para extraer diferentes entidades de un tweet
def extraccion(words, numtweet, extracted_data):
    tweets = tweepy.Cursor(api.search_tweets, q=words, lang="es", tweet_mode='extended').items(numtweet)
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
        in_tweet = [usuario, description, ubicacion, totaltweet, hashtext, text]

        printtweetdata(i, in_tweet, extracted_data)
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
    extracted_data  = []

    print("Buscando twits...")
    extraccion(words, numtweet, extracted_data)

    print('La extracción se ha completado.')