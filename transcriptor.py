import ledserver
import webserver
import blinkled
import serialM4

import time
import logging
from logging.handlers	import RotatingFileHandler
from threading			import Thread
from queue				import Queue

cmdQueue = Queue()

logfile = '/home/pi/git/neopixel/neopixel.log'

logging.basicConfig(
	filename=logfile, 
	level=logging.DEBUG,
	format='%(asctime)s %(levelname)s %(message)s', 
	datefmt='%Y-%m-%d %H:%M:%S')

log = logging.getLogger("transcriptor")

handler = RotatingFileHandler(logfile, maxBytes=5*1024*1024, backupCount=10)
log.addHandler(handler)


log.info("--------------------")
log.info("Transcriptor started")
log.info("--------------------")

log.info("Starting Serial M4 communication")
ser = serialM4.serialM4()
serThread = Thread(target = ser.run)
serThread.start()

log.info("Starting Blinker")
blink = blinkled.Blinker(ser)
blinkThread = Thread(target = blink.run)
blinkThread.start()

log.info("Starting LedServer")
led = ledserver.LedServer(cmdQueue, blink)
ledThread = Thread(target = led.start)
ledThread.start()

log.info("Starting WebServer")
web = webserver.webServer(cmdQueue)
webThread = Thread(target = web.run)
webThread.start()

log.info("Place initial comand to start idle mode")
cmdQueue.put("/led/idle")

log.info("Transcriptor successfully started")
while True:
	time.sleep(1)
