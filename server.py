#CONSTANTS
FETCH_RATE = 5
MONITOR_RATE = 15

#IMPORTS
import thread
import time
import raspcom
import monitor
import api
import environment
#BODY

def startServer():
	global running
	global scheduleId
	print "starting main server"
	running = False
	scheduleId = -1
	
	try:
		thread.start_new_thread(api.startAPIServer, ())
	except:
		print "Couldn't start API thread"
	
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
	if state and not running:
		raspcom.startRecording()
	elif not state and running:
		#do push
		raspcom.stopRecording()
	print "Setting device status = %s" % state
	running = state

def stopDevice():
	global scheduleId
	scheduleId = -1
	raspcom.stopDevice()

def startDeviceWithinTime(time):
        try:
	        thread.start_new_thread(waitingToStart, (time,False,))
        except:
	        print "Couldn't start wait thread"

def startDeviceAtLowestPrice(time):
	data = environment.startAtCheapest(time)
        try:
                thread.start_new_thread(waitingToStart, (data[0],False,))
        except:
                print "Couldn't start wait thread"
	return data

def startDeviceWithWind(time):
        try:
                thread.start_new_thread(waitingToStart, (time,True,))
        except:
                print "Couldn't start wait thread"



def waitingToStart(startTime, useWind):
	global scheduleId
	scheduleId += 1
	scheduleId %= 10
	myId = scheduleId

	currentMillis = int(round(time.time() * 1000))
	print "I'll start within %d seconds" % ((startTime - currentMillis)/1000)
	while (currentMillis < startTime):
		
		if useWind and environment.isWind():
			print "Wind detected! Starting wash."
			break

		time.sleep(1)
		currentMillis = int(round(time.time() * 1000))
		if myId != scheduleId:
			print "Abort schedule #",myId
			return
	raspcom.startDevice()

