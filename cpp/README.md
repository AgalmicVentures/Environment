
## C++ (`cpp/`)
This folder contains useful snippets of C++.

Some of the snippets are complete programs; these may be executed directly (to
learn how, look at the first line of each file):

	> cpp/Rdtsc.cpp
	180986468

### `CoreSwitch.cpp`
Watches the core is running on via the `rdtscp` instruction and reports
changes along with the time stamp counter.

### `Rdtsc.cpp`
Reads the processor's time stamp counter and prints it to `stdout`. Contains an
assembly implementation of `rdtsc`.
