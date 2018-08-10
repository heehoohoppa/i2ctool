import helperFunctions as helper
import SMWClient as client
import csvlib as csvlib
from copy import deepcopy

print ""
print "I2C Interface Program"
print "Property of: Cray"
print "Made by the best intern ever: Will Scott"
print "Use \"help\" at any time to get the corresponding commands"
print ""

################## global usage variables ####################
bus_num = "-1"
dev_num = "00"
bus_obj = csvlib.bus("0","empty")
dev_obj = csvlib.device("0", "0", "empty", "empty", "none")
csvfilename = "Device List.csv"
exh_bus_list = helper.csv_to_bus_list(csvfilename)

################# Initiate your SMW class ####################
out = raw_input("cname: ")
smw = client.SMWClient(out)
while smw.checkCname() == 0:
	print "Please put valid cname"
	# circle until we get a valid cname
	out = raw_input("cname: ")
	if out == "exit":
		exit()
	smw = client.SMWClient(out)


##############################################################
####### Functions to handle the command line interface #######

def board_level(argument, smw):
	args = argument.split()
	global bus_num
	global dev_num
	global bus_obj
	
	if args[0] == "goto_bus":
		try:
			bus_num = args[1]
		except:
			print "usage: goto_bus <busnum>"
			return "board"
		
		try:
			holder = smw.callCmd("cd /sys/bus/i2c/devices/i2c-" + str(bus_num))
			if holder == "":
				index = helper.find_index(bus_num, exh_bus_list)
				bus_obj = exh_bus_list[index]
				return "bus"
			else:
				print "goto_bus failed (1)"
				bus_num = "-1"
				return "board"
		except:
			print "goto_bus failed (2)"
			bus_num = "-1"
			return "board"
		return "bus"
	
	elif args[0] == "buses" or args[0] == "bus_list":
		# TODO: Give this function a whirl
		# TODO: offload all of this into helperFunctions, this should literally just be function calls
		try:
			if args[1] == "-a":
				helper.print_all_buses(smw)
			else:
				buses = helper.get_buses(smw)
		except:	
			buses = helper.get_buses(smw)

		for i in buses:
			index = helper.find_index(i, exh_bus_list)
			if index != -1:
				print exh_bus_list[index]

	elif args[0] == "walk_bus":
		try:
			helper.walk_bus(smw, args[1], exh_bus_list)
		except:
			print "usage: walk_bus <busnum>"

	elif args[0] == "pop_by_type":
		pass
	
	elif args[0] == "exit":
		return "exit"
	
	elif args[0] == "return":
		return "exit"
	
	elif args[0] == "set_cname" or args[0] == "cname":
		temp_smw = client.SMWClient(args[1])
		if temp_smw.checkCname == 0:
			print "Error: Invalid cname. cname not changed"
		else:
			smw = temp_smw
	
	elif args[0] == "get_ps" or args[0] == "node_ps":
		try:
			print smw.callCmd("/opt/cray/bin/node_ps " + args[1])
		except:
			print "usage: [ get_ps || node_ps ] <node>"

	elif args[0] == "adv_ps" or args[0] == "ss_pu":
		try:
			smw.callCmd("/opt/cray/bin/ss_pu " + args[1])
		except:
			print "usage: [ adv_ps || ss_pu ] <node>"
	
	elif args[0] == "cmd":
		args.pop(0)
		args = " ".join(args)
		print smw.callCmd(args)
	
	elif args[0] == "help" or args[0] == "-h":
		helper.board_help()
	
	else:
		print args[0] + ": invalid command"
	
	return "board"

