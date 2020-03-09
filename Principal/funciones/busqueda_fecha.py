import twint
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
import asyncio
import sys
import os
import pandas as pd
from datetime import date, timedelta

import numpy as np
import numpy.random
import matplotlib.pyplot as plt


def busqueda_por_fecha(termino, desde, hasta, hastaFinal, solo_busqueda, limite = 0):
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
            busqueda_por_fecha(termino, actual, actual + delta, hastaFinal, True, limite)
            actual += deltaIntervalo + delta
        
        if actual == final:
            actual -= delta
            busqueda_por_fecha(termino, actual, actual + delta, hastaFinal, True, limite)
        
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

    data = pd.read_csv("tweets_fecha.csv", sep=',', usecols=[ 'username','date','time','tweet','likes_count', 'link'], squeeze=True).values
    # userFechas = pd.read_csv("tweets_fecha.csv", sep=',', usecols=['username'], squeeze=True).values
    # nameFechas = pd.read_csv("tweets_fecha.csv", sep=',', usecols=['name'], squeeze=True).values
    # likesFechas = pd.read_csv("tweets_fecha.csv", sep=',', usecols=['likes_count'], squeeze=True).values

    # data = []
    data_dicc2 = []
    for i in range(len(listaFechas)):
        dicc = {}
        #dicc['name'] = data[i][0]

        dicc['date'] = data[i][0]
        dicc['time'] = data[i][1]
        dicc['username'] = data[i][2]
        dicc['tweet'] = data[i][3]
        dicc['like'] = data[i][4]
        dicc['link'] = data[i][5]




        data_dicc2.append(dicc)

    #deberia ser x like trate mil veces x alguna razon no me lo pesca . al hacerlo por link
    #se ve bn el sort por like D:
    data_dicc3 = sorted(data_dicc2, key=lambda i: i['like'], reverse=True)
    data = data_dicc3
    data = data[0:30]
    
    


    os.remove('tweets_fecha.csv')
    print(str(len(listaTFecha))+" tweets ")
    return [listaTFecha, listaFechas, data]


def crearMatriz(listaSentimentFecha, listaFechasTotales):
    matriz = []
    fila = []
    cont = 0
    largo = len(listaSentimentFecha)
    listaPolaridadFecha = list(zip(*listaSentimentFecha))[0]
    cantDeDivisiones = 60
    fechasColumna = []

    for valor, fecha in zip(listaPolaridadFecha, listaFechasTotales):
        if cont < round(largo/cantDeDivisiones):
            cont += 1
            fila.append(valor)
        else:
            fechasColumna.append(fecha)
            matriz.append(fila)
            cont = 0
            fila = []

    for i in matriz:
        i.sort()
    return [matriz, fechasColumna]


def procesarMatriz(matriz):
    negativoHasta = 0.4
    neutroHasta = 0.6

    largo_matriz = len(matriz)
    alto_matriz = len(matriz[0])

    abscisas = list(range(largo_matriz))

    matriz_positivos = []; lista_positivos = []
    matriz_positivos.append(abscisas)
    matriz_neutros = []; lista_neutros = []
    matriz_neutros.append(abscisas)

    for fila in matriz:

        porcentaje_neutro = 0
        porcentaje_positivo = 0

        for row in fila:
            if row > neutroHasta:
                porcentaje_positivo += 1
            elif row < neutroHasta and row > negativoHasta:
                porcentaje_neutro += 1

        porcentaje_neutro = (porcentaje_neutro*100)/alto_matriz
        porcentaje_positivo = (porcentaje_positivo*100)/alto_matriz

        lista_positivos.append(porcentaje_positivo)
        lista_neutros.append(porcentaje_neutro + porcentaje_positivo)
        
    matriz_positivos.append(lista_positivos)
    matriz_neutros.append(lista_neutros)
    matriz_procesada = [matriz_positivos, matriz_neutros]
    return matriz_procesada

def crearGrafico(listaSentimentFecha, listaFechasTotales):
    print("inicio crearGrafico")
    matriz, fechasColumna = crearMatriz(listaSentimentFecha, listaFechasTotales)
    rotatedMatriz = list(zip(*reversed(matriz))) # se rota para que quede en un sentido correcto
    plt.imshow(rotatedMatriz, cmap='viridis', interpolation='nearest', aspect='auto')
    plt.savefig('media/heatmap.jpg')
    plt.clf()

    # matriz_positivos, matriz_neutros = procesarMatriz(matriz)
    # plt.plot(matriz_positivos[0], matriz_positivos[1], '-ok',  color="red")
    # plt.plot(matriz_neutros[0], matriz_neutros[1], '-ok',  color="blue")
    # plt.xticks(matriz_positivos[0], fechasColumna, rotation='vertical')
    # plt.savefig('media/test.jpg')
    



    print("fin crearGrafico")