"""
CONCEPT : OPC UA - SERVEUR

OBJECTIF : Exposer une variable (temperature) dans l'espace d'adressage,
           organisee dans un Object node, lisible et modifiable par un client.

MOTS-CLES :
- Modele CLIENT-SERVEUR direct (PAS de broker comme MQTT) : le client se
  connecte directement a l'IP/port du serveur.
- Espace d'adressage (address space) : graphe hierarchique de noeuds.
    * Variable node : contient une valeur mesurable (ex: Temperature)
    * Object node    : regroupement logique (comme une instance de classe)
    * Method node    : action declenchable a distance (ex: Redemarrer)
    * ObjectType      : le "modele/gabarit" (comme une classe) -- un
      Object est une INSTANCE concrete d'un ObjectType.
- NodeId = namespace (ns, evite les conflits entre fabricants) +
  identifiant (i, le numero du noeud dans ce namespace). Ex: ns=2;i=2.
- Browse : un client peut explorer la structure sans documentation
  externe -> OPC UA est "auto-descriptif".
- Securite integree nativement (certificats X.509, modes None / Sign /
  SignAndEncrypt) -- contrairement a MQTT ou le TLS est ajoute en couche.
- Utilise typiquement dans l'automatisation industrielle (automates,
  usines) car interoperable entre fabricants differents.
"""

from opcua import Server
import time
import random

server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840/examen/serveur/")

# namespace : evite les conflits de noms entre differents fabricants/systemes
uri = "http://examen.cours.iot"
idx = server.register_namespace(uri)

# Object node : regroupement logique (l'equivalent d'une instance de classe)
objet_capteur = server.nodes.objects.add_object(idx, "Capteur1")

# Variable node : contient une valeur mesurable
var_temperature = objet_capteur.add_variable(idx, "Temperature", 20.0)
var_temperature.set_writable()  # permet au client de faire un Write

server.start()
print("Serveur OPC UA demarre sur opc.tcp://0.0.0.0:4840/examen/serveur/")

try:
    while True:
        nouvelle_valeur = round(random.uniform(18.0, 25.0), 1)
        var_temperature.set_value(nouvelle_valeur)
        time.sleep(2)
except KeyboardInterrupt:
    server.stop()