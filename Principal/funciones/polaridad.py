import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from classifier import *

from .wordcloud import Wordcloud

def Polaridad(listaTexto, imagen):
    
    print("inicio polaridad >")
    #Indicadores de polaridad
    clf=SentimentClassifier()

    X = []
    #Iterar texto plano A.K.A sin tokenizar
    for r in listaTexto:
        prediccion = clf.predict(r)
        X.append(prediccion)

    print("Termino polaridad >")
    if imagen:
        plt.hist(X, bins=10)
        plt.savefig('media/polaridad.jpg')

    
    plt.close()
    return list(zip(X, listaTexto))


#-----------------------------------------------------------------------------------------------------------
def PorcentajesPolaridad(listaSentiment, listaT, termino, wrdc):
    negativoHasta = 0.4
    neutroHasta = 0.6

    tweetsNegativos = extraer(listaSentiment, 0, negativoHasta)
    tweetsNeutros = extraer(listaSentiment, negativoHasta, neutroHasta)
    tweetsPositivos = extraer(listaSentiment, neutroHasta, 1)

    total = len(listaT)
    negativos = len(tweetsNegativos)
    neutros = len(tweetsNeutros)
    positivos = len(tweetsPositivos)
        
    #si se desea, se crea una imagen de Wordcloud para cada caso
    if wrdc:
        if total != 0:
            Wordcloud(listaT, "wordcloudGeneral", termino)
        if negativos != 0:
            Wordcloud(tweetsNegativos, "tweetsNegativos", termino)
        if neutros != 0:
            Wordcloud(tweetsNeutros, "tweetsNeutros", termino)
        if positivos != 0:
            Wordcloud(tweetsPositivos, "tweetsPositivos", termino)

        

    PorcentajeNegativos = (negativos/total)*100
    PorcentajeNeutros = (neutros/total)*100
    PorcentajePositivos = (positivos/total)*100

    return ([round(PorcentajeNegativos,1),round(PorcentajeNeutros,1),round(PorcentajePositivos,1)], tweetsPositivos, tweetsNegativos, tweetsNeutros)


#-----------------------------------------------------------------------------------------------------------
def extraer(listaDeTuplas, limiteInferior, limiteSuperior):
    listaRetorno = []
    for valor, tweet in listaDeTuplas:
        if valor > limiteInferior and valor < limiteSuperior:
            listaRetorno.append(tweet)
    return listaRetorno