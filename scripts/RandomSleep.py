#!/usr/bin/env python3

import random
import sys
import time

def main():
	if len(sys.argv) < 3:
		print('RandomSleep.py <MIN_SEC> <MAX_SEC>')
		return 1

	try:
		minSleep = float(sys.argv[1])
	except ValueError:
		print('Invalid minimum sleep')
		return 1

	try:
		maxSleep = float(sys.argv[2])
	except ValueError:
		print('Invalid minimum sleep')
		return 1

	sleepTime = random.uniform(minSleep, maxSleep)
	time.sleep(sleepTime)

	return 0

if __name__ == '__main__':
	sys.exit(main())
