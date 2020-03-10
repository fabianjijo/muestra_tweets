from django.conf.urls import url, include
from Principal.views import PagPrincipal
from django.urls import path


urlpatterns = [
    url(r"^$", PagPrincipal.as_view(), name='principal'),
]
