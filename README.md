# Environment
This repository contains the Agalmic Ventures standard development environment.
This includes everything from needed for developing systems from scratch and
operationalizing them, including standard configuration files, code templates
and examples, scripts and tools to support development, and Ansible playbooks
for instantiating standard infrastructure.

## What's Included

### Configs (`configs/`)
Standard configuration files for `bash`, `vim`, etc. which are installed as a
part of the standard environment.

### C++ (`cpp/`)
Snippets of generally useful C++. Some are standalone programs which maybe be
executed directly, as if they were scripts (see `cpp/README.md` for details).

### Licenses (`licenses/`)
Copies of the MIT license in a variety of language formats are included for use
with the `Prepend.py` script (see below).

### Playbooks (`playbooks/`)
Ansible playbooks for configuring development and production environments,
including security hardening and standard installations of common services.

### Scripts (`scripts/`)
Python and shell scripts for automating common development and operational
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
The simplest way to get started is to clone this repository.

To install this environment (symlinks, etc.) for a user, run the
`playbooks/create_user.yml` Ansible playbook on the desired user@host. It
will clone the repository to `~/Code/OpenSource/Environment` and set
everything up so configurations will Just Work.
