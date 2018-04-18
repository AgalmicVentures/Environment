
## Scripts (`scripts/`)

### Python

#### `AugmentLines.py`
Augments lines of text (e.g. with a time stamp).

#### `CheckPythonSyntax.py`
Checks the syntax of a Python file without actually executing it. Exits with
code 1 if it is not valid.

#### `ConvertEpochTime.py`
Converts an epoch time into UTC times for all possible divisors (seconds,
milliseconds, microseconds, and nanoseconds).

#### `CsvToJson.py`
Converts CSV documents to JSON with a variety of transformation options.

#### `ExamineBinary.py`
Examines a binary file of unknown format to determine as much as possible
about it e.g. by finding the most common substrings.

#### `FindHomoglyphs.py`
Finds unicode homoglyphs used in fingerprinting files and optionally removes
them.

#### `GenerateConfigs.py`
Generates the a set of JSON configurations given a base configuration and a
second JSON object with lists of values for parameters
(`{"a": [1, 2], "b": [3, 4, 5]}`). Useful with `Parallelize.py` and
`Template.py`.

#### `IPythonCleanup.py`
Cleans up an IPython notebook file by removing outputs and reseting other state.

#### `IPythonExtractCode.py`
Extracts code from an IPython notebook. Note that `nbconvert` may be more
suitable (see http://nbconvert.readthedocs.io/en/latest/external_exporters.html).

#### `JsonToXml.py`
Converts JSON documents to XML with a variety of transformation options.

#### `MulticastPeek.py`
Listens to a multicast group and dumps the packets it receives in a
human-readable format.

#### `MulticastPoke.py`
Sends a packet to a multicast group, optionally repeating it a number of times.
Useful for keeping groups alive.

#### `OrganizeTimestampedFiles.py`
Moves files with timestamps at then end of their names into subdirectories
based on a given timestamp format (default `%Y/%m` for monthly buckets).

#### `Parallelize.py`
Given a process name, run ID, and set of configurations, runs the process in
parallel over all of the configurations. For example,
`./Parallelize.py ./xyz run134 config1 config2 config3 config4 config5` will run
`./xyz1 run134 config1`, ..., `./xyz1 run134 config5`.
It will use as many CPU's as are available. Useful with `GenerateConfigs.py` and
`Template.py`.

#### `Prepend.py`
Prepends a file to a number of target files, optionally skipping their first
line if it is a shebang. Useful for e.g. prepending license files to code.

#### `RandomSleep.py`
Sleeps for a random amount of time given a minimum and maximum bound. Useful for
randomizing the start time of processes.

#### `SpacesToTabs.py`
Converts spaces to tabs in place one or more files. WARNING: This operates
in-place, so it is best used in a repository where the changes can be reverted.

#### `TabsToSpaces.sh`
Converts tabs to spaces in place one or more files. WARNING: This operates
in-place, so it is best used in a repository where the changes can be reverted.

#### `Template.py`
Instantiates a template with values from a JSON configuration. Useful with
`GenerateConfigs.py` and `Parallelize.py`.

#### `WatchFiles.py`
Watches one or more files for modifications and runs a command when they are
changed (e.g. for automating local builds).

### Shell

#### `check_config.sh`
Checks the configuration of the system, including network buffer sizes and other
commonly problematic values.

#### `create_ramdisk.sh`
Creates a named RAM disk (tmpfs) under `/mnt` with the specified size.

#### `create_virtual_environment.sh`
Creates a Python virtual environment (by default at `env/`) and loads
dependencies from `requirements.txt`, if it exists.

#### `drop_caches.sh`
Frees the page cache and all reclaimable slab objects (e.g. inodes).

#### `find_duplicates.sh`
Finds duplicate files, given a list of paths. Note that only neighboring
duplicates are found and this operates in linear time. Typically, it is used
like so: `find ... | xargs scripts/find_duplicates.sh | ...`.

#### `git`
Applies the same operation to all of the Git repositories in the current working
directory. Especially useful when you have a large number of projects.

#### `git_author_files.sh`
Returns a list of the files touched by the given author in the Git repository in
the current working directory.

#### `git_author_line_counts.sh`
Returns a list of currently existing files touched by the given author in the
Git repository in the current working directory. Output sorted by the number of
lines contributed in each file.a

#### `git_file_authors.sh`
Returns a summary of authors of a file in the Git repository in the current
working directory.

#### `hg`
Applies the same operation to all of the Mercurial repositories in the current
working directory. Especially useful when you have a large number of projects.

#### `ssh_tunnel.sh`
Helper script for setting up SSH tunnels: it passes its arguments to `ssh`
along with options to fork it to run in the background, and heartbeat once per
minute, allowing up to 60 misses. This results in unobtrusive tunnels that are
resilient to short disruptions in the connection. For example:

	scripts/ssh_tunnel.sh -L 12222:localhost:80 ihutchinson@AAA.BBB.CCC.DDD

#### `upgrade_python3_venv.sh`
Upgrades a `requirements.txt` for a Python 3 virtual environment to the latest
versions of each of its packages, then saves the result to the target location.
