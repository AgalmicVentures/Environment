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
	The main function of this script. Instantiates a template based on a JSON config.

	:return: int
	"""
	#Parse arguments
	parser = argparse.ArgumentParser(description='Fills out templates with JSON configurations.')
	parser.add_argument('template', help='Path to the template file.')
	parser.add_argument('config', help='Path to the configuration JSON file.')

	arguments = parser.parse_args(sys.argv[1:])

	with open(arguments.template) as templateFile, open(arguments.config) as configFile:
		#Read template
		template = templateFile.read()

		#Read config
		configStr = configFile.read()
		try:
			configJson = json.loads(configStr)
		except ValueError as e:
			print('Error parsing JSON: %s' % e)
			return 1

		#File out the template
		sys.stdout.write(template % configJson)

	return 0

if __name__ == '__main__':
	sys.exit(main())
