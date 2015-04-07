from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs
import json

PORT_NUMBER = 8083

class myHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		params = parse_qs(urlparse(self.path).query)
		print self.path
		paths = self.path.split("/", 3)
		
		self.send_response(200)
		self.send_header('Content-type','application/json')
		self.end_headers()
		
		if paths[1] == "get":
			handleGet(self, paths[2], params)
		elif paths[1] == "set":
			handleSet(self, paths[2], params)
		else:
			self.wfile.write(json.dumps({'error':'bad url'}))	
		return

def handleSet(socket, path, params):
	print "hej"

def handleGet(socket, path, params):
	paths = path.split("/", path.count("/"))
	if paths[0] == "history":
		getHistory(socket, params) 
	return

def getHistory(socket, params):
	amount = params["amount"]
	if amount:
		print "amount = ",amount
	print "history"

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


