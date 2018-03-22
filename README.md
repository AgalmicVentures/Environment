# Environment
This repository contains the Agalmic Ventures standard development environment.
Everything from install scripts and configuration files to basic development
and operations scripts are included.

## What's Included

### Configs (`configs/`)
Standard configuration files for `bash`, `vim`, etc. which are installed as a
part of the standard environment.

### Licenses (`licenses/`)
Copies of the MIT license in a variety of language formats are included for use
with the `Prepend.py` script (see below).

### Playbooks (`playbooks/`)
Ansible playbooks for configuring development and production environments,
including security hardening and standard installations of common services.

### Scripts (`scripts/`)
Python and shell scripts for automating common development and operations
tasks.

For example, there is a pipeline for running parallel simulations by
generating all combations of values as JSON objects, using those to instantiate
templates, then running a process with each configuration, up to the maximum
parallelism supported by the processor.

### SQL (`sql/`)
Stubs of SQL scripts for setting up a database environment in PostgreSQL.

### System (`system/`)
System files, usually for Linux, such as `udev` rules.

## Getting Started
The best way to install this environment is to run the
`playbooks/create_user.yml` Ansible playbook on the desired user@host.  It
will copy all files to where they need to be and install necessary symlinks so
configurations will just work.

To bootstrap the first copy, clone this repository to
`~/Code/OpenSource/Environment` and run the playbook on the local user.
