#!/bin/bash

# Copyright (c) 2015-2019 Agalmic Ventures LLC (www.agalmicventures.com)
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

set -u

readonly NC='\033[00m'
readonly RED='\033[1;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'

#Check for generated SSH keys
if [ "$(find ~/.ssh -name 'id_*.pub')" != "" ] ; then
	echo -e "${GREEN}SSH key detected${NC}"
else
	echo -e "${RED}No SSH key detected (run ssh-keygen)!${NC}"
fi

#Check if ulimit limits are reasonable
readonly CORE_SIZE_LIMIT=$(ulimit -c)
if [[ $CORE_SIZE_LIMIT == "unlimited" ]] ; then
	echo -e "${GREEN}Core files enabled${NC}"
elif [[ $CORE_SIZE_LIMIT == "0" ]] ; then
	echo -e "${RED}Core files disabled -- run 'ulimit -c unlimited' to enable them${NC}"
else
	echo -e "${YELLOW}Core file size limited ${CORE_SIZE_LIMIT} -- run 'ulimit -c unlimited' to remvoe this limit${NC}"
fi

readonly FILE_SIZE_LIMIT=$(ulimit -f)
if [[ $FILE_SIZE_LIMIT == "unlimited" ]] ; then
	echo -e "${GREEN}No file size limit${NC}"
else
	echo -e "${RED}File size limited to ${FILE_SIZE_LIMIT} -- run 'ulimit -f unlimited' to remvoe this limit${NC}"
fi

readonly OPEN_FILES_LIMIT=$(ulimit -n)
if [[ $OPEN_FILES_LIMIT == "unlimited" || $OPEN_FILES_LIMIT -gt 65535 ]] ; then
	echo -e "${GREEN}Max open files ${OPEN_FILES_LIMIT}${NC}"
elif [[ $OPEN_FILES_LIMIT -gt 1023 ]] ; then
	echo -e "${YELLOW}Max open files ${OPEN_FILES_LIMIT} is lowK${NC}"
else
	echo -e "${RED}Max open files ${OPEN_FILES_LIMIT} is VERY low${NC}"
fi

#Check OS before hardware
readonly UNAME=$(uname)
if [[ $UNAME == "Linux" ]] ; then
	echo -e "${GREEN}Detected Linux${NC}"
elif [[ $UNAME == "FreeBSD" ]] ; then
	echo -e "${GREEN}Detected FreeBSD${NC}"
elif [[ $UNAME == "Darwin" ]] ; then
	echo -e "${RED}Detected OS X -- script only works on Linux currently${NC}"
	exit
else
	echo -e "${RED}Detected unknown OS '$UNAME' -- script only works on Linux currently${NC}"
	exit 1
fi

#Check for single core (bad VM?)
readonly NUM_CPUS=$(grep -c processor < /proc/cpuinfo)
if [[ $NUM_CPUS -gt 1 ]] ; then
	echo -e "${GREEN}Detected $NUM_CPUS CPUs${NC}"
else
	echo -e "${YELLOW}Detected only 1 CPU!${NC}"
fi

#Display more information about the NUMA topology
numactl -H

#Check for too little RAM (bad VM?)
readonly MEMORY_KB=$(grep MemTotal < /proc/meminfo | awk '{print $2}')
if [[ $MEMORY_KB -gt 4000000 ]] ; then
	echo -e "${GREEN}Detected ${MEMORY_KB}K of memory${NC}"
elif [[ $MEMORY_KB -gt 2000000 ]] ; then
	echo -e "${YELLOW}Detected low memory: ${MEMORY_KB}K${NC}"
else
	echo -e "${RED}Detected very low memory: ${MEMORY_KB}K${NC}"
fi

#Check if sysctl limits are reasonable

#Max network buffer sizes
readonly RMEM_MAX=$(sysctl -n net.core.rmem_max)
if [[ $RMEM_MAX -gt 4000000 ]] ; then
	echo -e "${GREEN}Detected ${RMEM_MAX} max network read buffer size${NC}"
elif [[ $RMEM_MAX -gt 1000000 ]] ; then
	echo -e "${YELLOW}Detected low max network read buffer size (net.core.rmem_max): ${RMEM_MAX}${NC}"
else
	echo -e "${RED}Detected very low max network read buffer size (net.core.rmem_max): ${RMEM_MAX}${NC}"
fi

readonly WMEM_MAX=$(sysctl -n net.core.wmem_max)
if [[ $WMEM_MAX -gt 4000000 ]] ; then
	echo -e "${GREEN}Detected ${WMEM_MAX} max network write buffer size${NC}"
elif [[ $WMEM_MAX -gt 1000000 ]] ; then
	echo -e "${YELLOW}Detected low max network write buffer size (net.core.wmem_max): ${WMEM_MAX}${NC}"
else
	echo -e "${RED}Detected very low max network write buffer size (net.core.wmem_max): ${WMEM_MAX}${NC}"
fi

#Default network buffer sizes
readonly RMEM_DEFAULT=$(sysctl -n net.core.rmem_default)
if [[ $RMEM_DEFAULT -gt 4000000 ]] ; then
	echo -e "${GREEN}Detected ${RMEM_DEFAULT} default network read buffer size${NC}"
elif [[ $RMEM_DEFAULT -gt 1000000 ]] ; then
	echo -e "${YELLOW}Detected low default network read buffer size (net.core.rmem_default): ${RMEM_DEFAULT}${NC}"
else
	echo -e "${RED}Detected very low default network read buffer size (net.core.rmem_default): ${RMEM_DEFAULT}${NC}"
fi

readonly WMEM_DEFAULT=$(sysctl -n net.core.wmem_default)
if [[ $WMEM_DEFAULT -gt 4000000 ]] ; then
	echo -e "${GREEN}Detected ${WMEM_DEFAULT} default network write buffer size${NC}"
elif [[ $WMEM_DEFAULT -gt 1000000 ]] ; then
	echo -e "${YELLOW}Detected low default network write buffer size (net.core.wmem_default): ${WMEM_DEFAULT}${NC}"
else
	echo -e "${RED}Detected very low default network write buffer size (net.core.wmem_default): ${WMEM_DEFAULT}${NC}"
fi

#Check for important packages
for PACKAGE in fail2ban ufw ; do
	if dpkg -s $PACKAGE &> /dev/null ; then
		echo -e "${GREEN}${PACKAGE} installed."
	else
		echo -e "${RED}${PACKAGE} not installed."
	fi
done
