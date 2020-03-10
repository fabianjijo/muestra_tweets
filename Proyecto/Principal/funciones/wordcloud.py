from cucco import Cucco
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np

#from PIL import Image
#from IPython import get_ipython
#from os import path
#from .rutas import *
#from nltk.tag.stanford import StanfordNERTagger
#import operator
#import seaborn as sns
#from scipy import stats
#from stanfordcorenlp import StanfordCoreNLP
#import statistics
#import time


#Crea una imagen de Wordcloud
def Wordcloud(listaTexto, nombreArchivo, termino):
    #Normalizar el texto
    cucco = Cucco()
    text_tweets = ''
    for x in listaTexto:
        text_tweets += cucco.normalize(str(x)) + ' '

    stopwords_spa = stopwords.words('spanish')
        
    #Tokenizar tweets
    tokenized_words_tweets = word_tokenize(text_tweets)


    words_tweets = [word.lower() for word in tokenized_words_tweets if (len(word)>3 and word.lower() != termino.lower() and word.lower() not in termino.lower())]
    texto_words_tweets = [word for word in words_tweets if word not in stopwords_spa]
    
    
    '''#NER
        
    java_path = JavaPath()
    os.environ['JAVAHOME'] = java_path

    _model_filename = ModelPath()
    _path_to_jar = JarPath()
    st = StanfordNERTagger(model_filename=_model_filename, path_to_jar=_path_to_jar)

    classified_text_tweets= st.tag(texto_words_tweets)

    dict_tweets = dict()
    for element in classified_text_tweets:
        if(element[1]!='O'):
            if(element[0] in dict_tweets):
                dict_tweets[element[0]]+=1
            else:
                dict_tweets[element[0]]=1
    sorted(dict_tweets.items(),key=operator.itemgetter(1),reverse=True)[0:10]'''
    
  
    wordcloud = WordCloud(max_font_size=50, max_words=200, background_color="white").generate(str(texto_words_tweets).replace("'",""))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('media/'+nombreArchivo+'.jpg')
    plt.close()