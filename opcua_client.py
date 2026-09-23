"""
CONCEPT : OPC UA - CLIENT

OBJECTIF : Se connecter directement au serveur, lire/ecrire une variable,
           et s'y abonner (Monitored Item) pour n'etre notifie qu'au
           changement -- sans faire de polling.

MOTS-CLES :
- Read  : lecture PONCTUELLE de la valeur actuelle d'un noeud.
- Write : modification de la valeur d'une variable (si writable).
- Browse : explorer la structure du graphe pour decouvrir ce qui existe.
- Subscribe / Monitored Item (CreateMonitoredItems) : le client est
  notifie automatiquement SEULEMENT quand la valeur change, avec
  possibilite d'un seuil (deadband) -- plus fin que MQTT ou chaque
  publication declenche toujours une notification.
- NodeId : ns=<namespace>;i=<identifiant> -- ex "2:Temperature" ici
  fait reference au namespace 2 defini par le serveur.
"""

from opcua import Client
import time

client = Client("opc.tcp://localhost:4840/examen/serveur/")
client.connect()

try:
    # BROWSE : ici on connait deja le chemin ("Capteur1" -> "Temperature"),
    # mais dans un cas reel on pourrait explorer server.nodes.objects.get_children()
    objets = client.nodes.objects
    capteur1 = objets.get_child(["2:Capteur1"])
    temperature = capteur1.get_child(["2:Temperature"])

    # READ : lecture ponctuelle
    print("Lecture directe :", temperature.get_value())

    # WRITE : modification directe de la valeur (si set_writable() cote serveur)
    temperature.set_value(21.5)
    print("Nouvelle valeur ecrite :", temperature.get_value())

    # SUBSCRIBE / MONITORED ITEM : notifie seulement si la valeur change
    class Handler:
        def datachange_notification(self, node, val, data):
            print("Changement detecte ->", val)

    sub = client.create_subscription(500, Handler())  # verifie toutes les 500ms
    sub.subscribe_data_change(temperature)

    time.sleep(10)  # ecoute les changements pendant 10 secondes
finally:
    client.disconnect()