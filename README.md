
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

### `check_config.sh`
Checks the configuration of the system, including network buffer sizes and other commonly problematic values.

### `create_ramdisk.sh`
Creates a named RAM disk (tmpfs) under `/mnt` with the specified size.

### `colors.sh`
Defines a variety of formatting specifications with [ANSI codes](https://en.wikipedia.org/wiki/ANSI_escape_code).

### `git`
Applies the same operation to all of the repositories in the current working directory. Especially usefu when you have a large number of projects.
