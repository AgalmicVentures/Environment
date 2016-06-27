#!/bin/bash

#NOTE: This script may need to be run under sudo

apt-get install ufw

ufw allow ssh #Could also use the port number, 22
