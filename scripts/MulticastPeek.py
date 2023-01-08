#!/usr/bin/env python3

# Copyright (c) 2015-2023 Agalmic Ventures LLC (www.agalmicventures.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import datetime
import socket
import sys

def main(argv=None):
	"""
	The main function of this script.

	:param argv: List[str] Arguments to parse (default sys.argv)
	:return: int
	"""
	parser = argparse.ArgumentParser(description='Listen to a multicast group.')
	parser.add_argument('group', help='Multicast group to listen to (e.g. 224.1.1.1).')
	parser.add_argument('port', type=int, help='Multicast port to listen to (e.g. 5007).')

	parser.add_argument('-i', '--interface', default='0',
		help='Interface to listen on (default INADDR_ANY).')

	parser.add_argument('-c', '--count', action='store', type=int,
		help='Number of packets to receive.')

	if argv is None:
		argv = sys.argv
	arguments = parser.parse_args(argv[1:])

	#Setup the listening socket
	listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	listeningSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	multicastMembership = socket.inet_aton(arguments.group) + socket.inet_aton(arguments.interface)
	listeningSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, multicastMembership)
	listeningSocket.bind( (arguments.group, arguments.port) )

	#Listen for packets
	count = 0
	while True:
		packet = listeningSocket.recv(4096)
		print(('[%s] Packet %d ' % (datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S.%f'), count)).ljust(80, '*'))
		print()
		print('Python value: %s' % packet)
		print()
		print('ASCII: %s' % ' '.join('%2s' % chr(b) if chr(b).isprintable() else '.' for b in packet))
		print('  Hex: %s' % ' '.join('%02X' % b for b in packet))
		print()

		count += 1
		if arguments.count is not None and count >= arguments.count:
			break

	return 0

if __name__ == '__main__':
	sys.exit(main())
