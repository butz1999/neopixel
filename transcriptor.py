import ledserver
import webserver
import blinkled
import time
import logging
from threading		import Thread
from queue			import Queue

cmdQueue = Queue()

logging.basicConfig(
	filename='/home/pi/git/neopixel/neopixel.log', 
	level=logging.DEBUG,
	format='%(asctime)s %(levelname)s %(message)s', 
	datefmt='%Y-%m-%d %H:%M:%S')

log = logging.getLogger("transcriptor")


log.info("--------------------")
log.info("Transcriptor started")
log.info("--------------------")

log.info("Starting Blinker")
blink = blinkled.Blinker()
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
