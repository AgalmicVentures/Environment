#!/usr/bin/env python3

import argparse
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

def main():
	"""
	The main function of this script. Converts JSON to XML based on the arguments provided.

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

	arguments = parser.parse_args(sys.argv[1:])
	indent = arguments.indent
	newline = arguments.newline
	root = arguments.root
	ignores = set(arguments.ignore)
	prefix = arguments.prefix
	suffix = arguments.suffix
	transform = arguments.transform

	#Read input
	inputString = sys.stdin.read()
	try:
		inputJson = json.loads(inputString)
	except ValueError as e:
		print('Error parsing JSON: %s' % e)
		return 1

	#Convert
	outputXml = jsonToXml(root, inputJson, indent=indent, newline=newline, ignores=ignores, prefix=prefix, suffix=suffix, transform=transform)

	#Output
	print(outputXml)
	return 0

if __name__ == '__main__':
	sys.exit(main())
