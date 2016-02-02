# -*- coding: utf-8 -*-
from django.test import TestCase

# Create your tests here.
#==============================================================================
'''Bibliothèque de génération aléatoire'''
import random

'''Algo à tester'''
from smartvisit.algos_gmaps import optimization_algo_1

'''2 fonctions nécessaires'''
from smartvisit.algos_gmaps import isInDisk, nodeDistance

'''Liste des points de départ possibles pour les tests'''
test_addresses = ['Barbès-Rochechouart, Paris', 'Denfert-Rochereau, Paris', 'Tuileries, Paris', 'Etoile, Paris', 'Bastille, Paris', 'Nation, Paris']

#==============================================================================
''' Tests relatifs à l'algorithme d'optimisation de l'itinéraire '''
class AlgoTests(TestCase):
    def test_max_score(self):
        '''
        Le premier waypoint (éventuel) est le monument de plus haut score
        '''
        # Choix au hasard de deux monuments de la base de données
        m1 = random.choice(test_addresses)
        m2 = random.choice(test_addresses)

        # Durée requise : nombre aléatoire
        d = random.randint(0, 100000)
        
        # Calcul du trajet
        itinerary = optimization_algo_1(m1, m2,'walking',d,'')
        waypoints = itinerary[0]['waypoints']
        duration = itinerary[0]['duration']
        best_score = 0
            
        # Test : s'i existe au moins un waypoint, alors le premier de la liste est celui de plus haut score
        if(len(waypoints) > 0):
            best_score =  waypoints[0]['score']['total']
            for waypoint in waypoints:
                if waypoint['score']['total'] > best_score:
                    best_score = waypoint['score']
            self.assertTrue(best_score == waypoints[0]['score']['total'])

        # Cas sans interet    
        else:
            self.assertTrue(len(waypoints) == 0)
            
    def test_pas_de_waypoints_pas_d_itineraire(self):
        '''
        S'il n'y a pas de waypoints et que le départ et l'arrivée sont identiques, alors l'itinéraire est vide
        '''
        # Choix au hasard d'un monument dans la base de données
        monument = random.choice(test_addresses)

        # Durée requise : nombre aléatoire
        d = random.randint(0, 100000)
        
        # Calcul du trajet
        itinerary = optimization_algo_1(monument, monument, 'walking',d,'')
        waypoints = itinerary[1]
        duration = itinerary[0]['duration']

        # Test : si pas de waypoints, alors pas d'itinéraire
        if len(waypoints) == 0:
            self.assertTrue(duration == 0)
        else:
            self.assertTrue(duration > 0)
    
    def test_duree_non_depassee(self):
        '''
        La durée imposée ne doit pas être dépassée
        '''
        # Choix au hasard de deux monuments de la base de données
        m1 = random.choice(test_addresses)
        m2 = random.choice(test_addresses)

        # Durée requise : nombre aléatoire
        d = random.randint(0, 100000)
        
        # Calcul du trajet
        itinerary = optimization_algo_1(m1, m2, 'walking',d,'')
        duration = itinerary[0]['duration']
        
        # Test
        self.assertTrue(duration <= d)

#=============================================================================================================
    ''' Répétition des mêmes tests (les monuments sont aléatoires'''
    def test_max_score_COPY(self):
        AlgoTests.test_max_score(self)
    def test_max_score_COPY2(self):
        AlgoTests.test_max_score(self)
    def test_pas_de_waypoints_pas_d_itineraire_COPY(self):
        AlgoTests.test_pas_de_waypoints_pas_d_itineraire(self)
    def test_pas_de_waypoints_pas_d_itineraire_COPY2(self):
        AlgoTests.test_pas_de_waypoints_pas_d_itineraire(self)
    def test_duree_non_depassee_COPY(self):
        AlgoTests.test_duree_non_depassee(self)
    def test_duree_non_depassee_COPY2(self):
        AlgoTests.test_duree_non_depassee(self)
    
