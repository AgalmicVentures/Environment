#!/usr/bin/env python3

# Copyright (c) 2015-2021 Agalmic Ventures LLC (www.agalmicventures.com)
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

#TODO: inotify with a fallback

import argparse
import os
import stat
import sys
import time

def main(argv=None):
	"""
	The main function of this script.

	:param argv: List[str] Arguments to parse (default sys.argv)
	:return: int
	"""
	parser = argparse.ArgumentParser(description='Watches files and runs a command when they change.')
	parser.add_argument('-i', '--interval', action='store', type=float, default=0.1, help='Polling interval in seconds when not using inotify (default=0.1).')
	parser.add_argument('-p', '--pass-files', action='store_true', help='Flag indicating whether to pass changed files to the command.')
	parser.add_argument('-r', '--recurse', action='store_true', help='Recursively enumerate directories')
	parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output.')
	parser.add_argument('command', help='Command to run when one or more files change.')
	parser.add_argument('files', metavar='FILE', nargs='+', help='Files to watch')

	if argv is None:
		argv = sys.argv
	arguments = parser.parse_args(argv[1:])

	if arguments.verbose:
		print('Watching %s...' % ', '.join(arguments.files))

	stats = {}

	try:
		remainingFiles = set(arguments.files)
		while len(remainingFiles) > 0:
			#Check the last updated time on all the files
			changedFiles = []
			addedFiles = set()
			deletedFiles = set()
			for fileName in remainingFiles:
				try:
					newStat = os.stat(fileName)
				except FileNotFoundError:
					if arguments.verbose:
						print('Deleted: %s' % fileName)
					deletedFiles.add(fileName)
					continue

				oldStat = stats.get(fileName)
				changed = False
				if oldStat is None:
					stats[fileName] = newStat
					changed = True
				elif oldStat.st_mtime != newStat.st_mtime:
					changedFiles.append(fileName)
					stats[fileName] = newStat
					changed = True

				if arguments.recurse and changed and stat.S_ISDIR(newStat.st_mode):
					if arguments.verbose:
						print('Recursing: %s' % fileName)
					for (dirPath, dirNames, dirFileNames) in os.walk(fileName):
						for dirName in dirNames:
							fullPath = os.path.join(dirPath, dirName)
							addedFiles.add(fullPath)
							deletedFiles.discard(fullPath)
						for dirFileName in dirFileNames:
							fullPath = os.path.join(dirPath, dirFileName)
							addedFiles.add(fullPath)
							deletedFiles.discard(fullPath)

			remainingFiles -= deletedFiles
			remainingFiles.update(addedFiles)

			#Run the command?
			if len(changedFiles) > 0:
				if arguments.verbose:
					print('Changed: %s' % ', '.join(changedFiles))

				command = '%s %s' % (arguments.command, ' '.join(changedFiles)) if arguments.pass_files else arguments.command
				exitCode = os.system(command)
				if exitCode != 0:
					print('Failed with exit code: %d' % (exitCode))

			#Wait to poll again
			time.sleep(arguments.interval)
	except KeyboardInterrupt:
		pass #Not a problem

	return 0

if __name__ == '__main__':
	sys.exit(main())
