import os
import socket
import struct

# Client error codes

TCP_CONN_MISSING = 4


UDP_IP = "localhost"
UDP_PORT = 8888


def error(code, msg):
	print "ERROR: %d %s" (code, msg)

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
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	tcpIP = None
	tcpPort = None
	try:
		sock.sendto("list", (UDP_IP, UDP_PORT))
		data, addr = sock.recvfrom(1024)
		text = data.decode('ascii')
		print text

		sock.sendto("tcp", (UDP_IP, UDP_PORT))
		data, addr = sock.recvfrom(1024)
		text = data.decode('ascii')
		tcpIP = text.split('\n')[0]
		tcpPort = int(text.split('\n')[1])
		print text

	finally:
		sock.close()

	tcpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	if tcpIP is None or tcpPort is None:
		error(4, "tcp port, or tcp addr not found")
	tcpSock.connect((tcpIP, tcpPort))

	try:
		message = "get f1.txt"
		payload = struct.pack('>I', len(message)) + message
		tcpSock.sendall(payload)

		data = recv_server_msg(tcpSock)
		print data

		if data == "ok":
			data = recv_server_msg(tcpSock)
		
		print data

	finally:
		tcpSock.close()


	# # get args
	# if len(argv) != 2:
	# 	error(-1, "Expect 2 strings as args")

	# # connect to server
	# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# sock.bind((UDP_IP, UDP_PORT))

	# # send the list request

	# sock.sendto("list", (UDP_IP, UDP_PORT))

	# # get list response
	# # may need to get more data
	# data, addr = sock.recvfrom(1024)


	# # send first request, get the remote filename 

	# tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# tcp_sock.connect((TCP_IP, TCP_PORT))
	# tcp.send("get" + " " + argv[1] + " " + argv[2])
	# # get server response

	# data = s.recv(1024)

	# # interpret the data and get an error code

	# code = int(data[:4])

	# # if ok, then get the local file contents and put them in local file

	# if code == 0:
	# 	f = os.open(argv[1])
	# 	f.write(data)
	# 	f.close()

	# else:
	# 	error(-1, "Did not receive ok from server")
	# # if not, error

	# # close local file, close socket

	# sock.close()
	# tcp_sock.close()

main()

