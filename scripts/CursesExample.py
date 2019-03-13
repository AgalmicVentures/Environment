#!/usr/bin/env python3

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
