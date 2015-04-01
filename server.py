#CONSTANTS
FETCH_RATE = 5
MONITOR_RATE = 15

#IMPORTS
import time
import raspcom
import monitor
#BODY
running = False


def startServer():
	global running
	while True:
		if running:
			data = raspcom.fetchData()
			print "Device is up. Current energy consumption = %f" %data[1]

			raspcom.createEnergyPoint(data, FETCH_RATE)
			monitor.logic(data[1], running)
			time.sleep(FETCH_RATE)
		else:
			print "Device is down"
			data = raspcom.fetchData()
			monitor.logic(data[1], running)
			if not running:
				time.sleep(MONITOR_RATE)




def isRunning():
	return running

def setRunning(state):
	global running
	running = state
	print "Setting device status = %s" % state

startServer()

