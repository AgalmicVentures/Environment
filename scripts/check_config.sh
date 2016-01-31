#!/bin/bash

NC='\033[00m'
RED='\033[1;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'

#Check for generated SSH keys
if [ ! -e ~/.ssh/id_rsa.pub ]
then
	echo -e "${RED}No SSH key detected (run setup.sh or ssh-keygen)!${NC}"
fi

#Check OS before hardware
UNAME=`uname`
if [[ $UNAME == "Darwin" ]]
then
	echo -e "${RED}Detected OS X -- script only works on Ubuntu currently${NC}"
	exit
fi

#Check for single core (bad VM?)
NUM_CPUS=`cat /proc/cpuinfo | grep processor | wc -l`
if [[ $NUM_CPUS -gt 1 ]]
then
	echo -e "${GREEN}Detected $NUM_CPUS CPUs${NC}"
else
	echo -e "${YELLOW}Detected only 1 CPU!${NC}"
fi

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

#Check if sysctl limits are reasonable (esp. network buffers)
RMEM_MAX=`sysctl -n net.core.rmem_max`
if [[ $RMEM_MAX -gt 4000000 ]]
then
	echo -e "${GREEN}Detected ${RMEM_MAX} network read buffer${NC}"
elif [[ $RMEM_MAX -gt 1000000 ]]
then
	echo -e "${YELLOW}Detected low network read buffer (net.core.rmem_max): ${RMEM_MAX}${NC}"
else
	echo -e "${RED}Detected very low network read buffer (net.core.rmem_max): ${RMEM_MAX}${NC}"
fi

WMEM_MAX=`sysctl -n net.core.wmem_max`
if [[ $WMEM_MAX -gt 4000000 ]]
then
	echo -e "${GREEN}Detected ${WMEM_MAX} network write buffer${NC}"
elif [[ $WMEM_MAX -gt 1000000 ]]
then
	echo -e "${YELLOW}Detected low network write buffer (net.core.wmem_max): ${WMEM_MAX}${NC}"
else
	echo -e "${RED}Detected very low network write buffer (net.core.wmem_max): ${WMEM_MAX}${NC}"
fi

