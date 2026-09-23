
"""
CONCEPT : MQTT - PUBLISHER

OBJECTIF : Publier periodiquement une valeur de capteur simulee sur un
           topic, avec status en ligne/hors ligne via LWT et retain.

MOTS-CLES :
- Broker : serveur central qui recoit tous les messages et les
  redistribue. Publisher et subscriber ne se connectent jamais
  directement l'un a l'autre (modele decouple, contraste avec
  client-serveur direct d'OPC UA).
- Topic : chaine hierarchique separee par "/" (ex: maison/salon/temp).
  C'est une ADRESSE LOGIQUE, pas une donnee en soi.
- Payload : le contenu du message, en bytes bruts (MQTT ne connait
  pas le "type" -- ici on envoie une string representant un nombre).
- QoS (Quality of Service) :
    0 = fire-and-forget, peut se perdre
    1 = garanti d'arriver, peut arriver EN DOUBLE si l'accuse de
        reception se perd
    2 = garanti exactement une fois, plus lent/lourd (poignee de
        main en 4 etapes)
- Retain : le broker garde le DERNIER message publie sur un topic et
  le renvoie immediatement a tout nouveau subscriber, meme s'il
  s'abonne apres l'envoi.
- LWT (Last Will and Testament) : message defini a l'avance dans le
  CONNECT, publie AUTOMATIQUEMENT par le broker si ce client se
  deconnecte de facon ANORMALE (crash, coupure reseau) -- pas une
  deconnexion volontaire.
- Port 1883 = TCP non chiffre, port 8883 = TLS.
- Objectifs de MQTT : LEGER (peu de ressources/bande passante) et
  RESILIENT aux pannes reseau (QoS, LWT, reconnexion).
"""

import paho.mqtt.client as mqtt
import random
import time

BROKER = "test.mosquitto.org"   # broker public de test -- remplacer par celui du cours
PORT = 1883
TOPIC = "examen/capteur/temperature"
TOPIC_STATUS = "examen/capteur/status"

client = mqtt.Client(client_id="publisher_capteur")

# LWT : si ce client crash / perd la connexion sans se deconnecter proprement,
# le broker publiera lui-meme "offline" a notre place
client.will_set(TOPIC_STATUS, payload="offline", qos=1, retain=True)

client.connect(BROKER, PORT, keepalive=60)

# retain=True : un nouveau subscriber qui arrive plus tard saura tout de
# suite qu'on est en ligne, sans attendre notre prochaine publication
client.publish(TOPIC_STATUS, payload="online", qos=1, retain=True)

try:
    while True:
        temperature = round(random.uniform(18.0, 25.0), 1)
        # QoS 1 : ok pour une lecture reguliere, tolere un doublon rare
        client.publish(TOPIC, payload=str(temperature), qos=1)
        print(f"Publie sur {TOPIC} : {temperature}")
        time.sleep(2)
except KeyboardInterrupt:
    # deconnexion PROPRE : le LWT ne se declenche pas ici, donc on publie
    # nous-memes le status offline avant de partir
    client.publish(TOPIC_STATUS, payload="offline", qos=1, retain=True)
    client.disconnect()