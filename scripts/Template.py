#!/usr/bin/env python3

import argparse
import json
import sys

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
