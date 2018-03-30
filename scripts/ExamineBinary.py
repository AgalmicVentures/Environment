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
import collections
import pprint
import sys

def examineSubstrings(data, length):
	"""
	Examines substrings of the data of a given length, looking for patterns.

	:param data: bytes
	:param length: int
	"""
	#Count values in a sliding window over the data
	total = len(data) - length
	window = (data[k:k+length] for k in range(0, total))
	counts = collections.Counter(window)
	print((' %s Byte Substrings ' % length).center(100, '*'))
	print()
	for values, count in counts.most_common(20):
		if count <= 1:
			break
		print('%10s %30s %s' % (count, values, tuple(value for value in values)))
	print()

	#If a value is more common than expected, it may be a divider that separates tokens
	mostCommon, mostCommonCount = counts.most_common(1)[0]
	mostCommonFraction = float(mostCommonCount) / total
	#TODO: use real statistics here for a certain significance level
	if mostCommonFraction > 64.0 / (256 ** length):
		print(' Common Tokens '.center(80, '*'))
		print('Most common divider found: %s %s' % (mostCommon, tuple(mostCommon)))
		print()
		tokens = data.split(mostCommon)
		tokenCounts = collections.Counter(tokens)
		for token, count in tokenCounts.most_common(20):
			if count <= 1:
				break
			print('%10s   %30s %s' % (count, token, tuple(token)))
		print()

def main(argv=None):
	parser = argparse.ArgumentParser(description='Binary Examiner')
	parser.add_argument('file', help='File to check.')

	if argv is None:
		argv = sys.argv
	arguments = parser.parse_args(argv[1:])

	#Read the file
	try:
		with open(arguments.file, 'rb') as sourceFile:
			data = sourceFile.read()
	except IOError:
		return 3

	for length in [1, 2, 4, 8]:
		examineSubstrings(data, length)

	return 0

if __name__ == '__main__':
	sys.exit(main())
