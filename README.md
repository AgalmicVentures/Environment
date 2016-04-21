
# Development Environment
This repository contains basic helper scripts and configuration files needed to setup a development environment on a variety of platforms.

## Configs

### `.bashrc`
Many features including:
* Custom colorized prompt with timestamp and current working directory
* Warnings on non-zero return values
* Aliases for common commands, e.g. `ll` for `ls -lAh`

### `.hgrc`
Mercurial default settings.

### `.psqlrc`
A few simple interface improvements to `psql` (the PostgreSQL prompt), such as query timing.

### `.vimrc`
Lots of ease-of-use improvements for `vim`: backspace works as expected, left arrow can scroll back lines, etc.

## Scripts

### `augment_lines.py`
Augments lines of text (e.g. with a time stamp).

### `check_config.sh`
Checks the configuration of the system, including network buffer sizes and other commonly problematic values.

### `create_ramdisk.sh`
Creates a named RAM disk (tmpfs) under `/mnt` with the specified size.

### `colors.sh`
Defines a variety of formatting specifications with [ANSI codes](https://en.wikipedia.org/wiki/ANSI_escape_code).

### `git_author_files.sh`
Returns a list of the files touched by the given author in the Git repository in the current working directory.

### `git_file_authors.sh`
Returns a summary of authors of a file in the Git repository in the current working directory.

### `git_find_author.sh`
Returns a list of currently existing files touched by the given author in the Git repository in the current working directory. Output sorted by the number of lines contributed in each file.a

### `hg`
Applies the same operation to all of the Mercurial repositories in the current working directory. Especially useful when you have a large number of projects.
