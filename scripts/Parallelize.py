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
import datetime
import multiprocessing
import os
import subprocess
import sys
import time

def main(argv=None):
	"""
	The main function of this script.

	:param argv: List[str] Arguments to parse (default sys.argv)
	:return: int
	"""
	parser = argparse.ArgumentParser(description='Parallel Runner')
	parser.add_argument('run_script', help='The script to execute.')
	parser.add_argument('run_id', help='A unique identifier for the run.')
	parser.add_argument('configs', nargs='*', help='A set of configurations to run.')
	parser.add_argument('-p', '--processes', type=int, default=multiprocessing.cpu_count(),
		help='Number of processes to run.')
	parser.add_argument('-m', '--max-load', type=float,
		help='Maximum value of 1-minute load average; above this do not spawn additional processes.')
	parser.add_argument('-s', '--sleep', type=float, default=5.0,
		help='Time to sleep between checking process completions.')

	if argv is None:
		argv = sys.argv
	arguments = parser.parse_args(argv[1:])

	try:
		getLoadAvg = os.getloadavg
	except AttributeError:
		getLoadAvg = lambda: (0, 0, 0)
		if arguments.max_load is not None:
			print('WARNING: Load averages not available on this platform; cannot limit.')

	startTime = datetime.datetime.now()
	print('[%s] Starting %d processes for %d configs' % (startTime, arguments.processes, len(arguments.configs)))

	#Start processes
	processes = {}
	for i, config in enumerate(arguments.configs):
		#Wait for a CPU to become available
		while len(processes) >= arguments.processes or (
				arguments.max_load is not None and getLoadAvg()[0] > arguments.max_load):
			time.sleep(arguments.sleep)

			#Check for finished processes
			finishedConfigs = []
			for runningConfig, process in processes.items():
				exitCode = process.poll()
				if exitCode is not None:
					if exitCode != 0:
						sys.stdout.write('[%s] Config %s failed with exit code %d.' % (
							datetime.datetime.now(), runningConfig, exitCode))
						sys.stdout.flush()

					finishedConfigs.append(runningConfig)

			for finishedConfig in finishedConfigs:
				del processes[finishedConfig]

		sys.stdout.write('[%s] Starting %.4d/%.4d (%5.1f%%).\n' % (
			datetime.datetime.now(), i + 1, len(arguments.configs), 100.0 * (i + 1) / len(arguments.configs)))
		sys.stdout.flush()

		process = subprocess.Popen([arguments.run_script, arguments.run_id, config], shell=False)
		processes[config] = process

		#Throttle process creation if targeting a max load
		if arguments.max_load is not None:
			time.sleep(arguments.sleep)

	#Wait for processes to finish
	for process in processes.values():
		process.wait()

	endTime = datetime.datetime.now()
	print('[%s] Finished in %.2f seconds.' % (endTime, (endTime - startTime).total_seconds()))

	return 0

if __name__ == '__main__':
	sys.exit(main())
