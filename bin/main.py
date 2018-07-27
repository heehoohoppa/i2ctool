import helperFunctions as helper
import SMWClient as client
import csvlib as csvlib

print "I2C Interface Program"
print "Property of: Cray"
print "Made by the best intern ever: Will Scott"
print "Use \"help\" at any time to get the corresponding commands"
print ""

################# global usage variables #####################
global bus_num
global dev_num
bus_num = "-1"
dev_num = "00"
csvfilename = "../Device List.csv"
exh_bus_list = csvlib.csv_to_bus_list(csvfilename)

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
	
	if args[0] == "get_board":
		pass

	elif args[0] == "read_excel":
		pass 	# may be best to leave as a CSV

	elif args[0] == "goto_bus":
		try:
			bus_num = args[1]
			# Check to see if the bus exists
			killswitch = smw.callCmd(["cd /dev/bus/i2c/devices/i2c-" + bus_num])  		# TODO: double check that an empty cd actually overrides the output
			if killswitch != "":
				print "Error: invalid bus number"
				bus_num = -1
			else:
				return "bus"
		except:
			# try/except will ensure we actually have a args[1]
			print "usage: goto_bus <busnum>"
	
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
		active_bus_list = []
		for i in buses:
			index = csvlib.find_index(i, exh_bus_list)
			if index != -1:
				active_bus_list.append(exh_bus_list[index])	
		print active_bus_list

	elif args[0] == "walk_bus":
		helper.walk_bus(smw, args[1])
	
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
	
	elif args[0] == "get_ps":
		pass
	
	elif args[0] == "adv_ps":
		pass
	
	elif args[0] == "cmd":
		# TODO: double check this works as intended with the callCmd method
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
	
	if args[0] == "walk" or args[0] == "walk_bus":
		# TODO: have a -p/-m flag for "only display present/missing devices"
		# TODO: Actually compare these devices to everything else
		try:
			if args[1] == "-p":
				helper.walk_bus(smw, bus_num, exh_bus_list)
			elif args[1] == "-m":
				helper.walk_bus(smw, bus_num, exh_bus_list)
		except:
			helper.walk_bus(smw, bus_num, exh_bus_list)
		
	
	elif args[0] == "get_device":
		pass
	
	elif args[0] == "disp_types":
		pass
	
	elif args[0] == "exit":
		return "exit"
	
	elif args[0] == "return":
		pass
	
	elif args[0] == "get_ps":
		pass
	
	elif args[0] == "adv_ps":
		pass
	
	elif args[0] == "anc":
		pass
	
	elif args[0] == "help" or args[0] == "-h":
		pass
	
	else:
		print args[0] + ": invalid command"

	return "bus"

def device_level(argument, smw):
	args = argument.split()
	
	if args[0] == "printregs":
		pass
	
	elif args[0] == "watchregs":
		pass
	
	elif args[0] == "get":
		pass
	
	elif args[0] == "exit":
		pass
	
	elif args[0] == "return":
		pass
	
	elif args[0] == "get_ps":
		pass
	
	elif args[0] == "adv_ps":
		pass
	
	elif args[0] == "anc":
		pass
	
	elif args[0] == "help" or args[0] == "-h":
		pass
	
	else:
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
		input_string = raw_input(["dev" + bus_num + "-0x" + str(dev_num) + "> "])
		tracker = device_level(input_string, smw)


