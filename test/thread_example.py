from queue import Queue
from threading import Thread
import copy
import time

# A thread that produces data
def webserver(name, outqueue):
	while True:
		# Produce some data
		outqueue.put(copy.deepcopy(time.time()))
		time.sleep(0.9)
		
# A thread that consumes data
def ledhandler(name, inqueue):
	while True:
		# Get some data
		data = inqueue.get()
		# Process the data
		print(name, time.ctime(data))

queue = Queue()
web = Thread(target = webserver, args = ("webserver", queue))
led = Thread(target = ledhandler, args = ("ledhandler", queue))

try:
	web.start()
	led.start()
except:
    print("unable to start threads")
