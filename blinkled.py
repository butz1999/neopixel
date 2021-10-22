import board
import digitalio
from threading import Timer
from time import sleep

class Blinker():
	def __init__(self):
		print("Blinker constructor called")
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
		while True:
			self.state = not self.state
			self.led.value = self.state
			sleep(0.5)

	# Low level funktionen
	def setLock1(self, value):
		self.lock1.value = value

	def setLock2(self, value):
		self.lock2.value = value

	def setDrawer1(self, value):
		self.drawer1.value = value

	def setDrawer2(self, value):
		self.drawer2.value = value

	def lockOff(self):
		self.setLock1(False)
		self.setLock2(False)

	# High level funktionen
	def drawerOut(self):
		self.setDrawer1(False)
		self.setDrawer2(True)
		self.drawerTimer = Timer(self.drawerTimeout, self.drawerOff)
		self.drawerTimer.start()

	def drawerIn(self):
		self.setDrawer2(False)
		self.setDrawer1(True)
		self.drawerTimer = Timer(self.drawerTimeout, self.drawerOff)
		self.drawerTimer.start()

	def drawerOff(self):
		self.setDrawer1(False)
		self.setDrawer2(False)

	def reagentOff(self):
		self.setLock1(False)
		
	def reagentRelease(self):
		self.setLock1(True)
		self.reagentTimer = Timer(self.lockTimeout, self.lockOff)
		self.reagentTimer.start()
		
	def wasteOff(self):
		self.setLock2(False)
		
	def wasteRelease(self):
		self.setLock2(True)
		self.wasteTimer = Timer(self.lockTimeout, self.lockOff)
		self.wasteTimer.start()
	
