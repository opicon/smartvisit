# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 00:42:25 2016

@author: Théo
"""

from django.conf.urls import url
from . import views


#Route des différents url du module smartvisit qui renvoient les vues associées
urlpatterns = [
    url(r'^home$', views.home),  #Faire une requête
    url(r'^request$', views.request_user),  #Faire une requête
    url(r'^post$', views.post),  #Faire une requête
]