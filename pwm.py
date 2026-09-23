"""
CONCEPT : PWM (Pulse Width Modulation)

OBJECTIF : Simuler une intensite analogique (luminosite d'une LED) avec
           un signal numerique (le Raspberry Pi n'a pas d'ADC/DAC integre).

MOTS-CLES :
- Duty cycle (rapport cyclique) : % du temps ou le signal est a HIGH
  pendant une periode. 100% = pleine puissance, 0% = eteint.
  Exemple vu en classe : 25% sur une periode de 20ms -> HIGH pendant
  5ms, LOW pendant 15ms (20ms x 0.25 = 5ms).
- Frequence : nombre de cycles HIGH/LOW par seconde (ici 1000 Hz).
  Assez rapide pour que l'oeil percoive une luminosite continue,
  pas un clignotement.
- PWMOutputDevice.value va de 0.0 (0%) a 1.0 (100%) dans gpiozero.
- Utilisations typiques : luminosite LED, vitesse moteur DC,
  position d'un servomoteur (ou c'est la largeur de l'impulsion,
  pas juste le %, qui compte).
"""
 
# from gpiozero import PWMOutputDevice
# import time
from gpiozero.pins.mock import MockFactory, MockPWMPin
from gpiozero import Device

Device.pin_factory = MockFactory(pin_class=MockPWMPin)

from gpiozero import PWMOutputDevice
import time

led = PWMOutputDevice(18, frequency=1000)  # 1000 Hz


def set_luminosite(pourcentage):
    """pourcentage : 0 a 100. Convertit en duty cycle (0.0 a 1.0) pour gpiozero."""
    if not 0 <= pourcentage <= 100:
        raise ValueError("Le pourcentage doit etre entre 0 et 100")
    led.value = pourcentage / 100  # duty cycle


def fondu_progressif():
    """Fait varier la luminosite de 0% a 100% puis retour a 0%."""
    for pct in range(0, 101, 5):
        set_luminosite(pct)
        time.sleep(0.05)
    for pct in range(100, -1, -5):
        set_luminosite(pct)
        time.sleep(0.05)


if __name__ == "__main__":
    try:
        # Exemple vu en classe : 25% de luminosite sur 20ms de periode
        # -> duty cycle 0.25 -> HIGH pendant 5ms, LOW pendant 15ms
        set_luminosite(25)
        time.sleep(2)
        fondu_progressif()
    finally:
        led.close()