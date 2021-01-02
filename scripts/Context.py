
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

import atexit
import datetime
import inspect
try:
	import ujson as json
except ImportError:
	import json
import os
import subprocess
import threading
import traceback

def _updateRunEnd(context):
	"""
	Exit handler for clean shutdowns.
	"""
	endTime = datetime.datetime.now()
	startTime = context.startTime()
	print('Run duration: %s (%s - %s)' % (endTime - startTime, startTime, endTime))

class _Context(object):

	def __init__(self):
		self._startTime = datetime.datetime.now()

		#Check the version
		currentFile = os.path.abspath(inspect.getfile(inspect.currentframe()))
		currentDir = os.path.dirname(currentFile)
		parentDir = os.path.dirname(currentDir)
		workingDirectory = os.getcwd()
		os.chdir(parentDir)
		try:
			self._gitVersion = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf8').strip()
			print('Version: %s' % self._gitVersion)
		except subprocess.CalledProcessError:
			self._gitVersion = None
			print('WARNING: Could not retrieve git version!')
		os.chdir(workingDirectory)

		#Prepare for the end of the run
		atexit.register(_updateRunEnd, self)

	##### Accessors #####

	def gitVersion(self):
		"""
		Returns the git version of the running code.

		:return: str
		"""
		return self._gitVersion

	def startTime(self):
		"""
		Returns the start time of the running code.

		:return: datetime.datetime
		"""
		return self._startTime

	##### Helpers #####

	def handleException(self, exception, details=None):
		"""
		Handles an exception by logging it, inserting it into the database, etc.

		:param exception: The exception
		"""
		backtrace = traceback.format_exc()
		print(' EXCEPTION THROWN '.center(60, '*'))
		print(backtrace)

#The global context is truly a singleton because the hardware it is managing can have only
#one thing using it at a time.
_context = None
_contextLock = threading.Lock()

class Context(object):
	"""
	The global singleton that holds all other object that are instantiated only
	once (e.g. config, logging, DB connections, etc.).
	"""

	def __new__(cls):
		global _context
		if _context is None:
			if _contextLock.acquire():
				try:
					if _context is None:
							_context = _Context()
				finally:
					_contextLock.release()
		return _context
