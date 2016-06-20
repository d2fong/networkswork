import socket

# ERROR CODES
SERVER_ALREADY_STARTED = 5




def error(code, msg):
	print "[ERROR]: %s, %d"%(msg, code)

def log(lvl, msg):
	print "[%s]: %s"%(lvl, msg)

DEFAULT_SERVER_PORT = 8899
DEFAULT_MAX_CONNECTIONS = 5
DEFAULT_HOME_DIR = './home_server'



class Server:

	def __init__(self, addr=None,
	 port=DEFAULT_SERVER_PORT,
	 homeDir=DEFAULT_HOME_DIR,
	 maxConnections=DEFAULT_MAX_CONNECTIONS):
		self.addr = addr
		self.port = port
		self.homeDir = {
			"path": homeDir,
			"fileList": []
		}
		self.socket = None
		self.maxConnections = maxConnections

	# wonky things for storing the files
	# given a home directory, for each file in the
	# directory, add it to the file list
	# 
	def setup_homeDirAndFileList(self):
		# for f in self.homeDir:
			# self.fileList.append(f)
		pass

	# setup the socket stuff, connect etc..
	def spinup(self):
		if self.socket is not None:
			error(5, "The server has already been started")
		else:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

			if self.addr is None:
				self.addr = socket.gethostname()

			self.socket.bind((self.addr , self.port))
			log("INFO", "addr: %s, port: %d"%(self.addr, self.port))
			self.waitAndServe()

	def waitAndServe(self):
		while True:
			data, address = self.sock.recvfrom(4096)

			log("INFO", "Received %s bytes from address %s"% (len(data), address))
			log("INFO", "Message contents: %s", data)




	def create_connection(self):
		pass

	def end_connection(self):
		pass

	# receive commands from the client, see which one
	# we need to process and then process it
	def parse_command(self, command):
		if command.split(' ')[0] == "get":
			self.process_get(command)
		else:
			if command.split(' ')[0] == "put":
				self.process_put(command)

	def process_get(self, command):
		pass

	def process_put(self, command):
		pass

	def receive_data(self):
		pass

	def validate_filename(self, fname):
		pass


	# send our response to the client

	def send_response(self):
		pass 

	def send_file(self, fname):
		pass




def create_file(fname):
	pass


def open_file(fname):
	pass

def send_file(fname):
	pass


def serverTest():
	x = Server(port=8080, homeDir=" ")
	x.spinup()

serverTest()
