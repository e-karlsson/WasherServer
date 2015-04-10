from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs
import json
import history
import raspcom
import server

PORT_NUMBER = 8080
WASH_TIME = 45*60*1000

#handles http requests
class myHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		url = self.path.split("?",2)
		paths = url[0].split("/",2 )
		params = parse_qs(urlparse(self.path).query)
	
		self.send_response(200)
		self.send_header('Content-type','application/json')
		self.end_headers()
		
		if paths[1] == "get":
			handleGet(self, paths[2], params)
		elif paths[1] == "set":
			handleSet(self, paths[2], params)
		elif paths[1] == "start":
			handleStart(self, params)
		elif paths[1] == "stop":
			handleStop(self)
		else:
			self.wfile.write(json.dumps({'error':'bad url'}))	
		return

#handle all set requests
def handleSet(socket, path, params):
	paths = path.split("/", path.count("/"))
	if paths[0] == "settings":
		handleSettings(socket, params)
	if paths[0] == "wind":
		setWind(socket, params)

#handle all get requests
def handleGet(socket, path, params):
	paths = path.split("/", path.count("/"))
	if paths[0] == "history":
		getHistory(socket, params)
	if paths[0] == "live":
		getLive(socket) 
	if paths[0] == "settings":
		getSettings(socket)

#handle get history
def getHistory(socket, params):
	if params.get('amount'):
		amount = int(params['amount'][0])
		jData = history.getNRecords(amount)
		sendJSON(socket, jData)
	elif params.get('time'):
		time = int(params['time'][0])
		jData = history.getRecordsSince(time)
		sendJSON(socket, jData)

#handle get live feed
def getLive(socket):
	jData = raspcom.getLiveData()
	sendJSON(socket, jData)


def getSettings(socket):
	with open('settings/settings') as jsonfile:
		data = json.load(jsonfile)
	sendJSON(socket, data)

#sets the wind
def setWind(socket, params):
	if params.get('value'):
		value = int(params['value'][0])
		fo = open("settings/wind", "w")
		string = json.dumps({'isWind':value})
		print "saving: ", string
		fo.write(string)
		fo.close()
		sendJSON(socket, {'status':'ok'})
		return
	sendJSON(socket, {'status':'ok'})

#handles stop
def handleStop(socket):
	server.setRunning(False)
	server.stopDevice()
	sendJSON(socket, {'status':'ok'})
	return

#handles settings
def handleSettings(socket, params):
	if params.get('push') and params.get('price') and params.get('static') and params.get('reminderTime'):
		push = bool(params['push'][0])
		static = bool(params['static'][0])
		price = float(params['price'][0])
		reminderTime = int(params['reminderTime'][0])
		jsonData = {'push':push,'reminderTime':reminderTime,'static':static,'price':price}
		
		fo = open("settings/settings","w")
		string = json.dumps(jsonData)
		print "saving: ", string
		fo.write(string)
		fo.close()
		
		sendJSON(socket, {'status':'ok'})
	else:
		sendJSON(socket, {'status':'failed'})
	
#handles start
def handleStart(socket, params):
	if server.isRunning():
		sendJSON(socket, {'status':'failed','startAt':-1,'price':-1})
	elif params.get('washTime'):
		washTime = int(params['washTime'][0]) * 60 * 1000
		if params.get('time'):
			data = server.startDeviceWithinTime(int(params['time'][0]))
			sendJSON(socket, {'status':'ok','startAt':data[0],'price':data[1]})
			return
		elif params.get('readyAt'):
			readyAt = int(params['readyAt'][0])
			if params.get('useWind'):
				data = server.startDeviceWithWind(readyAt - washTime)
			elif params.get('lowPrice'):
				data = server.startDeviceAtLowestPrice(readyAt - washTime)
			else:
				data = server.startDeviceWithinTime(readyAt - washTime)
			
			sendJSON(socket, {'status':'ok','startAt':data[0],'price':data[1]})
			return
	sendJSON(socket, {'status':'failed','startAt':-1,'price':-1})

#sends json back to caller
def sendJSON(socket, data):
	print "Sending : ", data
	socket.wfile.write(json.dumps(data))

#starts the api server
def startAPIServer():

	try:

		server = HTTPServer(("", PORT_NUMBER), myHandler)
		print "Starting API server on port ", PORT_NUMBER

		server.serve_forever()

	except KeyboardInterrupt:
		print "Force shutting down API server"
		server.socket.close()

	except:
		print "Couldn't start API server"


