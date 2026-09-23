# """
# CONCEPT : GPIO (General Purpose Input/Output)

# OBJECTIF : Allumer une LED en sortie, lire un bouton en entrée, et
#            bien gerer le cleanup a la fin du programme.

# MOTS-CLES :
# - DigitalOutputDevice / DigitalInputDevice / Button (gpiozero)
# - HIGH = 3.3V, LOW = 0V (PAS 5V ni 12V -- confusion frequente avec l'Arduino)
# - Numerotation BCM (ex: GPIO17) != numero physique de la broche sur le
#   connecteur 40 pins. gpiozero utilise TOUJOURS le BCM par defaut.
# - Resistance en serie avec la LED : la LED a une resistance interne tres
#   faible -> sans resistance, le courant serait trop eleve (le Pi ne
#   fournit qu'environ 16mA par broche) -> LED grillee ou GPIO endommage.
# - Broche flottante : une entree non connectee capte du bruit electrique
#   et lit des valeurs aleatoires -> on regle ca avec une resistance
#   pull-up ou pull-down qui force un etat connu par defaut.
#     * pull-up   : etat de repos = HIGH, action -> relie a GND -> LOW
#     * pull-down : etat de repos = LOW,  action -> relie a 3.3V -> HIGH
#   gpiozero configure un pull-up interne par defaut sur Button().
# - Cleanup : le GPIO est un registre materiel reel, pas juste une
#   variable Python. Sans cleanup, l'etat/la configuration reste actif
#   apres la fin du script -> erreurs "GPIO already in use" au prochain
#   lancement, ou etat electrique laisse actif par erreur.
#   En ajoutant ces deux lignes avant l'import, 
#   gpiozero simule les broches en mémoire — ça te permet de 
#   vérifier que ton code (logique, syntaxe, appels de méthodes) fonctionne, 
#   sans crasher sur du matériel manquant. Bien sûr, tu ne verras pas de vraie 
#   LED s'allumer, mais tu verras que le code s'exécute sans erreur 
#   et tu peux même imprimer l'état (led.value) pour vérifier.

# Pour l'examen : si tu utilises réellement ton Raspberry 
# Pi (comme mentionné dans les specs), ce problème ne se posera pas — 
# le vrai matériel sera là. Ce mode mock est juste pour tester/pratiquer 
# sur ton PC avant.
# """
# import os
# os.environ['GPIOZERO_PIN_FACTORY'] = 'mock'

# from gpiozero import DigitalOutputDevice, Button


# import time

# # --- SORTIE : controler une LED ---
# # GPIO 17 (numerotation BCM), relie a une LED via une resistance (ex. 220-330 ohms)
# led = DigitalOutputDevice(17)

# # --- ENTREE : lire un bouton ---
# # Button() gere le pull-up interne automatiquement et inverse la logique :
# # bouton.is_pressed == True quand le bouton est reellement appuye
# bouton = Button(27)


# def clignoter(led_obj, nb_fois=5, delai=0.5):
#     """Fait clignoter la LED nb_fois, avec delai secondes entre chaque etat."""
#     for _ in range(nb_fois):
#         led_obj.on()   # GPIO -> HIGH (3.3V) : le courant circule, la LED s'allume
#         time.sleep(delai)
#         led_obj.off()  # GPIO -> LOW (0V)
#         time.sleep(delai)


# import time

# def surveiller_bouton():
#     """
#     Boucle event-driven (pas de polling) : gpiozero appelle automatiquement
#     when_pressed / when_released quand l'etat electrique change, plutot
#     que de verifier .is_pressed en boucle active.
#     """
#     bouton.when_pressed = led.on
#     bouton.when_released = led.off
#     print("En attente d'appuis sur le bouton (Ctrl+C pour arreter)...")
    
#     while True:
#         time.sleep(0.1)  # boucle qui garde le programme actif, verifie 10x/seconde


# if __name__ == "__main__":
#     try:
#         clignoter(led)
#         surveiller_bouton()
#     except KeyboardInterrupt:
#         print("Arret du programme.")
#     finally:
#         # CLEANUP : libere les GPIO pour eviter les conflits au prochain lancement
#         led.close()
#         bouton.close()

from gpiozero import DigitalOutputDevice, Button
import time
import os

os.environ['GPIOZERO_PIN_FACTORY'] = 'mock'

led = DigitalOutputDevice(17)
bouton = Button(27)

def clignoter(led_obj, nb_fois=5, delai=0.5):
    for _ in range(nb_fois):
        led_obj.on()
        print("LED -> ON")
        time.sleep(delai)
        led_obj.off()
        print("LED -> OFF")
        time.sleep(delai)

def surveiller_bouton():
    bouton.when_pressed = lambda: print("Bouton appuye -> LED ON") or led.on()
    bouton.when_released = lambda: print("Bouton relache -> LED OFF") or led.off()
    print("En attente d'appuis sur le bouton...")

if __name__ == "__main__":
    try:
        clignoter(led, nb_fois=2)
        surveiller_bouton()

        # --- SIMULATION D'UN APPUI (uniquement possible en mode mock) ---
        print("\n--- Simulation d'un appui sur le bouton ---")
        bouton.pin.drive_low()    # simule : bouton appuye (relie a GND -> LOW)
        time.sleep(1)
        bouton.pin.drive_high()   # simule : bouton relache (retour a HIGH via pull-up)
        time.sleep(1)

    except KeyboardInterrupt:
        print("Arret du programme.")
    finally:
        led.close()
        bouton.close()