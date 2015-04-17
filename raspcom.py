import urllib2
import json
import time 
import environment
import server

currentTime = lambda: int(round(time.time()*1000))

def startDevice():
	url = "http://192.168.1.5:8083/ZWaveAPI/Run/devices[2].instances[0].SwitchBinary.Set(255)"
	urllib2.urlopen(url).read()
	

def stopDevice():
        url = "http://192.168.1.5:8083/ZWaveAPI/Run/devices[2].instances[0].SwitchBinary.Set(0)"
	urllib2.urlopen(url).read()

#Get's the Live data from RaZBerry
def fetchData():
	url = "http://192.168.1.5:8083/ZWaveAPI/Run/devices[2].instances[0].commandClasses.Meter"
	data = urllib2.urlopen(url).read()

	jdata = json.loads(data)

	currentKwh = jdata["data"]["0"]["val"]["value"]

	currentW = jdata["data"]["2"]["val"]["value"]

	
	return [currentKwh, currentW, currentTime()]


#Creates energypoints
def createEnergyPoint(data, rate):
	global totalEnergy
	totalEnergy += (data[1] * rate)
	global latestEnergy
	latestEnergy = data[1]
	newPoint = {'time':data[2], 'value':data[1]}
	global energypoints
	energypoints.append(newPoint)

	

#Creates washrecords
def createWashRecord():
	global energypoints
	global startTime
	price = environment.getPriceAt(startTime)
	info = server.getProgramInfo()
	info['startTime'] = startTime
	info['endTime'] = currentTime()
	
	if len(energypoints) == 0:
		energypoints = [{'time':currentTime(),'value':0}]
	
	washRecord = {'programInfo':info,'price':price, "totalEnergy":totalEnergy, "points":energypoints}	

	washRecord = json.dumps(washRecord)

	fo = open("records/"+str(startTime), "w")
	fo.write(washRecord)
	fo.close()



#Reset global variables before recording
def startRecording():
	print "Start recording"
	global totalEnergy
	totalEnergy = 0.0
	global energypoints
	energypoints = []
	global startTime
	startTime = currentTime()
	global isRunning
	isRunning = True


#
def stopRecording():
	print "Stop recording"
	createWashRecord()
	global isRunning
	isRunning = False

def getLatestEnergy():
	global latestEnergy
	return latestEnergy

#get live data: status, time left, current energy
def getLiveData():
	global latestEnergy
	global timeLeft
	global isRunning	
	
	timeLeft = 43
	returnValue = {'isRunning':isRunning, 'timeLeft':timeLeft, 'energy':latestEnergy}
	return returnValue
	

def init():
	global latestEnergy
	latestEnergy = 0
