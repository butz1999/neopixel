import ledserver
import webserver
import blinkled
from threading		import Thread
from queue			import Queue

cmdQueue = Queue()

blink = blinkled.Blinker()
blinkThread = Thread(target = blink.run)
blinkThread.start()

led = ledserver.LedServer(cmdQueue, blink)
ledThread = Thread(target = led.start)
ledThread.start()

web = webserver.webServer(cmdQueue)
webThread = Thread(target = web.run)
webThread.start()

cmdQueue.put("/led/idle")

