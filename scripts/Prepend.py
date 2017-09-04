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

def main():
	#Parse arguments
	parser = argparse.ArgumentParser(description='Prepend Files')
	parser.add_argument('source', help='File to prepend to others.')
	parser.add_argument('targets', nargs='*', help='A set of configurations to run.')
	parser.add_argument('-s', '--skip-shebang', action='store_true',
		help='In files with a shebang on the first line, insert the file after that line.')
	arguments = parser.parse_args(sys.argv[1:])

	#Read the source file
	with open(arguments.source) as sourceFile:
		sourceContents = sourceFile.readlines()

	#Write it to the targets
	for target in arguments.targets:
		#Read the target
		with open(target) as targetFile:
			targetContents = targetFile.readlines()

		#Join the content, optionally skipping the first line if it's a shebang
		if arguments.skip_shebang and len(targetContents) > 0 and targetContents[0].startswith('#!'):
			newContents = [targetContents[0]] + sourceContents + targetContents[1:]
		else:
			newContents = sourceContents + targetContents

		#Write the target
		with open(target, 'w') as targetFile:
			targetFile.write(''.join(newContents))

	return 0

if __name__ == '__main__':
	sys.exit(main())
