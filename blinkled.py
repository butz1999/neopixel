import board
import digitalio
import logging
from threading import Timer
from time import sleep

#log = logging.getLogger("blinkled")

class Blinker():
	def __init__(self, ser):
		#log.info("BlinkLED constructor called")
		self.ser = ser
		self.state = False
		# GPIO
		self.led  = digitalio.DigitalInOut(board.D17)
		self.lock1 = digitalio.DigitalInOut(board.D22)
		self.lock2 = digitalio.DigitalInOut(board.D23)
		self.drawer1 = digitalio.DigitalInOut(board.D24)
		self.drawer2 = digitalio.DigitalInOut(board.D25)
		self.led.direction  = digitalio.Direction.OUTPUT
		self.lock1.direction = digitalio.Direction.OUTPUT
		self.lock2.direction = digitalio.Direction.OUTPUT
		self.drawer1.direction = digitalio.Direction.OUTPUT
		self.drawer2.direction = digitalio.Direction.OUTPUT
		#Timer to stop activity
		self.lockTimeout = 0.5
		self.drawerTimeout = 4
		
	def run(self):
		#log.info("blink: blink task started")
		while True:
			self.state = not self.state
			self.led.value = self.state
			sleep(0.5)

	# Low level funktionen
	def setLock1(self, value):
		#log.info("blink: setLock1")
		self.lock1.value = value

	def setLock2(self, value):
		#log.info("blink: setLock")
		self.lock2.value = value

	def setDrawer1(self, value):
		#log.info("blink: setDrawer1")
		self.drawer1.value = value

	def setDrawer2(self, value):
		#log.info("blink: setDrawer2")
		self.drawer2.value = value

	def lockOff(self):
		#log.info("blink: lockOff()")
		self.setLock1(False)
		self.setLock2(False)

	# High level funktionen
	def drawerOut(self):
		self.ser.open()
		self.setDrawer1(False)
		self.setDrawer2(True)
		self.drawerTimer = Timer(self.drawerTimeout, self.drawerOff)
		self.drawerTimer.start()

	def drawerIn(self):
		self.ser.close()
		self.setDrawer2(False)
		self.setDrawer1(True)
		self.drawerTimer = Timer(self.drawerTimeout, self.drawerOff)
		self.drawerTimer.start()

	def drawerOff(self):
		self.ser.stop()
		self.setDrawer1(False)
		self.setDrawer2(False)

	def reagentOff(self):
		self.setLock1(False)
		
	def reagentRelease(self):
		self.ser.reagent()
		self.setLock1(True)
		self.reagentTimer = Timer(self.lockTimeout, self.lockOff)
		self.reagentTimer.start()
		
	def wasteOff(self):
		self.setLock2(False)
		
	def wasteRelease(self):
		self.ser.waste()
		self.setLock2(True)
		self.wasteTimer = Timer(self.lockTimeout, self.lockOff)
		self.wasteTimer.start()
	
