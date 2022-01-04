#!/usr/bin/env python3

# Copyright (c) 2015-2022 Agalmic Ventures LLC (www.agalmicventures.com)
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

import curses
import sys
import time

def centerText(screen, text, row, flags=0):
	"""
	Centers some text on the screen in the given row.

	:param screen: curses screen
	:param text: str
	:param row: int
	:param flags: int
	:return: int Starting column
	"""
	c = (curses.COLS - len(text)) // 2
	screen.addstr(row, c, text, flags)
	return c

def cursesMain(screen):
	"""
	The main function of the curses program.

	:param screen: curses screen
	:return: int Exit code
	"""
	#Prompt
	c = centerText(screen, 'Enter Your Name', 1, curses.A_BOLD | curses.A_UNDERLINE)

	#Get the name
	name = ''
	while name == '':
		curses.echo()
		name = screen.getstr(2, c, 20).decode('utf-8')
		curses.noecho()

		message = 'What was that?'
		if name == '':
			time.sleep(1.0)
			centerText(screen, message, 5)
		else:
			centerText(screen, ' ' * len(message), 5)

	#Do something with it
	time.sleep(1.0)
	centerText(screen, 'Hello %s.' % name, 5)
	screen.refresh()
	time.sleep(2.0)
	centerText(screen, 'Let me tell you a story.', 7)
	screen.refresh()
	time.sleep(4.0)
	centerText(screen, 'Once upon a time...', 10)
	screen.refresh()

	#Wait
	screen.getkey()
	return 0

def main():
	"""
	Wraps the cursesMain() function to restore the screen at the end,
	regardless of how the program is terminated.

	:return: int Exit code
	"""
	screen = curses.initscr()

	curses.noecho()
	curses.cbreak()
	screen.keypad(True)

	try:
		exitCode = cursesMain(screen)
	finally:
		screen.keypad(False)
		curses.nocbreak()
		curses.echo()
		curses.endwin()

	return exitCode

if __name__ == '__main__':
	sys.exit(main())
