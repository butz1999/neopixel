from threading import Thread
from time import sleep
from random import *
def func1():
	global i
	while True:
		if i % 2 == 1:
			i = (i*3) +1
			print(1, i)
		if (i==1):
			break;
		sleep(0)
		#for wait in range(1000000):
		#	wait ** 2

def func2():
	global i
	while True:
		if i % 2 == 0:
			i /= 2
			print(2, i)
		if (i==1):
			break;
		sleep(0)
		#for wait in range(1000000):
		#	wait ** 2
	

for i in range(100000):
	t1 = Thread(target = func1)
	t2 = Thread(target = func2)
	t1.start()
	t2.start()
	print(i, "---------------------------")
	i+=1
