#!/usr/bin/env python3

import argparse
import datetime
import multiprocessing
import subprocess
import sys
import time

def main():
	#Parse arguments
	parser = argparse.ArgumentParser(description='Parallize helper script.')
	parser.add_argument('run_script', help='Find to do comments.')
	parser.add_argument('run_id', help='A unique identifier for the run')
	parser.add_argument('configs', nargs='*', help='A set of configurations to run.')
	arguments = parser.parse_args(sys.argv[1:])

	maxProcesses = multiprocessing.cpu_count()

	startTime = datetime.datetime.now()
	print('[%s] Starting %d processes for %d configs' % (startTime, maxProcesses, len(arguments.configs)))

	#Start processes
	processes = {}
	for i, config in enumerate(arguments.configs):
		#Wait for a CPU to become available
		while len(processes) >= maxProcesses:
			time.sleep(5)

			#Check for finished processes
			finishedConfigs = []
			for runningConfig, process in processes.items():
				returnCode = process.poll()
				if returnCode is not None:
					if returnCode != 0:
						sys.stdout.write('[%s] Config %s failed with return code %d' % (datetime.datetime.now(), runningConfig, returnCode))
						sys.stdout.flush()

					finishedConfigs.append(runningConfig)

			for finishedConfig in finishedConfigs:
				del processes[finishedConfig]

		sys.stdout.write('[%s] Starting %.4d/%.4d (%5.1f%%)\n' % (datetime.datetime.now(), i + 1, len(arguments.configs), 100.0 * (i + 1) / len(arguments.configs)))
		sys.stdout.flush()

		process = subprocess.Popen([arguments.run_script, arguments.run_id, config], shell=False)
		processes[config] = process

	#Wait for processes to finish
	for process in processes.values():
		process.wait()

	endTime = datetime.datetime.now()
	print('[%s] Finished in %.2f seconds' % (endTime, (endTime - startTime).total_seconds()))

	return 0

if __name__ == '__main__':
	sys.exit(main())
