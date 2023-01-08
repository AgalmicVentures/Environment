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
import ast
import datetime
import socket
import sys
import time

def main(argv=None):
	"""
	The main function of this script.

	:param argv: List[str] Arguments to parse (default sys.argv)
	:return: int
	"""
	parser = argparse.ArgumentParser(description='Listen to a multicast group.')
	parser.add_argument('group', help='Multicast group to listen to (e.g. 224.1.1.1).')
	parser.add_argument('port', type=int, help='Multicast port to listen to (e.g. 5007).')
	parser.add_argument('data', help='Data to send.')

	parser.add_argument('-c', '--count', action='store', type=int, default=1,
		help='Number of times to send.')
	parser.add_argument('-v', '--verbose', action='store_true',
		help='Verbose mode (announce when sending).')
	parser.add_argument('-w', '--wait', action='store', type=float, default=0.0,
		help='Wait time before sending again.')

	if argv is None:
		argv = sys.argv
	arguments = parser.parse_args(argv[1:])

	#Parse the input as if it's a Python bytes literal
	data = ast.literal_eval('b"' + arguments.data.replace('"', "\\x22") + '"')

	#Setup the socket
	sendingSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sendingSocket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

	#Listen for packets
	count = 0
	while True:
		#Send the data
		sendingSocket.sendto(data, (arguments.group, arguments.port))
		if arguments.verbose:
			print('[%s] Sent packet %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), count))

		#Wait
		if arguments.wait > 0 and count != arguments.count - 1:
			time.sleep(arguments.wait)

		count += 1
		if arguments.count is not None and count >= arguments.count:
			break

	return 0

if __name__ == '__main__':
	sys.exit(main())
