#!/usr/bin/env python3

import argparse
import csv
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

def main():
	"""
	The main function of this script. Converts CSV to JSON based on the arguments provided.

	:return: int
	"""
	#Parse arguments
	parser = argparse.ArgumentParser(description='Converts CSV files to JSON.')

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

	arguments = parser.parse_args(sys.argv[1:])

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
