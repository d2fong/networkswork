#!/bin/python

import os
import socket
import struct
import sys

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

def client():
	command = sys.argv[1]
	ip = sys.argv[4]
	port = int(sys.argv[5])
	if command == "get":
		get(ip, port, sys.argv[2], sys.argv[3])

	if command == "put":
		put(ip, port, sys.argv[2], sys.argv[3])

	return


def put(ip, port, localFile, remoteFile):
	# Parse arguments
	# localFile = sys.argv[1]
	# remoteFile = sys.argv[2]

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
		sock.sendto("list", (ip, port))
		data, addr = sock.recvfrom(1024)
		text = data.decode('ascii')
		log("INFO", "received list response: %s"%text)

		sock.sendto("tcp", (ip, port))
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

def get(ip, port, remoteFile, localFile):
	# Parse arguments
	# remoteFile = sys.argv[1]
	# localFile = sys.argv[2]

	# Negotiation phase: Create UDP socket and establish a TCP connectino
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	tcpIP = None
	tcpPort = None
	try:
		sock.sendto("list", (ip, port))
		data, addr = sock.recvfrom(1024)
		text = data.decode('ascii')
		log("INFO", "received list response: %s"%text)

		sock.sendto("tcp", (ip, port))
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
		message = "get %s" % remoteFile
		payload = struct.pack('>I', len(message)) + message
		tcpSock.sendall(payload)

		data = recv_server_msg(tcpSock)
		log("INFO", "received server response: %s" % data)

		if data == "ok":
			# receiveing file
			remoteFileSize = int(recv_server_msg(tcpSock))
			data = recv_server_msg(tcpSock)

			if remoteFileSize != len(data):
				error("Expected %d bytes, received %d"% (remoteFileSize, len(data)))
				return -1
		else:
			error(data)
			return -1
	finally:
		tcpSock.close()

	# Write the data to the file content
	try:
		f = open(localFile, "w+")
		f.write(data)
	except:
		error("Unable to open and write to local file")
		return -1
	finally:
		f.close()

	return 0

client()

