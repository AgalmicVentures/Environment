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
import re
import sys

def main(argv=None):
	"""
	The main function of this script.

	:param argv: List[str] Arguments to parse (default sys.argv)
	:return: int
	"""
	parser = argparse.ArgumentParser(description='Homoglyph Finder')
	parser.add_argument('-r', '--replace', action='store_true', help='Replace the characters when found?')
	parser.add_argument('--line-break', default='\n', help='String to replace line break-like with.')
	parser.add_argument('--space', default=' ', help='String to replace space-like characters with.')
	parser.add_argument('files', nargs='+', help='Input files.')

	if argv is None:
		argv = sys.argv
	arguments = parser.parse_args(argv[1:])

	#Regexes for various classes of unicode characters that have simpler alternatives
	#For example, \u200B is the infamous zero width space
	#http://kb.mozillazine.org/Network.IDN.blacklist_chars has a good list of these sorts of characters
	#TODO: use the list from http://www.unicode.org/Public/security/latest/confusables.txt
	replacements = {
		'[\u2028\u2029]': arguments.line_break,
		'[\u00A0\u2000-\u200B\u202F\u205F\u3000\uFEFF]': arguments.space,
	}

	#Go through each file
	for filename in arguments.files:
		changed = False
		with open(filename) as file:
			data = file.read()
			for pattern, replacement in replacements.items():
				match = re.search(pattern, data)
				if match:
					print('[%s] Found "%s" -> "%s"' % (filename, data[match.span()[0]:match.span()[1]], replacement))
					if arguments.replace:
						data = re.sub(pattern, replacement, data)
						changed = True

		if arguments.replace and changed:
			with open(filename, 'w') as file:
				file.write(data)

	return 0

if __name__ == '__main__':
	sys.exit(main())
