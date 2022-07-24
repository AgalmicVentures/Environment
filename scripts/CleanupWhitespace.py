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
import re
import sys

def main(argv=None):
	"""
	The main function of this script.

	:param argv: List[str] Arguments to parse (default sys.argv)
	:return: int
	"""
	parser = argparse.ArgumentParser(description='Cleanup Whitespace')
	parser.add_argument('-a', '--access', action='store', type=int, default=None,
		help='# lines after a public/protected/private declaration')
	parser.add_argument('-e', '--eol', action='store_true',
		help='Remove end of line whitespce')
	parser.add_argument('file', nargs='*', help='Files to cleanup.')

	if argv is None:
		argv = sys.argv
	arguments = parser.parse_args(argv[1:])

	for path in arguments.file:
		with open(path, 'rb') as inputFile:
			contents = inputFile.read()

		if arguments.access is not None:
			contents = re.sub(b'public:\n+', b'public:' + b'\n' * arguments.access, contents)
			contents = re.sub(b'protected:\n+', b'protected:' + b'\n' * arguments.access, contents)
			contents = re.sub(b'private:\n+', b'private:' + b'\n' * arguments.access, contents)

		if arguments.eol:
			contents = re.sub(b'[ \t]+\n', b'\n', contents)

		with open(path, 'wb') as outputFile:
			outputFile.write(contents)

	return 0

if __name__ == '__main__':
	sys.exit(main())
