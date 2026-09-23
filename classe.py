"""
CONCEPT : Programmation orientee objet en Python

OBJECTIF : Modeliser des capteurs avec classes, heritage, encapsulation
           et polymorphisme -- typique d'une question "creation de
           classe" a l'examen.

MOTS-CLES :
- Classe vs instance (objet) : Capteur est le modele, CapteurTemperature()
  est une instance concrete -- meme logique qu'ObjectType/Object en OPC UA.
- __init__ : constructeur, appele automatiquement a la creation.
- Encapsulation : self._valeur (underscore = "protege" par convention,
  pas d'acces direct recommande depuis l'exterieur).
- @property : expose _valeur en lecture via .valeur sans methode getter().
- Heritage : CapteurTemperature(Capteur) reutilise le code de la classe
  de base (super().__init__()).
- Polymorphisme : chaque sous-classe redefinit lire() a sa maniere,
  mais on peut appeler capteur.lire() de la meme facon peu importe le type.
"""


class Capteur:
    """Classe de base pour tout capteur."""

    def __init__(self, nom, unite):
        self.nom = nom
        self.unite = unite
        self._valeur = None  # attribut "protege" par convention

    @property
    def valeur(self):
        return self._valeur

    def lire(self):
        """A surcharger dans les sous-classes (polymorphisme)."""
        raise NotImplementedError("A implementer dans la sous-classe")

    def __str__(self):
        return f"{self.nom} : {self._valeur} {self.unite}"


class CapteurTemperature(Capteur):
    def __init__(self, nom="Temperature"):
        super().__init__(nom, "\u00b0C")

    def lire(self):
        import random
        self._valeur = round(random.uniform(15.0, 30.0), 1)
        return self._valeur


class CapteurHumidite(Capteur):
    def __init__(self, nom="Humidite"):
        super().__init__(nom, "%")

    def lire(self):
        import random
        self._valeur = round(random.uniform(30.0, 90.0), 1)
        return self._valeur


if __name__ == "__main__":
    capteurs = [CapteurTemperature(), CapteurHumidite()]
    for c in capteurs:
        c.lire()
        print(c)  # polymorphisme : chaque capteur sait s'afficher correctement