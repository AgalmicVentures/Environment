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

CLASS_TOP_TEMPLATE = '''
class %(name)s(object):
	"""
	Represents TODO.
	"""'''

SLOTS_TEMPLATE = '''
	__slots__ = [%(slots)s]'''

CLASS_INIT_TEMPLATE = '''
	def __init__(%(constructorArguments)s):
		%(constructorParts)s'''

TYPE_CHECK_TEMPLATE = '''if not isinstance(%(field)s, %(type)s):
			raise ValueError('%(field)s must be type %(type)s')
'''

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

REPR_METHOD_TEMPLATE = '''
	def __repr__(self):
		"""
		Returns an interprettable representation of this object.

		:return: str
		"""
		return \'%(className)s(%(constructorArguments)s)\' %% (%(constructorValues)s)'''

TO_JSON_METHOD_TEMPLATE = '''
	def toJson(self):
		"""
		Returns this object as JSON.

		:return: dict
		"""
		return {
			%(values)s
		}'''

STR_METHOD_TEMPLATE = '''
	def __str__(self):
		"""
		Returns this object as a JSON string.

		:return: str
		"""
		return json.dumps(self.toJson())'''

def jsonToPythonClass(name, data, ignores=set(), defaults=False, mutable=False,
		generateSlots=False, generateTypeChecks=False, generateRepr=False, generateJson=False, generateStr=False):
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

	classStr = CLASS_TOP_TEMPLATE % {
		'name': name,
	}
	parts = [classStr]

	if generateSlots:
		slotsStr = SLOTS_TEMPLATE % {
			'slots': ', '.join("'%s'" % field for field in fields),
		}
		parts.append(slotsStr)

	constructorArguments = fields if not defaults else [
		'%s=%s' % (name, repr(data[name]))
		for name in sorted(data.keys())
		if name not in ignores
	]
	constructorParts = []
	if generateTypeChecks:
		constructorParts.append('\t\t'.join(TYPE_CHECK_TEMPLATE % {'field': field, 'type': type(data[field]).__name__} for field in fields))
	constructorParts.extend('self._%s = %s' % (field, field) for field in fields)

	classInitStr = CLASS_INIT_TEMPLATE % {
		'name': name,
		'constructorArguments': ', '.join(['self'] + constructorArguments),
		'constructorParts': '\n\t\t'.join(constructorParts),
	}
	parts.append(classInitStr)

	getMethodStrs = [GET_METHOD_TEMPLATE % {
		'name': field,
		'typeName': type(data[field]).__name__
	} for field in fields]
	parts.extend(getMethodStrs)

	if mutable:
		setMethodStrs = [SET_METHOD_TEMPLATE % {
			'name': field,
			'capitalizedName': '' if len(field) == 0 else field[0].upper() + field[1:],
			'typeName': type(data[field]).__name__,
		} for field in fields]
		parts.extend(setMethodStrs)

	if generateRepr:
		reprStr = REPR_METHOD_TEMPLATE % {
			'className': name,
			'constructorArguments': ', '.join('%s=%%s' % field for field in fields),
			'constructorValues': ', '.join('self._%s' % field for field in fields),
		}
		parts.append(reprStr)

	if generateJson or generateStr:
		jsonStr = TO_JSON_METHOD_TEMPLATE % {
			'values': '\n\t\t\t'.join('\'%s\': self._%s,' % (field, field) for field in fields),
		}
		parts.append(jsonStr)

	if generateStr:
		parts = ['import json'] + parts
		parts.append(STR_METHOD_TEMPLATE)

	return '\n'.join(parts)

def main(argv=None):
	"""
	The main function of this script. Converts JSON to Python code based on the arguments provided.

	:param argv: List[str] Arguments to parse (default sys.argv)
	:return: int
	"""
	#Parse arguments
	parser = argparse.ArgumentParser(description='Converts JSON to Python Classes.')
	parser.add_argument('name',
		help='The name of the class.')

	parser.add_argument('-t', '--tab-width', type=int,
		help='The width of a tab in spaces (default actual tabs).')

	parser.add_argument('-i', '--ignore', default=[], action='append',
		help='Adds a key to ignore.')

	parser.add_argument('-d', '--defaults', action='store_true',
		help='Generate defaults for constructor arguments.')
	parser.add_argument('-T', '--type-checks', action='store_true',
		help='Generate type checks.')
	parser.add_argument('-m', '--mutable', action='store_true',
		help='Generate setters.')
	parser.add_argument('-r', '--repr', action='store_true',
		help='Generate __repr__.')
	parser.add_argument('-j', '--json', action='store_true',
		help='Generate toJson.')
	parser.add_argument('-s', '--str', action='store_true',
		help='Generate __str__ (and toJson).')
	parser.add_argument('-S', '--slots', action='store_true',
		help='Generate __slots__ .')
	#TODO: caching __hash__ (and __eq__?) -- immutable only for the hash?

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
	output = jsonToPythonClass(arguments.name, inputJson,
		ignores=set(arguments.ignore),
		defaults=arguments.defaults,
		mutable=arguments.mutable,
		generateSlots=arguments.slots,
		generateTypeChecks=arguments.type_checks,
		generateRepr=arguments.repr,
		generateJson=arguments.json,
		generateStr=arguments.str,
	)

	#Indent
	if arguments.tab_width is not None:
		output = output.replace('\t', arguments.tab_width * ' ')

	#Output
	print(output)
	return 0

if __name__ == '__main__':
	sys.exit(main())
