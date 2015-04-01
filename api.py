from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs
import json

PORT_NUMBER = 8080

class myHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		params = parse_qs(urlparse(self.path).query)
		print self.path
		self.send_response(200)
		self.send_header('Content-type','application/json')
		self.end_headers()
		self.wfile.write(json.dumps(params))	
		return



try:

	server = HTTPServer(("", PORT_NUMBER), myHandler)
	print "Started API server on port ", PORT_NUMBER

	server.serve_forever()

except KeyboardInterrupt:
	print "Force shutting down API server"
	server.socket.close()

