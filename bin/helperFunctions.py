# from csiclient import CSISocket
from csv import reader
import csvlib as csvlib
from copy import deepcopy


####################################################################
########################### Board Levels ###########################
def get_buses(smw):
	# Function returns a list of the bus numbers on the device and
	#  the name of each
	text_holder = smw.callCmd("/usr/sbin/i2cdetect -l")

	# go through each line, pull out the bus number
	# this is just a bunch of string parsing
	bus_nums = []
	index = text_holder.find("\n")
	
	while index != -1:
		try:
			bus_nums.append(int(text_holder[4:7]))
		except:
			bus_nums.append(int(text_holder[4:6]))
		text_holder = text_holder[index+1:]
		index = text_holder.find("\n")

	return bus_nums

def print_all_buses(smw):
	# TODO: This whole function
	present_buses = get_buses(smw)
	return present_buses



###################################################################
########################### Bus Levels ############################
def walk_bus(smw, bus_number, exh_bus_list, pm='none'):
	
	text_holder = smw.callCmd("/usr/sbin/i2cdetect -y " + bus_number)
	text_holder = text_holder[(text_holder.find("\n")+1):]
	arr = text_holder.split()
	addresses = []
	# Parse the text_holder, stick the addresses found in 'addresses'
	for i in range(0,len(arr)):
		if arr[i] != "--" and arr[i].find(":") == -1:
			addresses.append(arr[i])

	# Get your current bus
	index = find_index(bus_number, exh_bus_list)
	current_bus = deepcopy(exh_bus_list[index])
	# Set the presence of the devices
	current_bus.setDevicePresences(addresses)
	# Iterate over the addresses and print them out
	if pm == 'none':
		current_bus.printDevices()
	elif pm == 'present':
		current_bus.printPresentDevices()
	elif pm == 'missing':
		current_bus.printMissingDevices()

	# print the unknown devices
	unknown_addresses = current_bus.getMissingDevices(addresses)
	if len(unknown_addresses) > 0:
		for addr in unknown_addresses:
			try:
				if len(addr) == 1:
					filepath = "/sys/bus/i2c/devices/i2c-" + str(bus_number) + "/" + str(bus_number) + "000" + str(addr) + "/name"
				elif len(addr) == 2:
					filepath = "/sys/bus/i2c/devices/i2c-" + str(bus_number) + "/" + str(bus_number) + "00" + str(addr) + "/name"
				elif len(addr) == 3:
					filepath = "/sys/bus/i2c/devices/i2c-" + str(bus_number) + "/" + str(bus_number) + "0" + str(addr) + "/name"
				name = smw.callCmd("cat " + filepath)
				print "    0x" + addr + ":(+) " + name
			except:
				print "    0x" + addr + ":(+) present, but can't find name"
	return

# incomplete function
# Designed to copy an instance of exh_bus_list and set the device.isPresent variables. I think.
def create_bus(smw, bus_num, exh_bus_list):
	index = find_index(bus_num, exh_bus_list)
	if index != -1:
		bus_name = exh_bus_list[index].getName()
	else:
		print "invalid bus number"
		return
	out_bus = csvlib.bus(bus_num, bus_name)

	# Iterate and add the devices 
	text_holder = smw.callCmd("/usr/sbin/i2cdetect -y " + bus_num)
	text_holder = text_holder[(text_holder.find("\n")+1):]
	arr = text_holder.split()
	addresses = []
	# Parse the text_holder, stick the addresses found in 'addresses'
	for i in range(0,len(arr)):
		if arr[i] != "--" and arr[i].find(":") == -1:
			addresses.append(arr[i])
	ref_addrs = exh_bus_list[index].getAddresses()
	# Okay we have the addresses, now we just need to populate it and get the corresponding properties
	for a in ref_addrs:
		pass
	return out_bus



#################################################################
######################## Useful Functions #######################
def csv_to_bus_list(filename):
    bus_list = []
    current_bus = '-1'
    with open(filename, 'rb') as csvfile:       # 'rb'?
		iterable = reader(csvfile)
		iterable.next()
		for row in iterable:
			if(row[0] != current_bus):
				bus_list.append(csvlib.bus(row[0], row[1]))
				bus_list[len(bus_list)-1].addDevice(row[2], row[3], row[4], row[5])
				current_bus = row[0]
			else:
				bus_list[len(bus_list)-1].addDevice(row[2], row[3], row[4], row[5])
    return bus_list

# Function to find the index in exh_bus_list in which the bus_number resides.
def find_index(bus_num, bus_list):
    # Gonna binary search this bitch
    bus_num = int(bus_num)
    L = 0
    R = len(bus_list) - 1
    while L < R:
        tracker = int((L+R)/2)
        if int(bus_list[tracker].getNum()) < bus_num:
            L = tracker + 1
        elif int(bus_list[tracker].getNum()) > bus_num:
            R = tracker - 1
        else:
            return tracker
    return -1


##################################################################
######################## Help Printers ###########################
def global_help():
	print """
			Global Commands
help
	- display available commands
exit
	- exit the program
return
	- move "up" in the heirarchy (e.g. move from bus to board, or device to bus)
set_cname
	- change the system the program is working on
cmd
	- pass a raw command to the BC (as if you were xtlogin'd)
"""

def board_help():
	global_help()
	print """
			Board-Level Commands
get_board
	- prints the type of board the user has logged onto
bus_list || buses
	- lists all of the present buses
goto_bus <busnum>
	- move to the bus level
walk_bus <busnum>
	- list the devices present on the bus
"""

def bus_help():
	global_help()
	print """
			Bus-Level Commands
walk_bus || walk [-p/-m]
	- list the devices, present or not present, on the bus.
	-  with the -p flag, will only list present devices
	-  with the -m flag, will only list missing devices
get_device <hexaddr>
	- return basic information on the device at <hexaddr>
goto_device <hexaddr>
	- move to the device level
"""

def dev_help():
	global_help()
	print """
			Device-Level Commands
print_regs
	- read essential registers from the device
print_regs -a
	- output all raw register values
watch_regs
	- set up a continuous stream to view register values

		Commands to Voltage Regulators
	(note: supported commands depend on chip manufacturer)
get_vout
get_vout_status
get_vin
get_iout
get_iout_status
get_temperature
get_temperature_status
get_power
get_status
	- read the device status word
print_cmds
	- prints a list of hex values and register pairs
raw_cmd <hexval>
	- send a raw hex value and display the output

"""



