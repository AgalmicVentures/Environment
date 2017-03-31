#!/usr/bin/env python3

import argparse
import random
import sys
import time

def main():
	parser = argparse.ArgumentParser(description='Randomized sleep script (e.g. for offseting process start times).')
	parser.add_argument('min', type=float, help='Minimum time to sleep (seconds).')
	parser.add_argument('max', type=float, help='Maximum time to sleep (seconds).')
	parser.add_argument('-v', '--verbose', action='store_true', help='Output wait time in seconds.')
	arguments = parser.parse_args(sys.argv[1:])

	sleepTime = random.uniform(arguments.min, arguments.max)
	if arguments.verbose:
		print(str(sleepTime))
	time.sleep(sleepTime)

	return 0

if __name__ == '__main__':
	sys.exit(main())
