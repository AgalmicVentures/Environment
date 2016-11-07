#!/usr/bin/env python3

#TODO: inotify with a fallback

import argparse
import os
import sys
import time

def main():
	"""
	The main function of this script. Watches a number of files by polling their modified times, and runs a command when they change.

	:return: int
	"""
	#Parse arguments
	parser = argparse.ArgumentParser(description='Watches files and runs a command when they change.')
	parser.add_argument('-i', '--interval', action='store', type=float, default=0.1, help='Polling interval in seconds when not using inotify (default=0.1).')
	parser.add_argument('-p', '--pass-files', action='store_true', help='Flag indicating whether to pass changed files to the command.')
	parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output.')
	parser.add_argument('command', help='Command to run when one or more files change.')
	parser.add_argument('files', metavar='FILE', nargs='+', help='Files to watch')

	arguments = parser.parse_args(sys.argv[1:])

	if arguments.verbose:
		print('Watching %s...' % ', '.join(arguments.files))

	stats = {}

	try:
		while True:
			#Check the last updated time on all the files
			changedFiles = []
			for fileName in arguments.files:
				newStat = os.stat(fileName)
				oldStat = stats.get(fileName)
				if oldStat is None:
					stats[fileName] = newStat
				elif oldStat.st_mtime != newStat.st_mtime:
					changedFiles.append(fileName)
					stats[fileName] = newStat

			#Run the command?
			if len(changedFiles) > 0:
				if arguments.verbose:
					print('Changed %s:' % ', '.join(changedFiles))

				command = '%s %s' % (arguments.command, ' '.join(changedFiles)) if arguments.pass_files else arguments.command
				os.system(command)

			#Wait to poll again
			time.sleep(arguments.interval)
	except KeyboardInterrupt:
		pass #Not a problem

	return 0

if __name__ == '__main__':
	sys.exit(main())
