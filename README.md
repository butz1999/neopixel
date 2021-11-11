# neopixel
Kolaborative Umgebung für die Feasibility Studie von Andi.

# Rhaspberry-Pi vorbereiten
* Rhaspi Image herunter laden.
* https://learn.adafruit.com/adafruit-neopixel-uberguide
* Python3 installieren: `sudo apt install python3`
* GIT installieren: `sudo apt install git`
* Hostname setzen: `sudo nano /etc/hostname`
* Dynamisches DHCP in fixe IP: https://www.elektronik-kompendium.de/sites/raspberry-pi/1912151.htm
* DHCP deaktivieren: `sudo service dhcpcd stop`
* Netz neu starten: `sudo service networking restart` oder Raspi neu starten: `sudo reboot`

# HSE Settings
* Zeitserver: `sudo apt install ntp`
* Service Stoppen: `sudo service ntp stop`
* Konfig editieren: `sudo nano /etc/ntp.conf`
* Zeitserver hinzufügen: `timeserver 172.16.0.1`
* Testen: `sudo ntpd -gq`
* Starten: `sudo service ntp start` oder `reboot`

# PC
* Windows installieren. 
* Statische IP setzen.
* Chromium installieren: <link fehlt>
* Microsoft xy installieren: <link fehlt>

# Adafruit
* Tutorial von Adafruit: https://learn.adafruit.com/adafruit-neopixel-uberguide
* Adafruit CircuitPython Essentials: https://learn.adafruit.com/circuitpython-essentials
* Speziell Board aufsetzen: https://learn.adafruit.com/adafruit-neopixel-uberguide/python-circuitpython
* Neopixel Library installieren: `sudo pip3 install adafruit-circuitpython-neopixel`
* CircuitPython: https://circuitpython.readthedocs.io/en/latest/docs/index.html
* CircuitPython Neopixel: https://circuitpython.readthedocs.io/projects/neopixel/en/latest/index.html
* CircuitPython DigitalIO: https://circuitpython.readthedocs.io/en/7.0.x/shared-bindings/digitalio/index.html#digitalio.DigitalInOut
* CircuitPython Library: https://learn.adafruit.com/circuitpython-led-animations (nicht sicher, ob das für's Rhaspi ist...)

# Webserver
* Python doku: https://docs.python.org/3/library/http.server.html#module-http.server
* Beispiel: https://pythonbasics.org/webserver/
* Webserver mit Handler Instanz: https://stackoverflow.com/questions/18444395/basehttprequesthandler-with-custom-instance

# Serial communication
* Adafruit doku: https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/uart-serial

# Kommunikation
* ZMQ: https://zeromq.org/languages/python/
* ZMQ installieren: `sudo pip3 install pyzmq`

# Autostart
* Start als Service: https://raspberrypi.stackexchange.com/questions/4123/running-a-python-script-at-startup

# Multithreading
* Beispiel: https://www.tutorialspoint.com/python/python_multithreading.htm
* Repetitive Timer: https://stackoverflow.com/questions/12435211/python-threading-timer-repeat-function-every-n-seconds

# Verdrahtung
* Rhaspi mit Neopixel: https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring
* Detail gross: https://learn.adafruit.com/assets/64121
* Raspi Pinout: https://learn.sparkfun.com/tutorials/raspberry-gpio/gpio-pinout
* BoxTec Level Konverter: https://shop.boxtec.ch/logic-level-converter-directional-p-41728.html