def bus_level(argument, smw):
	args = argument.split()
	global bus_num
	global dev_num
	global bus_obj
	
	########## check the bus object ###########
	if bus_num != bus_obj.getNum():
		bus_obj = helper.create_bus(smw, bus_num, exh_bus_list)
		# why is this shit necessary...?

	if args[0] == "walk" or args[0] == "walk_bus":
		try:
			if args[1] == "-p":
				helper.walk_bus(smw, bus_num, exh_bus_list, 'present')
			elif args[1] == "-m":
				helper.walk_bus(smw, bus_num, exh_bus_list, 'missing')
		except:
			helper.walk_bus(smw, bus_num, exh_bus_list)
	
	if args[0] == "info":
		index = helper.find_index(bus_num, exh_bus_list)
		exh_bus_list[index].printInfo()

	elif args[0] == "get_device":
		try:
			address = args[1]
		except:
			print "usage: get_device <hexaddr>"
		helper.print_device(smw, bus_num, address)

	elif args[0] == "goto_device":
		try:
			address = args[1]
		except:
			print "usage goto_device <hexaddr>"
			return "bus"
		#TODO: figure out what command will help us check if it's present
		# print smw.callCmd("/usr/sbin/i2cget -y %s 0x%s 0x00" % (bus_num, address))
		out = smw.callCmd("/usr/sbin/i2cget -y %s 0x%s 0x00" % (bus_num, address))
		if out[0:5] == "Error":
			print "device not found on bus"
			return "bus"
		elif out[0:2] == "0x":
			dev_num = address
			index = helper.find_index(bus_num, exh_bus_list)
			bus_obj = exh_bus_list[index]
			return "device"
		else:
			print "???"
			dev_num = address
			index = helper.find_index(bus_num, exh_bus_list)
			bus_obj = exh_bus_list[index]
			return "device"

	
	elif args[0] == "disp_types":
		pass
	
	elif args[0] == "exit":
		return "exit"
	
	elif args[0] == "return" or args[0] == "back" or args[0] == "up":
		return "board"
	
	elif args[0] == "get_ps" or args[0] == "node_ps":
		try:
			smw.callCmd("node_ps " + args[1])
		except:
			print "usage: [ get_ps || node_ps ] <node>"

	elif args[0] == "adv_ps" or args[0] == "ss_pu":
		try:
			smw.callCmd("ss_pu " + args[1])
		except:
			print "usage: [ adv_ps || ss_pu ] <node>"
	
	elif args[0] == "cmd":
		args.pop(0)
		args = " ".join(args)
		print smw.callCmd(args)
	
	elif args[0] == "help" or args[0] == "-h":
		helper.bus_help()
	
	else:
		print args[0] + ": invalid command"

	return "bus"

def device_level(argument, smw):
	args = argument.split()
	global bus_num
	global dev_num
	global bus_obj
	global dev_obj
	
	dev_obj = bus_obj.getDevice(dev_num)

	if args[0] == "printregs" or args[0] == "print_regs":
		# bus_obj.printDevices()
		# dev_obj.getAddr()
		dev_obj.print_regs(smw)
	
	elif args[0] == "watchregs" or args[0] == "watch_regs":
		dev_obj.watch_regs(smw)
	
	elif args[0] == "info":
		# TODO: make sure every bus/device object has the relevant info
		#  that's in the CSV. User shouldn't ever have to see the CSV.
		dev_obj.printInfo()
	
	elif args[0] == "exit":
		return "exit"
	
	elif args[0] == "return":
		dev_num = "00"
		return "bus"
	
	elif args[0] == "get_ps":
		pass
	
	elif args[0] == "adv_ps":
		pass
	
	elif args[0] == "cmd":
		args.pop(0)
		args = " ".join(args)
		print smw.callCmd(args)
	
	elif args[0] == "help" or args[0] == "-h":
		helper.dev_help()
	
	else:
		dev_args = [args[0], smw]
		for i in args[1:]:
			dev_args.append(i)
		try:
			if dev_obj.handleCommand(dev_args):
				return "device"
			else:
				print args[0] + ": invalid command"
		except:
			print args[0] + ": invalid command"

	return "device"


##################### Main ######################
input_string = raw_input("> ")
tracker = board_level(input_string, smw)

while tracker != "exit":
	if tracker == "board":
		input_string = raw_input("> ")
		tracker = board_level(input_string, smw)
	elif tracker == "bus":
		input_string = raw_input("bus" + bus_num + "> ")
		tracker = bus_level(input_string, smw)
	elif tracker == "device":
		input_string = raw_input(bus_num + "-0x" + str(dev_num) + "> ")
		tracker = device_level(input_string, smw)


