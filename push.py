import json
import time
import thread

currentTime = lambda: int(round(time.time()*1000))

	
#call if user should not be reminded
def reset():
	global hasPushed
	hasPushed = True

def deviceStopped():
	global hasPushed
	hasPushed = False
	data = loadSettings()
	if data['push']:
		sendPush('done')
		remindTime = data['reminderTime']
		if remindTime > 0:
			print "Reminding user in %d minutes" % remindTime
			pushTime = currentTime() + remindTime*60*1000
			
			try:
				thread.start_new_thread(waitToRemind, (pushTime,))
			except:
				print "Couldn't start reminder thread"
				

def sendPush(message):
	pushdata = {'data':{'message':message},'registration_ids':loadIds()}
	print "Sent Push: ", message
	print "Push json: ", json.dumps(pushdata)


def shouldPush():
	global hasPushed
	data = loadSettings()
	return data['push'] and not hasPushed

def remindTime():
	data = loadSettings()
	return data['reminderTime']

def loadSettings():
	with open('settings/settings') as jsonfile:
		data = json.load(jsonfile)
	return data

def removeId(ID):
	ids = loadIds()
	if ids.count(ID) != 0:
		ids.remove(ID)
		print "Removed %d from GCM ID's" % ID
	saveIds(ids)


def addId(ID):
	ids = loadIds()
	if ids.count(ID) == 0:
		ids.append(ID)
		print "Addes %d to GCM ID's" % ID
	saveIds(ids)

def saveIds(ids):
	data = {'ids':ids}
	data = json.dumps(data)
	
	fo.open('gcm/ids', "w")
	fo.write(data)
	fo.close()


def loadIds():
	with open('gcm/ids') as jsonfile:
		data = json.load(jsonfile)
	if 'ids' not in data:
		return []
	return data['ids']

def waitToRemind(pushTime):
	while (currentTime() < pushTime):
		time.sleep(1)
	
	if shouldPush():
		sendPush('reminder')


reset()
