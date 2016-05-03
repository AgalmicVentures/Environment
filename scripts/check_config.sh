#!/bin/bash

set -u

NC='\033[00m'
RED='\033[1;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'

#Check for generated SSH keys
if [ -e ~/.ssh/id_rsa.pub ]
then
	echo -e "${GREEN}SSH key detected${NC}"
else
	echo -e "${RED}No SSH key detected (run setup.sh or ssh-keygen)!${NC}"
fi

#Check OS before hardware
UNAME=`uname`
if [[ $UNAME == "Linux" ]]
then
	echo -e "${GREEN}Detected Linux${NC}"
elif [[ $UNAME == "FreeBSD" ]]
then
	echo -e "${GREEN}Detected FreeBSD${NC}"
elif [[ $UNAME == "Darwin" ]]
then
	echo -e "${RED}Detected OS X -- script only works on Linux currently${NC}"
	exit
else
	echo -e "${RED}Detected unknown OS '$UNAME' -- script only works on Linux currently${NC}"
	exit 1
fi

#Check for single core (bad VM?)
NUM_CPUS=`cat /proc/cpuinfo | grep processor | wc -l`
if [[ $NUM_CPUS -gt 1 ]]
then
	echo -e "${GREEN}Detected $NUM_CPUS CPUs${NC}"
else
	echo -e "${YELLOW}Detected only 1 CPU!${NC}"
fi

#Display more information about the NUMA topology
numactl -H

#Check for too little RAM (bad VM?)
MEMORY_KB=`cat /proc/meminfo | grep MemTotal | awk '{print $2}'`
if [[ $MEMORY_KB -gt 4000000 ]]
then
	echo -e "${GREEN}Detected ${MEMORY_KB}K of memory${NC}"
elif [[ $MEMORY_KB -gt 2000000 ]]
then
	echo -e "${YELLOW}Detected low memory: ${MEMORY_KB}K${NC}"
else
	echo -e "${RED}Detected very low memory: ${MEMORY_KB}K${NC}"
fi

#Check if sysctl limits are reasonable

#Max network buffer sizes
RMEM_MAX=`sysctl -n net.core.rmem_max`
if [[ $RMEM_MAX -gt 4000000 ]]
then
	echo -e "${GREEN}Detected ${RMEM_MAX} max network read buffer size${NC}"
elif [[ $RMEM_MAX -gt 1000000 ]]
then
	echo -e "${YELLOW}Detected low max network read buffer size (net.core.rmem_max): ${RMEM_MAX}${NC}"
else
	echo -e "${RED}Detected very low max network read buffer size (net.core.rmem_max): ${RMEM_MAX}${NC}"
fi

WMEM_MAX=`sysctl -n net.core.wmem_max`
if [[ $WMEM_MAX -gt 4000000 ]]
then
	echo -e "${GREEN}Detected ${WMEM_MAX} max network write buffer size${NC}"
elif [[ $WMEM_MAX -gt 1000000 ]]
then
	echo -e "${YELLOW}Detected low max network write buffer size (net.core.wmem_max): ${WMEM_MAX}${NC}"
else
	echo -e "${RED}Detected very low max network write buffer size (net.core.wmem_max): ${WMEM_MAX}${NC}"
fi

#Default network buffer sizes
RMEM_DEFAULT=`sysctl -n net.core.rmem_default`
if [[ $RMEM_DEFAULT -gt 4000000 ]]
then
	echo -e "${GREEN}Detected ${RMEM_DEFAULT} default network read buffer size${NC}"
elif [[ $RMEM_DEFAULT -gt 1000000 ]]
then
	echo -e "${YELLOW}Detected low default network read buffer size (net.core.rmem_default): ${RMEM_DEFAULT}${NC}"
else
	echo -e "${RED}Detected very low default network read buffer size (net.core.rmem_default): ${RMEM_DEFAULT}${NC}"
fi

WMEM_DEFAULT=`sysctl -n net.core.wmem_default`
if [[ $WMEM_DEFAULT -gt 4000000 ]]
then
	echo -e "${GREEN}Detected ${WMEM_DEFAULT} default network write buffer size${NC}"
elif [[ $WMEM_DEFAULT -gt 1000000 ]]
then
	echo -e "${YELLOW}Detected low default network write buffer size (net.core.wmem_default): ${WMEM_DEFAULT}${NC}"
else
	echo -e "${RED}Detected very low default network write buffer size (net.core.wmem_default): ${WMEM_DEFAULT}${NC}"
fi
