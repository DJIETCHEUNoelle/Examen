"""
EXERCICE COMBINE : GPIO (entree/sortie) + POO (classes) + MQTT (publisher)

SCENARIO : un detecteur de mouvement (PIR) en entree declenche une LED
en sortie (alarme locale) ET publie un evenement sur MQTT pour qu'un
appareil distant (ex: sirene, dashboard) puisse reagir.

OBJECTIF : montrer comment combiner plusieurs concepts du cours dans un
seul programme, comme demande a l'examen pratique.

MOTS-CLES COUVERTS :
- GPIO entree (PIR) / sortie (LED) -- HIGH=3.3V, LOW=0V, BCM
- Event-driven (callback when_pressed) vs polling
- POO : classe, encapsulation, methode
- MQTT : qui publie (le detecteur, car il GENERE l'info) vs qui
  s'abonnerait ailleurs (ex: une sirene distante, qui REAGIT)
- Cleanup des GPIO a la fin

Sur Windows/PC (sans vrai Raspberry Pi) : mode mock active pour tester
la logique sans materiel physique.
"""

import os
os.environ['GPIOZERO_PIN_FACTORY'] = 'mock'  # simule les GPIO sur PC

from gpiozero import Button, DigitalOutputDevice
import paho.mqtt.client as mqtt
import time


class DetecteurMouvement:
    """
    Represente un capteur PIR branche en ENTREE.
    ENCAPSULATION : le GPIO reel (self._bouton) est cache derriere
    cette classe -- le reste du programme n'a pas besoin de savoir
    comment gpiozero fonctionne en dessous.
    """

    def __init__(self, pin_bcm):
        # Button() gere le pull-up interne : au repos = HIGH,
        # "detection" (simulee) = LOW
        self._bouton = Button(pin_bcm)

    def sur_detection(self, callback):
        """
        Enregistre un callback event-driven (pas de polling) :
        appele automatiquement par gpiozero quand l'etat change.
        """
        self._bouton.when_pressed = callback

    def simuler_detection(self):
        """Force une detection simulee (utile en mode mock, sans vrai PIR)."""
        self._bouton.pin.drive_low()   # simule : mouvement detecte
        time.sleep(0.2)
        self._bouton.pin.drive_high()  # retour au repos

    def fermer(self):
        self._bouton.close()


class Alarme:
    """
    Represente une LED (ou buzzer) en SORTIE -- reagit a une commande.
    """

    def __init__(self, pin_bcm):
        self._led = DigitalOutputDevice(pin_bcm)

    def activer(self):
        self._led.on()   # GPIO -> HIGH (3.3V)
        print("ALARME : LED allumee")

    def desactiver(self):
        self._led.off()  # GPIO -> LOW (0V)
        print("ALARME : LED eteinte")

    def fermer(self):
        self._led.close()


class PublisherMQTT:
    """
    Encapsule la connexion MQTT et la publication d'un evenement.

    ROLE MQTT ICI : ce systeme est le PUBLISHER -- il GENERE
    l'information (une detection vient de se produire). Un appareil
    distant (ex: sirene, dashboard) jouerait le role de SUBSCRIBER
    en s'abonnant au meme topic pour reagir a son tour.
    """

    def __init__(self, broker, port, topic):
        self.topic = topic
        self.client = mqtt.Client(client_id="detecteur_mouvement")
        self.client.connect(broker, port, keepalive=60)

    def publier_evenement(self, message):
        # QoS 1 : garanti d'arriver, tolere un doublon rare -- suffisant
        # pour une alerte de mouvement (pas besoin du QoS 2 plus lourd)
        self.client.publish(self.topic, payload=message, qos=1)
        print(f"MQTT : publie '{message}' sur {self.topic}")

    def fermer(self):
        self.client.disconnect()


class SystemeSecurite:
    """
    Classe qui ORCHESTRE les trois pieces ci-dessus : c'est ici que
    GPIO, POO et MQTT se combinent dans un seul flux logique.
    """

    def __init__(self, pin_detecteur, pin_alarme, broker, port, topic):
        self.detecteur = DetecteurMouvement(pin_detecteur)
        self.alarme = Alarme(pin_alarme)
        self.mqtt = PublisherMQTT(broker, port, topic)

        # callback : quand le detecteur "capte" un mouvement, on
        # declenche a la fois l'alarme locale ET la publication MQTT
        self.detecteur.sur_detection(self._on_mouvement_detecte)

    def _on_mouvement_detecte(self):
        print("\n--- Mouvement detecte ---")
        self.alarme.activer()
        self.mqtt.publier_evenement("mouvement_detecte")
        time.sleep(1)
        self.alarme.desactiver()

    def tester(self):
        """Simule une detection (mode mock, sans vrai capteur)."""
        self.detecteur.simuler_detection()

    def arreter(self):
        self.detecteur.fermer()
        self.alarme.fermer()
        self.mqtt.fermer()


if __name__ == "__main__":
    systeme = SystemeSecurite(
        pin_detecteur=17,
        pin_alarme=27,
        broker="test.mosquitto.org",
        port=1883,
        topic="examen/securite/mouvement",
    )

    try:
        print("Systeme demarre, simulation d'une detection...")
        systeme.tester()
        time.sleep(2)  # laisse le temps a MQTT de publier avant de fermer
    except KeyboardInterrupt:
        print("Arret demande par l'utilisateur.")
    finally:
        systeme.arreter()  # CLEANUP : GPIO + connexion MQTT