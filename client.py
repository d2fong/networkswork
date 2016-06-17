
class Client:

	TCP_DEFAULT_PORT = -1
	TCP_DEFAULT_ADDR = ""

	def __init__(self, serverAddr, serverPort):
		self.serverAddr = serverAddr
		self.serverPort = serverPort
		self.tcpPort = Client.TCP_DEFAULT_PORT
		self.tcpAddr = Client.TCP_DEFAULT_ADDR

	def negotiate_connection(self):
		pass

	def create_list_request(self):
		pass

	def transaction_connection(self):
		pass



def testClient():
	c = Client("localhost", 9090)
	
testClient()

