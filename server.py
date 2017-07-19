from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from generate_reply_completed import generateReply

import logging
logging.basicConfig(level=logging.DEBUG)

logging.debug("Comenzando server...")



# Simple WebSocket for single-user chat bot
class ChatServer(WebSocket):

	def handleMessage(self):
		logging.debug("server handleMessage")
		
		# echo message back to client
		message = self.data
		response = generateReply(message)
		self.sendMessage(response)

	def handleConnected(self):
		print(self.address, 'connected')

	def handleClose(self):
		print(self.address, 'closed')


#print(generateReply("I am not cool."))
server = SimpleWebSocketServer('', 8000, ChatServer)
server.serveforever()