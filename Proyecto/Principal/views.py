from django.shortcuts import render
from django.views import View
from datetime import datetime

from .funciones.busqueda import busqueda
from .funciones.busqueda2 import busqueda2
from .funciones.busqueda_fecha2 import busqueda_por_fecha2
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


       # muestreo= 'on'
        #print("----")
        #muestreo = request.POST.get('completed', '')
        #print("----")
        muestreo = 'on'
        #print(muestreo)

        busqueda_fecha = 'off'
        if desde != '' and desde != '':
            busqueda_fecha = 'on'





        if busqueda_fecha == 'off':
            listaT, data, data_neg, data_neu, data_pos = busqueda2(termino)

            print("--Tiempo total: %s segundos--" % (time.time() - start_time))

            context = {'cantidad':len(listaT), 'termino':termino, 'busqueda_fecha':busqueda_fecha, 'data':data, 'data_neu':data_neu,
                       'data_neg':data_neg, 'data_pos':data_pos
            }
            return render(request, 'pagPrincipal.html', context)

        elif busqueda_fecha == 'on':
            #Búsqueda con rango de fecha, maximo 6 meses de rango
            listaTFecha, listaFechas, data, data_neg, data_neu, data_pos =  busqueda_por_fecha2(termino, desde, hasta, hasta, False)

            context = {'termino': termino, 'desde': desde, 'hasta': hasta, 'busqueda_fecha': busqueda_fecha, 'data':data, 'data_neg':data_neg
            , 'data_neu':data_neu, 'data_pos':data_pos}
            return render(request, 'pagPrincipal.html', context)

        print("--Tiempo total: %s segundos--" % (time.time() - start_time))






        context = {'termino': termino}#, 'lista': lista}
        return render(request, self.template_name, context)




