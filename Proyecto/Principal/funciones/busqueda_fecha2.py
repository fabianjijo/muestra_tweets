import twint
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
import asyncio
import sys
import os
import pandas as pd
from datetime import date, timedelta
from classifier import *

import numpy as np
import numpy.random
import matplotlib.pyplot as plt


def busqueda_por_fecha2(termino, desde, hasta, hastaFinal, solo_busqueda, limite = 0):
    clf = SentimentClassifier()
    if solo_busqueda == False:
        dAño, dMes, dDia = desde.split('/')
        hAño, hMes, hDia = hasta.split('/')

        inicio = date(int(dAño), int(dMes), int(dDia))
        final = date(int(hAño), int(hMes), int(hDia))
        delta = timedelta(days=1)

        total = 1000 #limite (hay que establecer un mínimo o se demoraría demasiado)

        diasTotales = final - inicio
        if diasTotales.days > 190:
            print("diasTotales("+diasTotales+") > 190")
            return 0

        if diasTotales.days > 50:
            intervalo = (diasTotales.days-50)/44.33            
        else:
            intervalo = 0

        limite = (total*(intervalo+1)/diasTotales.days)*1000
        deltaIntervalo = timedelta(days=round(intervalo))
        actual = inicio

        print("limite: "+str(limite)+"| deltaIntervalo: "+str(deltaIntervalo))

        while actual < final:
            busqueda_por_fecha2(termino, actual, actual + delta, hastaFinal, True, limite)
            actual += deltaIntervalo + delta
        
        if actual == final:
            actual -= delta
            busqueda_por_fecha2(termino, actual, actual + delta, hastaFinal, True, limite)
        
    elif solo_busqueda == True:

        asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())
        c = twint.Config()
        c.Search = termino
        c.Lang = 'es'
        c.Popular_tweets = True
        c.Limit = limite

        c.Store_csv = True
        c.Output = "tweets_fecha.csv"
        
        c.Until = str(hasta)
        c.Since = str(desde)

        sys.stdout = open(os.devnull, "w") 
        twint.run.Search(c)
        sys.stdout = sys.__stdout__

        print(str(desde)+" > "+str(hasta))
        return 0
    
    tweetsFecha = pd.read_csv("tweets_fecha.csv", sep=',', usecols=['tweet'], squeeze=True)
    listaTFecha = tweetsFecha.values

    Fechas = pd.read_csv("tweets_fecha.csv", sep=',', usecols=['date'], squeeze=True)
    listaFechas = Fechas.values



    data = pd.read_csv("tweets_fecha.csv", sep=',',
                       usecols=['id', 'username', 'name', 'link', 'tweet', 'likes_count', 'date'], squeeze=True).values

    data_dicc = []
    data_dicc_neg = []
    data_dicc_pos = []
    data_dicc_neu = []

    text_ant = 'asd'
    i = 0
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
            polaridad = clf.predict(tweetsFecha[i])
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

    data_dicc = sorted(data_dicc, key=lambda i: i['like'], reverse=True)
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


    os.remove('tweets_fecha.csv')
    print(str(len(listaTFecha))+" tweets ")
    return [listaTFecha, listaFechas, data , data_neg, data_neu, data_pos]
