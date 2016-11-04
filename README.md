
# Development Environment
This repository contains basic helper scripts and configuration files needed to setup a development environment on a variety of platforms.

## Configs

### `.bashrc`
Many features including:
* Custom colorized prompt with timestamp and current working directory
* Warnings on non-zero return values
* Aliases for common commands, e.g. `ll` for `ls -lAh`

### `.gitconfig`
Git default settings.

### `.hgrc`
Mercurial default settings.

### `.psqlrc`
A few simple interface improvements to `psql` (the PostgreSQL prompt), such as query timing.

### `.vimrc`
Lots of ease-of-use improvements for `vim`: backspace works as expected, left arrow can scroll back lines, etc.

## Scripts

### Python

#### `AugmentLines.py`
Augments lines of text (e.g. with a time stamp).

#### `CsvToJson.py`
Converts CSV documents to JSON with a variety of transformation options.

#### `GenerateConfigs.py`
Generates the a set of JSON configurations given a base configuration and a second JSON object with lists of values for parameters (`{"a": [1, 2], "b": [3, 4, 5]}`). Useful with `Parallelize.py` and `Template.py`.

#### `JsonToXml.py`
Converts JSON documents to XML with a variety of transformation options./'/

#### `Parallelize.py`
Given a process name, run ID, and set of configurations, runs the process in parallel over all of the configurations. For example,
`./Parallelize.py ./xyz run134 config1 config2 config3 config4 config5` will run `./xyz1 run134 config1`, ..., `./xyz1 run134 config5`.
It will use as many CPU's as are available. Useful with `GenerateConfigs.py` and `Template.py`.

#### `RandomSleep.py`
Sleeps for a random amount of time given a minimum and maximum bound. Useful for randomizing the start time of processes.

#### `Template.py`
Instantiates a template with values from a JSON configuration. Useful with `GenerateConfigs.py` and `Parallelize.py`.

### Shell

#### `check_config.sh`
Checks the configuration of the system, including network buffer sizes and other commonly problematic values.

#### `create_ramdisk.sh`
Creates a named RAM disk (tmpfs) under `/mnt` with the specified size.

#### `colors.sh`
Defines a variety of formatting specifications with [ANSI codes](https://en.wikipedia.org/wiki/ANSI_escape_code).

#### `drop_caches.sh`
Frees the page cache and all reclaimable slab objects (e.g. inodes).

#### `git`
Applies the same operation to all of the Git repositories in the current working directory. Especially useful when you have a large number of projects.

#### `git_author_files.sh`
Returns a list of the files touched by the given author in the Git repository in the current working directory.

#### `git_author_line_counts.sh`
Returns a list of currently existing files touched by the given author in the Git repository in the current working directory. Output sorted by the number of lines contributed in each file.a

#### `git_file_authors.sh`
Returns a summary of authors of a file in the Git repository in the current working directory.

#### `hg`
Applies the same operation to all of the Mercurial repositories in the current working directory. Especially useful when you have a large number of projects.

#### `setup_firewall.sh`
Installs and configures a basic firewall (may need to run as root).

