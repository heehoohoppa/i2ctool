#!/bin/bash

# This script manages the i2c.py file

#################################################################
################## pull I2C bus/addr pairs ######################

str=`cat i2ctestfile.txt`

# TODO: check the string to make sure it worked (what's the message if i2cdetect fails?)

# Remove the header of i2cdetect
IFS=$'\n'
str=${str#*busses:}

unset bus_numbers

# extract the bus numbers
for line in $str[@]
do
	line=${line%smbus*}
	line=${line#*i2c-}
	line=${line%%" "*}
	bus_numbers=( "${bus_numbers[@]}" "${line[*]}")
done

IFS=$' '
echo "${bus_numbers[@]}"


# screen the associated addresses on each bus, pass to a python script
#  to avoid messing with 2d arrays

str2=`cat i2ctestfile2.txt`

# TODO: check to make sure it worked



