#!/usr/bin/env python3

import argparse
import datetime
import itertools
import json
import os
import random
import sys

try:
    from itertools import izip
except ImportError:
    izip = zip

def main():
	#Parse arguments
	parser = argparse.ArgumentParser(description='Parallize helper script.')
	parser.add_argument('--fraction', type=float, default=1.0, help='Fraction of configs to sample, in the interval (0.0 to 1.0] (default=1.0).')
	parser.add_argument('--seed', default=None, help='Seed for the random number generator if sampling.')
	parser.add_argument('config', help='Path to the base configuration.')
	parser.add_argument('parameters', help='Path to the parameter configuration.')
	parser.add_argument('output_path', help='Output path.')
	arguments = parser.parse_args(sys.argv[1:])

	if arguments.fraction > 1.0:
		print('WARNING: Fraction must be in the interval (0.0, 1.0] -- capping at 1.0')
		arguments.fraction = 1.0
	elif arguments.fraction <= 0.0:
		print('ERROR: Fraction must be positive.')
		return 1

	startTime = datetime.datetime.now()
	print('[%s] Starting config generation...' % (startTime))

	if arguments.seed is not None:
		random.seed(arguments.seed)

	with open(arguments.config) as configFile:
		configData = configFile.read()
	config = json.loads(configData)

	with open(arguments.parameters) as parametersFile:
		parametersData = parametersFile.read()
	parameters = json.loads(parametersData)

	#Generate the Cartesian product of parameters
	count = 0
	parameterNames = sorted(parameters.keys())
	parameterValueLists = [parameters[k] for k in parameterNames]
	for parameterValues in itertools.product(*parameterValueLists):
		#Random sampling
		if arguments.fraction < 1.0 and arguments.fraction < random.random():
			continue

		#Generate the updated config
		#This could use the same dictionary over and over but that would be less clear
		updatedConfig = dict(config)
		outputFileNameParts = []
		for parameterName, parameterValue in izip(parameterNames, parameterValues):
			updatedConfig[parameterName] = parameterValue
			outputFileNameParts.append('%s=%s' % (parameterName, parameterValue))

		#Write it to a file
		outputFileName = '%s.json' % '_'.join(outputFileNameParts)
		with open(os.path.join(arguments.output_path, outputFileName), 'w') as outputFile:
			outputFile.write(json.dumps(updatedConfig, indent=2, separators=(',', ': '), sort_keys=True))

		count += 1

	endTime = datetime.datetime.now()
	print('[%s] Finished %d combinations in %.2f seconds' % (endTime, count, (endTime - startTime).total_seconds()))

	return 0

if __name__ == '__main__':
	sys.exit(main())