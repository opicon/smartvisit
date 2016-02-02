APPLICATION SMART-VISIT
=======================

-------------------------
PRINCIPE DE L'APPLICATION
-------------------------

Itinéraire intelligent : 
Étant donnés une adresse de départ, une adresse d'arrivée, une durée imposée, un mode de transport, un choix de catégorie de lieux à visiter, l'application calcule un itinéraire prenant les adresses de départ et d'arrivée pour extrémités, et passant par un maximum de lieux de la catégorie imposée dans la durée impartie.
Le programme fait appel aux APIs de GoogleMaps et comporte un algorithme d'optimisation de l'itinéraire (calcul des points de passage).

----------------
CONTENU DETAILLE
----------------

Répertoire DEV (conteneur d'un projet Django)

- db.sqlite3 :			base de données
- manage.py :			utilitaire en ligne de commande pour interagir avec le projet Django
- smart_visit :			web server gateway interface (passerelle entre serveurs)
- smartvisit
	- __init__.py
	- admin.py :			gestion du compte administrateur
	- algos_gmaps.py :		algorithmes de calcul et d'optimisation d'un trajet
	- forms.py :			définit la forme d'une requête d'itinéraire
	- migrations/ :			traitement des modifications apportées de l'extérieur
	- models.py :			définit le modèle de données qui contiendra les lieux à visiter
	- templates/ : 			requêtes possibles (html)
	- tests.py :			tests unitaires
	- urls.py :				urls du modèle smartvisit
	- views.py :			traitement des requêtes
- static :				maquette de l'application
- templates :			page d'accueil (html)

------------------------
A INSTALLER AU PREALABLE
------------------------

- Python (version 3.0 ou supérieure)
- Bibliothèques django et googlemaps

--------------------------
LANCEMENT DE L'APPLICATION
--------------------------

Se placer dans le répertoire DEV et créer les adresses en écrivant la ligne de commande : python3 manage.py runserver	
Taper l'URL http://127.0.0.1:8000/home



