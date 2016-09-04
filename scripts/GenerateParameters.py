#!/usr/bin/env python3

import argparse
import datetime
import itertools
import json
import os
import sys

try:
    from itertools import izip
except ImportError:
    izip = zip

def main():
	#Parse arguments
	parser = argparse.ArgumentParser(description='Parallize helper script.')
	parser.add_argument('config', help='Path to the base configuration.')
	parser.add_argument('parameters', help='Path to the parameter configuration.')
	parser.add_argument('output_path', help='Output path.')
	arguments = parser.parse_args(sys.argv[1:])

	startTime = datetime.datetime.now()
	print('[%s] Starting config generation...' % (startTime))

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
