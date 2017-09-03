#!/usr/bin/env python3

# Copyright (c) 2015-2017 Agalmic Ventures LLC (www.agalmicventures.com)
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
import sys

def spacesToTabs(filename, spacesPerTab):
	with open(filename) as inf:
		lines = inf.readlines()

	with open(filename, 'w') as outf:
		for line in lines:
			numTabs = 0
			for n, ch in enumerate(line):
				if ch != '\t':
					numTabs = n
					break

			numSpaces = int(numTabs * spacesPerTab)
			numSpacesToRemove = numSpaces * spacesPerTab
			newLine = (' ' * numSpaces) + line[numTabs:]

			outf.write(newLine)

def main():
	#Parse arguments
	parser = argparse.ArgumentParser(description='Tabs To Spaces Converter')
	parser.add_argument('-n', '--spaces', type=int, default=4, help='Spaces per tab (default=4).')
	parser.add_argument('input_files', nargs='+', help='Input files.')
	arguments = parser.parse_args(sys.argv[1:])

	for filename in arguments.input_files:
		spacesToTabs(filename, arguments.spaces)

	return 0

if __name__ == '__main__':
	sys.exit(main())
