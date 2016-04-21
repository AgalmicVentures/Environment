#!/usr/bin/env python3

import argparse
import datetime
import sys

def main():
	parser = argparse.ArgumentParser(description='Augment lines with additional information like number and time.')
	parser.add_argument('-f', '--format', default='[%(number)6d   %(time)s] %(line)s',
		help='Sets the format string for the augmented line with the following subsitutions: %%(number)s, %%(time)s, %%(line)s.')
	parser.add_argument('-t', '--time-format', default='%Y-%m-%d %H:%M:%S.%f',
		help='Sets the time\'s format string (default=%%Y-%%m-%%d %%H:%%M:%%S.%%f).')

	arguments = parser.parse_args(sys.argv[1:])

	for n, line in enumerate(sys.stdin):
		now = datetime.datetime.now()
		augmentedLine = arguments.format % {
			'number': n,
			'time': now.strftime(arguments.time_format),
			'line': line[:-1],
		}

		print(augmentedLine)

	return 0

if __name__ == '__main__':
	sys.exit(main())
