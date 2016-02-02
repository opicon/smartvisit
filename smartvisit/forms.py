# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 21:53:24 2016

@author: Théo
"""

from django import forms
from smartvisit.models import Places #on récupère le modèle de création d'endroit pour créer un formulaire dans le modèle

#-------------------------------------------------------------------------------------
#Définir les choix dans les formulaire à choix
#

#définir les choix pour les modes de transports
modes_gmaps = (
    ('walking', 'walking'),                                                                 
    ('driving', 'driving'),
    ('bicycling', 'bicycling'),
    ('transit', 'transit'))

#choix pour la catégorie d'endroit à visiter
categories_choices = (('monument','monument'),('nature','nature'),('art','art'),('quartier','quartier'),('insolite','insolite'),('restaurant','restaurant')) 

#--------------------------------------------------------------------------------------
# Définit le formulaire pour la requête de visite de l'utilisateur
class request_user_form(forms.Form):                                            #Formulaire qui prend la demande d'un utilisateur
    startpoint = forms.CharField(max_length = 300)                              #Point de départ (texte)
    endpoint = forms.CharField(max_length = 300)                                #Point d'arrivée (texte)
    heures = forms.IntegerField(min_value = 0,max_value = 59)                   #Heures de balade (entier)
    minutes = forms.IntegerField(min_value = 0,max_value = 59)                  #Minutes de balade (entier)
    mode = forms.ChoiceField(choices = modes_gmaps,widget = forms.Select())     #Mode de déplacement (choix défini plus tôt)
    category = forms.MultipleChoiceField(choices = categories_choices)
    


# Définit le formulaire à partir du modèle de données des lieux à visiter pour l'ajout d'un nouveau lieu
class new_place_form(forms.ModelForm):                                          #Formulaire d'ajout d'un lieu dans la base de données
    class Meta:
        model = Places                                                          #On récupère le modèle Places
        fields = ('adresse','ville','categorie','description','wikipedia','photo') #On va demander les champs suivants