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

def encodeXmlEntities(data):
	"""
	Encodes strings for inclusion in XML.

	:param data: str
	:return: str
	"""
	#TODO: not complete
	return data.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace("'", '&apos;').replace('"', '&quot;')

def jsonToXml(tag, data, indent='\t', newline='\n', ignores=set(), prefix='', suffix='', transform=lambda x: x, depth=0):
	"""
	Converts a JSON dictionary to an XML string by recursively calling itself.

	:param tag: str Tag name of the current level
	:param data: dict JSON data at the current level
	:param indent: str Indent string (default `'\t'`)
	:param newline: str New line string (default `'\n'`)
	:param ignores: set Keys to ignore
	:param prefix: str Prefix to prepend to keys
	:param suffix: str Suffix to append to keys
	:param transform: function Transformation to apply to keys (e.g. to lower case)
	:return: str
	"""
	t = type(data)
	if t is dict:
		dataXmls = [newline]
		for k in sorted(data.keys()):
			if k in ignores:
				continue

			v = data[k]
			dataXmls.append(jsonToXml(k, v, indent=indent, newline=newline,
				ignores=ignores, prefix=prefix, suffix=suffix, transform=transform, depth=depth + 1))
		dataXml = ''.join(dataXmls)
	elif t is str:
		dataXml = encodeXmlEntities(data)
	else:
		dataXml = str(data)

	transformedTag = prefix + transform(tag) + suffix
	indentString = indent * depth
	return '%s<%s>%s%s</%s>%s' % (
		indentString,
		transformedTag,
		dataXml,
		indentString if dataXml[-1] == '\n' else '',
		transformedTag,
		newline
	)

def main(argv=None):
	"""
	The main function of this script. Converts JSON to XML based on the arguments provided.

	:param argv: List[str] Arguments to parse (default sys.argv)
	:return: int
	"""
	#Parse arguments
	parser = argparse.ArgumentParser(description='Converts JSON to XML.')
	parser.add_argument('-t', '--indent', default='\t',
		help='Sets the string used for a single level of indentation.')
	parser.add_argument('-n', '--newline', default='\n',
		help='Sets the string used for new lines.')
	parser.add_argument('-r', '--root', default='root',
		help='Sets the root tag.')

	parser.add_argument('-i', '--ignore', default=[], action='append',
		help='Adds a key to ignore.')

	parser.add_argument('-p', '--prefix', default='',
		help='Sets the tag prefix (e.g. for namespacing).')
	parser.add_argument('-s', '--suffix', default='',
		help='Sets the tag suffix (e.g. for namespacing).')

	parser.add_argument('-c', '--capitalize', dest='transform',
		action='store_const', const=str.capitalize, default=lambda x: x,
		help='Capitalizes tag names (default=None)')
	parser.add_argument('-l', '--lower', dest='transform',
		action='store_const', const=str.lower,
		help='Lowercases tag names (default=None)')
	parser.add_argument('-u', '--upper', dest='transform',
		action='store_const', const=str.upper,
		help='Uppercases tag names (default=None)')
	#TODO: underscores to camel

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
	outputXml = jsonToXml(arguments.root, inputJson,
		indent=arguments.indent,
		newline=arguments.newline,
		ignores=set(arguments.ignore),
		prefix=arguments.prefix,
		suffix=arguments.suffix,
		transform=arguments.transform)

	#Output
	print(outputXml)
	return 0

if __name__ == '__main__':
	sys.exit(main())
