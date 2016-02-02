# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from smartvisit.models import Places #importe le modèle de données Places dans la gestion administrateur

admin.site.register(Places) #enregistre le modèle Places dans la gestion admin
