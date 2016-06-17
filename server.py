



class Server:

	def __init__(self, addr, port, homeDir):
		self.addr = addr
		self.port = port
		self.homeDir = {
			"path": homeDir,
			"fileList": []
		}


	# wonky things for storing the files
	def setup_homeDir(self):
		pass

	# setup the socket stuff, connect etc..
	def spinup(self):
		pass

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
	x = Server("", 8080, ".")

