# from csiclient import CSISocket
import csv
import csvlib as csvlib
from copy import deepcopy


####################################################################
########################### Board Levels ###########################
def get_buses(smw):
	# Function returns a list of the bus numbers on the device and
	#  the name of each
	text_holder = smw.callCmd("/usr/sbin/i2cdetect -l")

	# go through each line, pull out the bus number
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
	# TODO: display what each device is. Gonna do a lot of i2cget and i2cdump
	
	text_holder = smw.callCmd("/usr/sbin/i2cdetect -y " + bus_number)
	text_holder = text_holder[(text_holder.find("\n")+1):]
	arr = text_holder.split()
	addresses = []
	# Parse the text_holder, stick the addresses found in 'addresses'
	for i in range(0,len(arr)):
		if arr[i] != "--" and arr[i].find(":") == -1:
			addresses.append(arr[i])

	# Get your current bus
	index = csvlib.find_index(bus_number, exh_bus_list)
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

def create_bus(smw, bus_num, exh_bus_list):
	index = csvlib.find_index(bus_num, exh_bus_list)
	if index != -1:
		bus_name = exh_bus_list[index].getName()
		path = exh_bus_list[index].getPath()
	else:
		print "invalid bus number"
		return
	out_bus = csvlib.bus(bus_num, bus_name, path)

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



##################################################################
######################### Device Levels ##########################
''' Method to read through a CSV file with the column format:
	  bus | bus name | addr | device name | part# | path
	Where bus (int) is the i2c bus number, bus name (str) is the arbitrary name assigned to 
	the bus, addr (int) is the address - stored as a hex string in the csv converted to int
	in this method, device name (str) is the arbitrary device name, part# (str) is the Cray 
	or manufacturer assigned part#, path (str) is the filepath on the PDC for accessing the 
	i2c	device.

	Args: csv_file = "your_file.csv"
		  bus_nums = list of buses (int) fed from the get_bus_numbers() method

	Return: list of class Device().
'''
def check_device(smw, bus, address):
	pass

def print_device(smw, bus, address):
	pass # First check if the device 




##################################################################
######################## Help Printers ###########################
def board_help():
	print """get_board
	- prints the type of board the user has logged onto
bus_list
	- lists all of the buses
goto_bus <busnum>
	- move to the bus level

"""

def bus_help():
	print "gonna need a lot of very pretty print statements here"

def dev_help():
	print "gonna need a lot of very pretty print statements here"