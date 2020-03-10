import twint
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
import asyncio
import sys
import os
import pandas as pd

from classifier import *  #esto-<---


def busqueda2(termino):
    clf = SentimentClassifier()  #agregue esto<----
    #print('-------')
    #print(clf.predict('Los perros son bonitos'))
    #print('-------')

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




    data = pd.read_csv("tweets.csv", sep=',', usecols=['id','username', 'name', 'link', 'tweet', 'likes_count', 'date'], squeeze=True).values


    data_dicc = []
    data_dicc_neg = []
    data_dicc_pos = []
    data_dicc_neu = []


    text_ant = 'asd'
    i=0
    while i < len(data):
        dicc = {}
        if (text_ant != data[i][3]):
            text_ant = data[i][3]
            dicc['name'] = data[i][1]
            dicc['username'] = data[i][2]
            dicc['tweet'] = data[i][3]
            dicc['link'] = data[i][4]
            dicc['like'] = data[i][5]
            dicc['date'] = data[i][6]
            polaridad = clf.predict(tweets[i])
            dicc['polaridad'] = polaridad

            if polaridad <= 0.4:
                dicc['sentimiento'] = 'negativo'
                data_dicc_neg.append(dicc)
            elif polaridad <= 0.6:
                dicc['sentimiento'] = 'neutro'
                data_dicc_neu.append(dicc)
            else:
                dicc['sentimiento'] = 'positivo'
                data_dicc_pos.append(dicc)


            data_dicc.append(dicc)

        i = i + 1


    
    data_dicc = sorted(data_dicc, key = lambda i: i['like'], reverse=True)
    data = data_dicc
    data = data[0:50]

    data_dicc_neg = sorted(data_dicc_neg, key=lambda i: i['like'], reverse=True)
    data_neg = data_dicc_neg
    data_neg = data_neg[0:10]

    data_dicc_neu = sorted(data_dicc_neu, key=lambda i: i['like'], reverse=True)
    data_neu = data_dicc_neu
    data_neu = data_neu[0:10]

    data_dicc_pos = sorted(data_dicc_pos, key=lambda i: i['like'], reverse=True)
    data_pos = data_dicc_pos
    data_pos = data_pos[0:10]


    #Lista que contiene el texto de cada tweet obtenido
    listaT = tweets.values
    print(str(len(listaT))+" tweets ")
    #se elimina el archivo csv
    os.remove('tweets.csv')
    return listaT, data , data_neg, data_neu, data_pos
