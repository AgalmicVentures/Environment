#!/usr/bin/env python3

import argparse
import datetime
import multiprocessing
import subprocess
import sys
import time

def main():
	#Parse arguments
	parser = argparse.ArgumentParser(description='Prepend Files')
	parser.add_argument('source', help='File to prepend to others.')
	parser.add_argument('targets', nargs='*', help='A set of configurations to run.')
	parser.add_argument('-s', '--skip-shebang', action='store_true',
		help='In files with a shebang on the first line, insert the file after that line.')
	arguments = parser.parse_args(sys.argv[1:])

	#Read the source file
	with open(arguments.source) as sourceFile:
		sourceContents = sourceFile.readlines()

	#Write it to the targets
	for target in arguments.targets:
		with open(target) as targetFile:
			targetContents = targetFile.readlines()

		if arguments.skip_shebang and len(targetContents) > 0 and targetContents[0].startswith('#!'):
			newContents = [targetContents[0]] + sourceContents + targetContents[1:]
		else:
			newContents = sourceContents + targetContents

		with open(target, 'w') as targetFile:
			targetFile.write(''.join(newContents))

	return 0

if __name__ == '__main__':
	sys.exit(main())
