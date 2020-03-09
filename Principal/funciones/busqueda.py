import twint
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
import asyncio
import sys
import os
import pandas as pd


def busqueda(termino):
    
    limite = 850
    asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())  #Soluciona un problema de threads
    c = twint.Config()
    c.Search = termino
    c.Lang = 'es'
    c.Popular_tweets = True
    c.Limit = limite
    
    c.Store_csv = True
    c.Output = "tweets.csv"

    print("inicio Search ("+termino+")>")
    #Para que 'twint.run.Search(c)' no imprima los valores por consola
    sys.stdout = open(os.devnull, "w") 
    twint.run.Search(c)
    sys.stdout = sys.__stdout__
    print("termino Search >")
    

    #Se lee solo la columna 'tweet' del archivo "tweets.csv"
    tweets = pd.read_csv("tweets.csv", sep=',', usecols=['tweet'], squeeze=True)

    data = pd.read_csv("tweets.csv", sep=',', usecols=['username', 'name', 'link', 'tweet', 'likes_count', 'date'], squeeze=True).values

    data_dicc = []
    for i in range(len(data)):
        dicc = {}
        dicc['name'] = data[i][0]
        dicc['username'] = data[i][1]
        dicc['tweet'] = data[i][2]
        dicc['link'] = data[i][3]
        dicc['like'] = data[i][4]
        dicc['date'] = data[i][5]
        data_dicc.append(dicc)
    
    data_dicc = sorted(data_dicc, key = lambda i: i['like'], reverse=True)
    data = data_dicc
    data = data[0:30]

    #Lista que contiene el texto de cada tweet obtenido
    listaT = tweets.values
    print(str(len(listaT))+" tweets ")
    #se elimina el archivo csv
    os.remove('tweets.csv')
    return listaT, data
