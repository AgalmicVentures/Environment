#!/usr/bin/env python3

# Copyright (c) 2015-2023 Agalmic Ventures LLC (www.agalmicventures.com)
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
import os
import re
import sys

INTERESTING_EXTENSIONS = {
	'.crt',
	'.csr',

	'.key',
	'.pem',
	'.pub',
}

def containsSecrets(path, useName=True, useContent=True):
	"""
	Returns true if a path contains secrets (e.g. a private key).

	:param path: str
	:return: bool
	"""
	#File name based matching
	if useName:
		root, fileName = os.path.split(path)
		base, extension = os.path.splitext(fileName)
		if extension in INTERESTING_EXTENSIONS:
			return True
		elif extension == '' and fileName.startswith('id_'):
			return True

	#Content-based matching
	if useContent:
		with open(path, 'rb') as file:
			#Load the beginning of the file, for fingerprinting
			header = file.read(1024)
			firstLineBreak = header.find(b'\n')
			firstLine = header[:firstLineBreak] if firstLineBreak > 0 else header

			#Look for headers like:
			#-----BEGIN RSA PRIVATE KEY-----
			if re.match(b'^-----BEGIN [A-Z ]+-----', firstLine):
				return True

	return False

def main(argv=None):
	"""
	The main function of this script.

	:param argv: List[str] Arguments to parse (default sys.argv)
	:return: int
	"""
	parser = argparse.ArgumentParser(description='Secrets Extractor')
	parser.add_argument('--no-content', action='store_false',
		help='Ignore content in determining whether a file contains secrets.')
	parser.add_argument('--no-name', action='store_false',
		help='Ignore file name in determining whether a file contains secrets.')
	parser.add_argument('path', default='.',
		help='Path to search for secrets.')

	if argv is None:
		argv = sys.argv
	arguments = parser.parse_args(argv[1:])

	#Go through each file
	for root, dirs, files in os.walk(arguments.path, topdown=False):
		#Nothing to do with dirs (os.walk does all the recursion)

		#Handle files
		for file in files:
			filePath = os.path.join(root, file)
			if containsSecrets(filePath, useName=not arguments.no_name, useContent=not arguments.no_content):
				print(filePath)

	return 0

if __name__ == '__main__':
	sys.exit(main())
