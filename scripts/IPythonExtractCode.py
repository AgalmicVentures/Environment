#!/usr/bin/env python3

# Copyright (c) 2015-2018 Agalmic Ventures LLC (www.agalmicventures.com)
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
import json
import sys

def main(argv=None):
	parser = argparse.ArgumentParser(description='IPython Cleanup Tool')
	parser.add_argument('-s', '--separator', default=None,
		help='Separator to add between cells')
	parser.add_argument('file', help='IPython note book file to clean.')

	if argv is None:
		argv = sys.argv
	arguments = parser.parse_args(argv[1:])

	#Try parsing the file
	try:
		with open(arguments.file) as sourceFile:
			source = sourceFile.read()
			sourceJson = json.loads(source)
	except IOError:
		return 3
	except ValueError:
		return 2

	#Grab code from cells
	first = True
	for cell in sourceJson.get('cells', []):
		#Skip everything else
		if cell.get('cell_type') != 'code':
			continue

		if not first and arguments.separator is not None:
			print()
			print(arguments.separator)
			print()
		first = False

		#Join the lines (which already have newlines in normal notebooks)
		source = ''.join(
			#Automatically comment out magic commands
			#TODO: support other language comment types?
			'# ' + line if line.startswith('%') else line
			 for line in cell.get('source', []))

		print(source)

	return 0

if __name__ == '__main__':
	sys.exit(main())
