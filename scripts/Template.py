#!/usr/bin/env python3

# Copyright (c) 2015-2017 Agalmic Ventures LLC (www.agalmicventures.com)
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
	"""
	The main function of this script. Instantiates a template based on a JSON config.

	:return: int
	"""
	#Parse arguments
	parser = argparse.ArgumentParser(description='Fills out templates with JSON configurations.')
	parser.add_argument('template', help='Path to the template file.')
	parser.add_argument('config', help='Path to the configuration JSON file.')

	if argv is None:
		argv = sys.argv
	arguments = parser.parse_args(argv[1:])

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
