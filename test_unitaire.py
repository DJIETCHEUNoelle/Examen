"""
CONCEPT : Tests unitaires

OBJECTIF : Verifier automatiquement que le code (ici la classe Capteur)
           se comporte comme attendu, sans verification manuelle.

MOTS-CLES :
- unittest.TestCase : classe de base a heriter pour ecrire des tests.
- setUp() : execute AVANT chaque test individuel -- prepare un etat propre.
- assertEqual / assertTrue / assertIsNone : verifient qu'une condition
  est vraie ; le test echoue automatiquement si l'assertion est fausse.
- Un test unitaire teste une seule unite de code (une methode, un
  comportement precis) de facon isolee.
"""

# import unittest
# import sys
# import os

# #sys.path.append(os.path.join(os.path.dirname(__file__), "..", "python_oop"))
# from capteurs import CapteurTemperature, CapteurHumidite


# class TestCapteurTemperature(unittest.TestCase):

#     def setUp(self):
#         """Execute avant CHAQUE test : garantit un capteur neuf, sans effet de bord."""
#         self.capteur = CapteurTemperature()

#     def test_valeur_initiale_est_none(self):
#         self.assertIsNone(self.capteur.valeur)

#     def test_lire_retourne_dans_la_plage_attendue(self):
#         valeur = self.capteur.lire()
#         self.assertTrue(15.0 <= valeur <= 30.0)

#     def test_unite_correcte(self):
#         self.assertEqual(self.capteur.unite, "\u00b0C")


# class TestCapteurHumidite(unittest.TestCase):

#     def test_lire_retourne_dans_la_plage_attendue(self):
#         capteur = CapteurHumidite()
#         valeur = capteur.lire()
#         self.assertTrue(30.0 <= valeur <= 90.0)


# if __name__ == "__main__":
#     unittest.main()

import unittest
from classe import CapteurTemperature, CapteurHumidite


class TestCapteurTemperature(unittest.TestCase):

    def setUp(self):
        self.capteur = CapteurTemperature()

    def test_valeur_initiale_est_none(self):
        self.assertIsNone(self.capteur.valeur)

    def test_lire_retourne_dans_la_plage_attendue(self):
        valeur = self.capteur.lire()
        self.assertTrue(15.0 <= valeur <= 30.0)

    def test_unite_correcte(self):
        self.assertEqual(self.capteur.unite, "°C")


class TestCapteurHumidite(unittest.TestCase):

    def test_lire_retourne_dans_la_plage_attendue(self):
        capteur = CapteurHumidite()
        valeur = capteur.lire()
        self.assertTrue(30.0 <= valeur <= 90.0)


if __name__ == "__main__":
    unittest.main()