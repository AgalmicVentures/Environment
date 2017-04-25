#!/usr/bin/env python3

import argparse
import datetime
import multiprocessing
import subprocess
import sys
import time

def main():
	#Parse arguments
	parser = argparse.ArgumentParser(description='Parallel Runner')
	parser.add_argument('run_script', help='The script to execute.')
	parser.add_argument('run_id', help='A unique identifier for the run.')
	parser.add_argument('configs', nargs='*', help='A set of configurations to run.')
	parser.add_argument('-p', '--processes', type=int, default=multiprocessing.cpu_count(),
		help='Time to sleep between checking process completions.')
	parser.add_argument('-s', '--sleep', type=float, default=5.0,
		help='Time to sleep between checking process completions.')
	arguments = parser.parse_args(sys.argv[1:])

	startTime = datetime.datetime.now()
	print('[%s] Starting %d processes for %d configs' % (startTime, arguments.processes, len(arguments.configs)))

	#Start processes
	processes = {}
	for i, config in enumerate(arguments.configs):
		#Wait for a CPU to become available
		while len(processes) >= arguments.processes:
			time.sleep(arguments.sleep)

			#Check for finished processes
			finishedConfigs = []
			for runningConfig, process in processes.items():
				returnCode = process.poll()
				if returnCode is not None:
					if returnCode != 0:
						sys.stdout.write('[%s] Config %s failed with return code %d.' % (datetime.datetime.now(), runningConfig, returnCode))
						sys.stdout.flush()

					finishedConfigs.append(runningConfig)

			for finishedConfig in finishedConfigs:
				del processes[finishedConfig]

		sys.stdout.write('[%s] Starting %.4d/%.4d (%5.1f%%).\n' % (
			datetime.datetime.now(), i + 1, len(arguments.configs), 100.0 * (i + 1) / len(arguments.configs)))
		sys.stdout.flush()

		process = subprocess.Popen([arguments.run_script, arguments.run_id, config], shell=False)
		processes[config] = process

	#Wait for processes to finish
	for process in processes.values():
		process.wait()

	endTime = datetime.datetime.now()
	print('[%s] Finished in %.2f seconds.' % (endTime, (endTime - startTime).total_seconds()))

	return 0

if __name__ == '__main__':
	sys.exit(main())
