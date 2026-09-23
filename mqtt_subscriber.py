"""
CONCEPT : MQTT - SUBSCRIBER

OBJECTIF : S'abonner a un topic (avec wildcard) et reagir via un
           callback a chaque nouveau message, sans polling.

MOTS-CLES :
- Wildcards :
    "+" remplace UN SEUL niveau     -> maison/+/temperature
    "#" remplace TOUS les niveaux restants -> maison/#
- Callback on_message : fonction appelee AUTOMATIQUEMENT par la
  librairie quand un message arrive sur la connexion TCP deja
  ouverte -- modele event-driven, pas une boucle qui verifie
  activement (polling).
- Le matching topic <-> filtre se fait NIVEAU PAR NIVEAU, pas par
  recherche de texte/regex.
- Publisher et subscriber sont decouples : le publisher ne sait pas
  qui recoit, le subscriber ne sait pas qui a envoye -- tout passe
  par le broker.
"""

import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
PORT = 1883
# wildcard "#" : capte le status ET la temperature, peu importe la suite
TOPIC_FILTER = "examen/capteur/#"


def on_connect(client, userdata, flags, rc):
    print("Connecte au broker, code :", rc)
    client.subscribe(TOPIC_FILTER)


def on_message(client, userdata, msg):
    # callback : appele automatiquement des qu'un message PUBLISH arrive
    print(f"[{msg.topic}] {msg.payload.decode()}")


client = mqtt.Client(client_id="subscriber_dashboard")
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, keepalive=60)
client.loop_forever()  # boucle bloquante qui ecoute les messages entrants