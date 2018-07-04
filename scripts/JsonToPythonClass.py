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
try:
	import ujson as json
except ImportError:
	import json
import sys

CLASS_TEMPLATE = '''class %(name)s(object):
	"""
	Represents TODO.
	"""

	def __init__(%(constructorArguments)s):
		%(constructorAssignments)s'''

GET_METHOD_TEMPLATE = '''
	def %(name)s(self):
		"""
		Returns TODO.

		:return: %(typeName)s
		"""
		return self._%(name)s'''

SET_METHOD_TEMPLATE = '''
	def set%(capitalizedName)s(self, %(name)s):
		"""
		Sets TODO.

		:param: %(typeName)s
		"""
		self._%(name)s = %(name)s'''

def jsonToPythonClass(name, data, indent='\t', ignores=set(), mutable=False):
	"""
	Converts a JSON dictionary to an XML string by recursively calling itself.

	:param name: str Name of the class
	:param data: dict JSON data at the current level
	:param indent: str Indent string (default `'\t'`)
	:param ignores: set Keys to ignore
	:return: str
	"""
	t = type(data)
	if t is not dict:
		return '#TODO: Only dictionary types are currently supported'

	fields = [name for name in sorted(data.keys()) if name not in ignores]

	classStr = CLASS_TEMPLATE % {
		'name': name,
		'constructorArguments': ', '.join(['self'] + fields),
		'constructorAssignments': '\n\t\t'.join('self._%s = %s' % (field, field) for field in fields),
	}
	getMethodStrs = [GET_METHOD_TEMPLATE % {
		'name': field,
		'typeName': type(data[field]).__name__
	} for field in fields]

	parts = [
		classStr,
	] + getMethodStrs

	if mutable:
		setMethodStrs = [SET_METHOD_TEMPLATE % {
			'name': field,
			'capitalizedName': '' if len(field) == 0 else field[0].upper() + field[1:],
			'typeName': type(data[field]).__name__,
		} for field in fields]
		parts += setMethodStrs

	return '\n'.join(parts)

def main(argv=None):
	"""
	The main function of this script. Converts JSON to XML based on the arguments provided.

	:param argv: List[str] Arguments to parse (default sys.argv)
	:return: int
	"""
	#Parse arguments
	parser = argparse.ArgumentParser(description='Converts JSON to XML.')
	parser.add_argument('name',
		help='The name of the class.')

	parser.add_argument('-t', '--indent', default='\t',
		help='Sets the string used for a single level of indentation.')

	parser.add_argument('-i', '--ignore', default=[], action='append',
		help='Adds a key to ignore.')

	parser.add_argument('-m', '--mutable', action='store_true',
		help='Generate setters.')

	if argv is None:
		argv = sys.argv
	arguments = parser.parse_args(argv[1:])

	#Read input
	inputString = sys.stdin.read()
	try:
		inputJson = json.loads(inputString)
	except ValueError as e:
		print('Error parsing JSON: %s' % e)
		return 1

	#Convert
	outputXml = jsonToPythonClass(arguments.name, inputJson,
		indent=arguments.indent,
		ignores=set(arguments.ignore),
		mutable=arguments.mutable)

	#Output
	print(outputXml)
	return 0

if __name__ == '__main__':
	sys.exit(main())
