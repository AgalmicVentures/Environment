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
import csv
try:
	import ujson as json
except ImportError:
	import json
import sys

def csvToJson(reader, transform=lambda x: x, prefix='', suffix='', ignores=[]):
	"""
	Converts a stream of CSV data to a stream of JSON data

	:param reader: csv.DictReader
	:return: sequence of JSON dictionaries
	"""
	for line in reader:
		outputJson = {}
		for k, v in line.items():
			if k in ignores:
				continue

			transformedKey = prefix + transform(k) + suffix
			outputJson[transformedKey] = v

		yield outputJson

def main(argv=None):
	"""
	The main function of this script. Converts CSV to JSON based on the arguments provided.

	:param argv: List[str] Arguments to parse (default sys.argv)
	:return: int
	"""
	#Parse arguments
	parser = argparse.ArgumentParser(description='CSV -> JSON Converter')

	parser.add_argument('-S', '--single', action='store_true',
		help='Generate a single document, rather than 1 document per line')

	parser.add_argument('-d', '--delimiter', default=',',
		help='Delimiter character (default is a comma)')
	parser.add_argument('-q', '--quote', default='"',
		help='Quote character (default is a double quote)')

	parser.add_argument('-i', '--ignore', default=[], action='append',
		help='Adds a column to ignore.')

	parser.add_argument('-p', '--prefix', default='',
		help='Sets the column prefix (e.g. for namespacing).')
	parser.add_argument('-s', '--suffix', default='',
		help='Sets the column suffix (e.g. for namespacing).')

	parser.add_argument('-c', '--capitalize', dest='transform',
		action='store_const', const=str.capitalize, default=lambda x: x,
		help='Capitalizes column names when converting to keys (default=None)')
	parser.add_argument('-l', '--lower', dest='transform',
		action='store_const', const=str.lower,
		help='Lowercases column names when converting to keys (default=None)')
	parser.add_argument('-u', '--upper', dest='transform',
		action='store_const', const=str.upper,
		help='Uppercases column names when converting to keys (default=None)')
	#TODO: underscores to camel

	if argv is None:
		argv = sys.argv
	arguments = parser.parse_args(argv[1:])

	#Read input
	if arguments.single:
		print('[')
	lastOutput = None
	for outputJson in csvToJson(
		csv.DictReader(sys.stdin, delimiter=arguments.delimiter, quotechar=arguments.quote),
		transform=arguments.transform, prefix=arguments.prefix, suffix=arguments.suffix, ignores=arguments.ignore):
		if lastOutput is not None:
			print(lastOutput)

		lastOutput = json.dumps(outputJson, sort_keys=True) + ',' if arguments.single else ''

	if lastOutput is not None:
		print(lastOutput[:-1])
	if arguments.single:
		print(']')

	return 0

if __name__ == '__main__':
	sys.exit(main())
