#!/usr/bin/env python3

# Copyright (c) 2015-2020 Agalmic Ventures LLC (www.agalmicventures.com)
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
import random
import sys
import time

def main(argv=None):
	"""
	The main function of this script.

	:param argv: List[str] Arguments to parse (default sys.argv)
	:return: int
	"""
	parser = argparse.ArgumentParser(description='Randomized sleep script (e.g. for offseting process start times).')
	parser.add_argument('min', type=float, help='Minimum time to sleep (seconds).')
	parser.add_argument('max', type=float, help='Maximum time to sleep (seconds).')
	parser.add_argument('-v', '--verbose', action='store_true', help='Output wait time in seconds.')

	if argv is None:
		argv = sys.argv
	arguments = parser.parse_args(argv[1:])

	sleepTime = random.uniform(arguments.min, arguments.max)
	if arguments.verbose:
		print(str(sleepTime))
	time.sleep(sleepTime)

	return 0

if __name__ == '__main__':
	sys.exit(main())
