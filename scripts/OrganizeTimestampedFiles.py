#!/usr/bin/env python

# Copyright (c) 2015-2019 Agalmic Ventures LLC (www.agalmicventures.com)
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
import datetime
import os
import re
import sys

def main(argv=None):
	"""
	The main function of this script.

	:param argv: List[str] Arguments to parse (default sys.argv)
	:return: int
	"""
	parser = argparse.ArgumentParser(description='Organizes files with timestamps in their name into directories.')
	parser.add_argument('-P', '--path', default='.', help='Where to look for files.')
	parser.add_argument('-d', '--dir', default='%Y/%m',
		help='The new directory files should be put in (timestamp format, default %%Y/%%m).')
	parser.add_argument('-x', '--extension', default=[], action='append',
		help='Add extension to look for (default all files).')
	parser.add_argument('-v', '--verbose', action='store_true', help='Output more information.')
	parser.add_argument('-D', '--dry-run', action='store_true', help='Do a dry run, only showing the renames.')

	if argv is None:
		argv = sys.argv
	arguments = parser.parse_args(argv[1:])

	#Create regular expressions
	extensionsRegexStr = '|'.join(arguments.extension) if len(arguments.extension) > 0 else '.*'
	fileNameRegexStr = (
		#Main name + date
		r'[a-zA-Z_-]+([0-9]{4})[_-]?([0-9]{2})[_-]?([0-9]{2})' +
		#Optional timestamp
		r'(?:[_-]?([0-9]{2})(?:[:_-]?([0-9]{2})(?:[:_-]?([0-9]{2}(?:[.:_-]?([0-9]{3-6}))?))?)?)?' +
		#Extension
		r'.(%s)' % extensionsRegexStr
	)
	fileNameRegex = re.compile(fileNameRegexStr)

	for fileName in os.listdir(arguments.path):
		#Parse the file name, skipping those without timestamps at the end
		match = fileNameRegex.match(fileName)
		if match is None:
			continue

		#Read the timestamp
		year = int(match.groups()[0])
		month = int(match.groups()[1])
		day = int(match.groups()[2])
		hour = int(match.groups()[3]) if match.groups()[3] is not None else 0
		minute = int(match.groups()[4]) if match.groups()[4] is not None else 0
		second = int(match.groups()[5]) if match.groups()[5] is not None else 0
		timestamp = datetime.datetime(year, month, day, hour, minute, second)

		#Format it into a directory name, and make the directories if necessary
		newDir = timestamp.strftime(arguments.dir)
		newDirPath = os.path.join(arguments.path, newDir)
		if not os.path.exists(newDirPath):
			os.makedirs(newDirPath)

		#Calculate the new path
		oldFilePath = os.path.join(arguments.path, fileName)
		newFileName = os.path.join(newDir, fileName)
		newFilePath = os.path.join(arguments.path, newFileName)
		if arguments.verbose:
			print('%s --> %s' % (fileName, newFileName))

		if not arguments.dry_run:
			os.rename(oldFilePath, newFilePath)

	return 0

if __name__ == '__main__':
	sys.exit(main())

