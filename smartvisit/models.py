# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
categories_choices = (('monument','monument'),('nature','nature'),('art','art'),('quartier','quartier'),('insolite','insolite'),('restaurant','restaurant')) 

#Définition du modèle de données Places qui contiendra les différents lieux à visiter
class Places(models.Model):
    adresse = models.CharField(max_length=100)             #addresse
    ville = models.CharField(max_length=100)                #ville
    categorie = models.CharField(max_length=15, choices=categories_choices)     
    latitude = models.FloatField()      #latitude
    longitude =  models.FloatField()
    score = models.IntegerField()
    description = models.CharField(max_length=1000)
    wikipedia = models.CharField(max_length=300)
    photo = models.CharField(max_length=300)
    
    def __str__(self):

        return self.adresse