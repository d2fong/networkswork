#!/bin/python

import os
import socket
import struct

# ERROR CODES
SERVER_ALREADY_STARTED = 5

# SERVER CONFIG
DEFAULT_MAX_CONNECTIONS = 5
DEFAULT_HOME_DIR = os.path.abspath('./home_server')

# PROTOCOL MSG IDENTIFIERS
MSG_LIST = "list"
MSG_TCPCONN = "tcp"
MSG_GET = "get"
MSG_PUT = "put"

# Helper Functions
def error(msg):
	log("ERROR", msg)

def log(lvl, msg, data=None):
	print "[%s]: %s"%(lvl, msg)



class Server:

	def __init__(self, addr=None,
	 port=None,
	 homeDir=DEFAULT_HOME_DIR,
	 maxConnections=DEFAULT_MAX_CONNECTIONS):
		self.addr = addr
		self.port = port
		self.homeDir = {
			"path": homeDir,
			"fileList": []
		}
		self.udpSocket = None
		self.tcpSocket = None
		self.maxConnections = maxConnections

	# Set up a file list, this takes the all the files stored in the 
	# server file directory, and adds them to the list that shows which files are 
	# available to the sender
	def setup_file_list(self):
		base_path = self.homeDir['path']
		files = [f for f in os.listdir(base_path) if os.path.isfile(os.path.join(base_path, f))]
		self.homeDir['fileList'] = files
		# log("INFO", "Set up file list, contents: ")
		# map(lambda x: log("INFO", "file entry: " + x), files)

	# setup the socket stuff, connect etc..
	def spinup(self):
		if self.udpSocket is not None:
			error("The server has already been started")
		else:
			self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

			if self.addr is None:
				self.addr = socket.gethostname()

			if self.port is None:
				self.udpSocket.bind(('' , 0))
				self.port = self.udpSocket.getsockname()[1]
			else:
				self.udpSocket.bind(('', self.port))

			log("INFO", "addr: %s, port: %d"%(self.addr, self.port))

			self.wait_and_serve()


	# wait for client negotiation requests, parse them, and respond
	def wait_and_serve(self):
		while True:
			data, address = self.udpSocket.recvfrom(4096)
			text = data.decode('ascii')

			log("INFO", "Received %s bytes from address %s"% (len(data), address))
			log("INFO", "Message contents: %s"%text)

			if text == MSG_LIST:
				payload = '\n'.join(self.homeDir['fileList'])
						
				log("INFO", "sending filelist string \n%s"%(payload))
				self.udpSocket.sendto(payload.encode('ascii'), address)
			
			if text == MSG_TCPCONN:
				# create socket
				self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.tcpSocket.bind(('', 0))

				log("INFO", "tcp connection created on addr: %s, port %d"%
					(socket.gethostname(), self.tcpSocket.getsockname()[1]))

				# create address/port tuple and send it to the client
				payload = socket.gethostname() + "\n" + str(self.tcpSocket.getsockname()[1])
				self.udpSocket.sendto(payload.encode('ascii'), address)

				# handle the tcp request
				self.handle_tcp_request()

	def handle_tcp_request(self):
		# accept 1 client connectiona at a time
		self.tcpSocket.listen(1)

		# connect to a client and serve a single request
		conn, addr = self.tcpSocket.accept()

		# get the whole message from the client
		msg = self.recv_client_msg(conn)
		log("INFO", "got message %s"%msg)

		msgType = msg[:3]

		if msgType == MSG_GET:
			fileName = msg[4:]
			if fileName not in self.homeDir["fileList"]:
				response = "error file not in filelist"
				self.send(conn, response)
			else:
				fPath = self.homeDir["path"] + '/' + fileName
				log("INFO", "opening file %s"%fPath)
				fileContent = None
				expectedBytes = None
				try:
					f = open(fPath,"r")
					fileContent = f.read()
					expectedBytes = len(fileContent)
					# f.close()
				except:
					self.send(conn,"error could not open file")
					return

				self.send(conn, "ok")
				self.send(conn, str(expectedBytes))
				self.send(conn, fileContent)

		if msgType == MSG_PUT:
			parsedMsg = msg.split('\n')
			fileName = parsedMsg[0][4:]
			fPath = self.homeDir["path"] + "/" + fileName
			if fileName not in self.homeDir["fileList"]:
				self.homeDir["fileList"].append(fileName)
				try:
					f = open(fPath, "w+")
					f.write(parsedMsg[1])
					# f.close()
				except:
					self.send(conn, "error could not create file")
					return
			else:
				try:
					f = open(fPath, "w")
					f.write(parsedMsg[1])
					# f.close()
				except Exception as e:
					print e
					self.send(conn, "error could not open and write file")
					return

			self.send(conn, "ok")

	# custom recv/send functions
	# Each message has it's size appended at the front of it
	def send(self, sock, msg):
		payload = struct.pack('>I', len(msg)) + msg
		sock.sendall(payload)

	def recv_client_msg(self, sock):
		msgLen = self.recv_n_bytes(sock, 4)

		if not msgLen:
			return None

		msgLenNum = struct.unpack('>I', msgLen)[0]

		log("INFO", "received message length %d"%msgLenNum)

		return self.recv_n_bytes(sock, msgLenNum)

	# receive n bytes
	def recv_n_bytes(self, sock, n):
		buf = str()

		while len(buf) < n:
			p = sock.recv(n - len(buf))
			if not p:
				return None
			buf += p
		return buf


def serverTest():
	x = Server()
	x.setup_file_list()
	x.spinup()

serverTest()
