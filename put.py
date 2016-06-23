import os
import socket
import struct
import sys

UDP_IP = "localhost"
UDP_PORT = 8888

def log(lvl, msg, data=None):
	print "[%s]: %s"%(lvl, msg)

def error(msg):
	log("ERROR", msg)

def recv_server_msg(socket):
	msgLen = recv_n_bytes(socket, 4)

	if not msgLen:
		return None

	msgLenNum = struct.unpack('>I', msgLen)[0]

	return recv_n_bytes(socket, msgLenNum)

# receive n bytes
def recv_n_bytes(socket, n):
	buf = str()

	while len(buf) < n:
		p = socket.recv(n - len(buf))
		if not p:
			return None
		buf += p
	return buf

# Input: String1, String2 in argv
# String1: Remote Filename
# String2: Local Filename
def main():
	# Parse arguments
	localFile = sys.argv[1]
	remoteFile = sys.argv[2]

	# Open the file and read the content
	content = ''
	f = None
	try:
		f = open(localFile, "r")
		content = f.read()
		f.close()
	except:
		error("Unable to open and write to local file")
		return -1

	# Negotiation phase: Create UDP socket and establish a TCP connectino
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	tcpIP = None
	tcpPort = None
	try:
		sock.sendto("list", (UDP_IP, UDP_PORT))
		data, addr = sock.recvfrom(1024)
		text = data.decode('ascii')
		log("INFO", "received list response: %s"%text)

		sock.sendto("tcp", (UDP_IP, UDP_PORT))
		data, addr = sock.recvfrom(1024)
		text = data.decode('ascii')
		tcpIP = text.split('\n')[0]
		tcpPort = int(text.split('\n')[1])
		log("INFO", "connected to tcp transaction addr: %s %d"%(tcpIP, tcpPort))

	finally:
		sock.close()

	# Connect to the tcp socket on the server
	tcpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	if tcpIP is None or tcpPort is None:
		error("tcp port, or tcp addr not found")
		return -1
	tcpSock.connect((tcpIP, tcpPort))

	# Transaction phase: lookup remote file on server, and write it to local file
	data = None
	try:
		message = "put " + remoteFile + '\n' + content
		payload = struct.pack('>I', len(message)) + message
		tcpSock.sendall(payload)

		data = recv_server_msg(tcpSock)
		log("INFO", "received server response: %s" % data)

		if data != "ok":
			error(data)
			return -1
	finally:
		tcpSock.close()

	return 0


main()









# UDP_IP = "Dylans-MacBook-Air.local"
# TCP_IP = UDP_IP
# UDP_PORT = 8888
# TCP_PORT = 8889

# def error(code, msg):
# 	print "ERROR: %d %s" (code, msg)


# # Input: String1, String2 in argv
# # String1: Local Filename
# # String2: Remote Filename
# def main():

# 	# get args
# 	if len(argv) != 2:
# 		error(-1, "Expected 2 strings as args")

# 	# connect to server
# 	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 	sock.bind((UDP_IP, UDP_PORT))

# 	# send the list request

# 	sock.sendto("list", (UDP_IP, UDP_PORT))

# 	# NEED TO RECV DATA PROPERLY
# 	data, addr = sock.recvfrom(1024)

# 	# open local file

# 	f = os.open(argv[1])

# 	# make buffer of local file contents

# 	buf = buffer(f)


# 	# send first request, put the remote filename 

# 	tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 	tcp_sock.connect((TCP_IP, TCP_PORT))
# 	tcp.send("put" + " " + argv[1] + " " + argv[2])

# 	# get server response AGAIN GET DATA PROPERLY

# 	data = s.recv(1024)

# 	# interpret the data to get an error code

# 	code = int(data[:4])

# 	# if ok, then send the local file contents

# 	if code == 0:
# 		f = os.open(argv[1])
# 		f.write(data)
# 		f.close()

# 	else:
# 		error(-1, "Did not receive ok from server")

# 	sock.close()
# 	tcp_sock.close()
# 	# if not, error

# 	# close local file, close socket