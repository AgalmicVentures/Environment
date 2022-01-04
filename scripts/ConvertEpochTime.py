#!/usr/bin/env python3

# Copyright (c) 2015-2022 Agalmic Ventures LLC (www.agalmicventures.com)
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
import sys

def main(argv=None):
	"""
	The main function of this script.

	:param argv: List[str] Arguments to parse (default sys.argv)
	:return: int
	"""
	parser = argparse.ArgumentParser(description='Epoch Time Converter')
	parser.add_argument('-f', '--format', default='%Y-%m-%dT%H:%M:%S.%f',
		help='Output format (default: ISO 8601).')
	parser.add_argument('time', type=float, help='Epoch time in arbitrary units.')

	if argv is None:
		argv = sys.argv
	arguments = parser.parse_args(argv[1:])

	#Do the conversion for each possible divisor
	divisors = [
		('s ', 1),
		('ms', 1000),
		('us', 1000 * 1000),
		('ns', 1000 * 1000 * 10000),
	]
	for unit, divisor in divisors:
		quotient = arguments.time / divisor
		try:
			utcTime = datetime.datetime.utcfromtimestamp(quotient)
			print('%d %s --> %s' % (arguments.time, unit, utcTime.strftime(arguments.format)))
		except ValueError:
			pass #Skip year out of range errors

	return 0

if __name__ == '__main__':
	sys.exit(main())
