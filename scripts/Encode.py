#!/usr/bin/env python3

# Copyright (c) 2015-2020 Agalmic Ventures LLC (www.agalmicventures.com)
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
import base64
import binascii
import hashlib
import sys

ENCODINGS = {
	'base16': lambda d: base64.b16encode(d).decode('utf8'),
	'base32': lambda d: base64.b32encode(d).decode('utf8'),
	'base64': lambda d: base64.b64encode(d).decode('utf8'),
	'base85': lambda d: base64.b85encode(d).decode('utf8'),

	'base16d': lambda d: base64.b16decode(d).decode('utf8'),
	'base32d': lambda d: base64.b32decode(d).decode('utf8'),
	'base64d': lambda d: base64.b64decode(d).decode('utf8'),
	'base85d': lambda d: base64.b85decode(d).decode('utf8'),

	'crc32': lambda d: '%x' % binascii.crc32(d),
	'hex': lambda d: binascii.hexlify(d).decode('utf8'),
	'unhex': lambda d: binascii.unhexlify(d.strip()).decode('utf8'),
}

for algorithmName in hashlib.algorithms_available:
	if hasattr(hashlib, algorithmName):
		algorithm = getattr(hashlib, algorithmName)
		ENCODINGS[algorithmName] = lambda d, algorithm=algorithm: algorithm(d).hexdigest()

def main(argv=None):
	"""
	The main function of this script.

	:param argv: List[str] Arguments to parse (default sys.argv)
	:return: int
	"""
	parser = argparse.ArgumentParser(description='Encoder')
	parser.add_argument('encoding', help='Encoding to use (sha1, base64, etc.)..')
	#parser.add_argument('file', help='File to check.')
	parser.add_argument('file', nargs='?', type=argparse.FileType('rb'),
		default=sys.stdin)

	if argv is None:
		argv = sys.argv
	arguments = parser.parse_args(argv[1:])

	encoding = ENCODINGS.get(arguments.encoding)
	if encoding is None:
		print('ERROR: Encoding %s not found. Available encodings:\n%s' % (
			arguments.encoding,
			'\n'.join('\t%s' % e for e in sorted(ENCODINGS.keys()))))
		return 1

	#Read the file
	try:
		data = arguments.file.read()

		#stdin will return unicode
		if isinstance(data, str):
			data = data.encode('utf8')
	except IOError:
		return 3

	#Encode
	encoded = encoding(data)
	print(encoded)

	return 0

if __name__ == '__main__':
	sys.exit(main())
