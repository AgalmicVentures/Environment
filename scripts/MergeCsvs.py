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
import csv
import itertools
import sys

def main(argv=None):
	"""
	The main function of this script.

	:param argv: List[str] Arguments to parse (default sys.argv)
	:return: int
	"""
	parser = argparse.ArgumentParser(description='Merge CSV Files')
	parser.add_argument('-n', '--no-headers', action='store_true',
		help='Do not write headers to the output.')

	parser.add_argument('-d', '--deduplicate', action='store_true',
		help='De-duplicate identical rows.')
	parser.add_argument('-s', '--sort', type=int,
		help='Column to sort on (0-indexed, default no sorting).')

	parser.add_argument('-N', '--newline-only', action='store_true',
		help='Use newlines as line endings, no carriage returns.')
	parser.add_argument('-q', '--quoting', type=int, default=csv.QUOTE_MINIMAL,
		help='Select quoting - 0=MINIMAL (default), 1=ALL, 2=NONNUMERIC, 3=NONE')

	parser.add_argument('output', help='Output file')
	parser.add_argument('files', nargs='+', help='Input files.')

	if argv is None:
		argv = sys.argv
	arguments = parser.parse_args(argv[1:])

	#Read all of the files
	headers = None
	data = []
	for filename in arguments.files:
		with open (filename) as csvFile:
			csvReader = csv.reader(csvFile)
			for n, row in enumerate(csvReader):
				#Handle headers
				if n == 0:
					if headers is None:
						headers = row
					elif headers != row:
						print('Mismatched headers in %s' % filename)
						return 1
					continue

				data.append(row)

	#Sort all the rows by key
	if arguments.sort is not None:
		data.sort(key=lambda row: int(row[arguments.sort]))

	#De-duplicate
	if arguments.deduplicate:
		data = [row for row, _ in itertools.groupby(data)]

	#Write to another file
	with open(arguments.output, 'w', newline='') as outputFile:
		csvWriter = csv.writer(outputFile,
			lineterminator='\n' if arguments.newline_only else '\r\n',
			quoting=arguments.quoting)
		if headers is not None and not arguments.no_headers:
			csvWriter.writerow(headers)
		csvWriter.writerows(data)

	return 0

if __name__ == '__main__':
	sys.exit(main())
