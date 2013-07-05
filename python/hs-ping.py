#!/usr/bin/env python

# Copyright (C) 2013 NEC de Colombia/TX-NOC
# Author: Carlos Uribe <cauribe@nec.com.co>

import os
import select
import socket
import struct
import sys
import time

ICMP_ECHO_REQUEST = 8

def checksum(source_string):
	sum = 0
	count_to = (len(source_string) / 2) * 2

	for count in xrange(0, count_to, 2):
		this = ord(source_string[count + 1]) * 256 + ord(source_string[count])
		sum = sum + this
		sum = sum & 0xffffffff
	
	if count_to < len(source_string):
		sum = sum + ord(source_string[len(source_string) - 1])
		sum = sum & 0xffffffff
	
	sum = (sum >> 16) + (sum & 0xffff)
	sum = sum + (sum >> 16)
	answer = ~sum
	answer = answer & 0xffff	
	answer = answer >> 8 | (answer << 8 & 0xff00)
	return answer

def receive_one_ping(my_socket, id, timeout):
	time_left = timeout

	while True:
		started_select = time.time()
		what_ready = select.select([my_socket], [], [], time_left)
		how_long_in_select = (time.time() - started_select)
		
		if what_ready[0] == []:
			return
		
		time_received = time.time()
		received_packet, addr = my_socket.recvfrom(1024)
		icmpHeader = received_packet[20:28]
		type, code, checksum, packet_id, sequence = struct.unpack("bbHHh", icmpHeader)
		
		if packet_id == id:
			bytes = struct.calcsize("d")
			time_sent = struct.unpack("d", received_packet[28:28 + bytes])[0]
			return time_received - time_sent
		time_left = time_left - how_long_in_select
		
		if time_left <= 0:
			return

def send_one_ping(my_socket, dest_addr, id, psize):
	dest_addr  =  socket.gethostbyname(dest_addr)
	psize = psize - 8
	my_checksum = 0

	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, id, 1)
	bytes = struct.calcsize("d")
	
	data = (psize - bytes) * "Q"
	data = struct.pack("d", time.time()) + data
	
	my_checksum = checksum(header + data)
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), id, 1)
	packet = header + data
	
	my_socket.sendto(packet, (dest_addr, 1))

def do_one(dest_addr, timeout, psize):
	icmp = socket.getprotobyname("icmp")
	
	try:
		my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
	except socket.error, (errno, msg):
		msg = ""
	
	my_id = os.getpid() & 0xFFFF
	send_one_ping(my_socket, dest_addr, my_id, psize)
	delay = receive_one_ping(my_socket, my_id, timeout)
	my_socket.close()
	
	return delay

if __name__ == '__main__':
	print do_one(sys.argv[1], sys.argv[2], sys.argv[3])
