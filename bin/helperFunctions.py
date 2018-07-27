# from csiclient import CSISocket
import csv
import csvlib as csvlib

# Looks like csi.client("i2cdetect") is how to do this

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
def walk_bus(smw, bus_number, exh_bus_list):
	# TODO: display what each device is. We may want to scrap this method and re-do it
	#   	by searching the i2c-xxx directories
	# text_holder = call(["i2cdetect", "-y", "bus_number"])
	
	text_holder = smw.callCmd(["/usr/sbin/i2cdetect -y " + bus_number])
	text_holder = text_holder[(text_holder.find("\n")+1):]
	arr = text_holder.split()
	addresses = []
	# Parse the text_holder, stick the addresses found in 'addresses'
	for i in range(0,len(arr)):
		if arr[i] != "--" and arr[i].find(":") == -1:
			addresses.append(arr[i])

	# Get your current bus
	index = csvlib.find_index(bus_number, exh_bus_list)
	current_bus = exh_bus_list[index] 	# TODO: make sure this actually COPIES it, not points at it
	# Iterate over the addresses and print them out
	for i in addresses:
		print current_bus.getDevice(i)



def compare_addresses(input_addresses, stored_addresses):
	pass



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
def populate_device_list(csv_file, bus_nums):
	device_list = []

	with open(csv_file, 'rb') as csvfile:
		csvline = csv.reader(csvfile, dialect='excel')
		next(csvline, None)

		for row in csvline:
			if row[0]:
				i2c_bus = int(row[0])
				i2c_bus_name = row[1]
			if i2c_bus in bus_nums and not row[0]:
				address = int(row[2], 16)
				device_name = row[3]
				part_num = row[4]
				file_path = row[5]
				device_list.append(device_lists.Device(i2c_bus, i2c_bus_name, address, file_path))


	return device_list



##################################################################
######################## Help Printers ###########################
def board_help():
	print "gonna need a lot of very pretty print statements here"

def bus_help():
	pass

def dev_help():
	pass