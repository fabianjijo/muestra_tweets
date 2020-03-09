from django.shortcuts import render
from django.views import View
from datetime import datetime

from .funciones.busqueda import busqueda
from .funciones.polaridad import Polaridad, PorcentajesPolaridad
from .funciones.wordcloud import Wordcloud
from .funciones.busqueda_fecha import busqueda_por_fecha, crearGrafico
import time

from django.http import JsonResponse

class PagPrincipal(View):

    template_name = 'pagPrincipal.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        termino = request.POST.get('busqueda')
        if termino == '':
            return render(request, 'pagPrincipal.html')
        desde = request.POST.get('desde_submit')
        hasta = request.POST.get('hasta_submit')

        start_time = time.time()

        busqueda_fecha = 'off'
        if desde != '' and   desde != '':
            busqueda_fecha = 'on'

        if busqueda_fecha == 'off':
            listaT, data = busqueda(termino)        
            listaSentiment = Polaridad(listaT, True) #lista de tuplas, cada tupla contiene el valor de la polaridad y el tweet
            listaPorcentajes, tweetsPositivos, tweetsNegativos, tweetsNeutross  = PorcentajesPolaridad(listaSentiment, listaT, termino, True)
            PorcentajeNegativos, PorcentajeNeutros, PorcentajePositivos = listaPorcentajes               
            print("--Tiempo total: %s segundos--" % (time.time() - start_time))

            #¿filtrar en el front?
            negativa=False;neutra=False;positiva=False
            if 'checks' in request.POST:
                checks = request.POST.get('checks')
                if 'negativa' in checks:
                    negativa = True
                if 'neutra' in checks:
                    neutra = True
                if 'positiva' in checks:
                    positiva = True    

            context = {'cantidad':len(listaT), 'termino':termino, 'PorcentajeNegativos':PorcentajeNegativos, 'PorcentajeNeutros':PorcentajeNeutros, 
                'PorcentajePositivos':PorcentajePositivos, 'busqueda_fecha':busqueda_fecha, 'data':data,
                'tweetsPositivos':tweetsPositivos, 'tweetsNegativos':tweetsNegativos, 'tweetsNeutross':tweetsNeutross
            }
            return render(request, 'pagPrincipal.html', context)

        elif busqueda_fecha == 'on':
            #Búsqueda con rango de fecha, maximo 6 meses de rango
            listaTFecha, listaFechas, data =  busqueda_por_fecha(termino, desde, hasta, hasta, False)
            listaSentimentFecha = Polaridad(listaTFecha, False)
            crearGrafico(listaSentimentFecha, listaFechas)
            
            context = {'termino': termino, 'desde': desde, 'hasta': hasta, 'busqueda_fecha': busqueda_fecha, 'data':data}
            return render(request, 'pagPrincipal.html', context)

        print("--Tiempo total: %s segundos--" % (time.time() - start_time))
        
        
        context = {'termino': termino, 'lista': lista}
        return render(request, self.template_name, context)

