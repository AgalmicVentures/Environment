#!/usr/bin/env python3

# Copyright (c) 2015-2019 Agalmic Ventures LLC (www.agalmicventures.com)
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
	parser = argparse.ArgumentParser(description='Augment lines with additional information like number and time.')
	parser.add_argument('-f', '--format', default='[%(number)6d   %(time)s] %(line)s',
		help='Sets the format string for the augmented line with the following subsitutions: %%(number)s, %%(time)s, %%(line)s.')
	parser.add_argument('-t', '--time-format', default='%Y-%m-%d %H:%M:%S.%f',
		help='Sets the time\'s format string (default=%%Y-%%m-%%d %%H:%%M:%%S.%%f).')

	if argv is None:
		argv = sys.argv
	arguments = parser.parse_args(argv[1:])

	for n, line in enumerate(sys.stdin):
		now = datetime.datetime.now()
		augmentedLine = arguments.format % {
			'number': n,
			'time': now.strftime(arguments.time_format),
			'line': line[:-1],
		}

		print(augmentedLine)

	return 0

if __name__ == '__main__':
	sys.exit(main())
