from copy import deepcopy

def lin11_to_dec(arg):
    # input will be 16-bit hex
    # output x = y * 2**n
    num = int(arg, 16)
    mask = 0b0000011111111111

    lower = num & mask
    if len(str(bin(lower))) == 13:
        # perform two's compliment operator, then take the negative
        lower = lower ^ mask
        lower += 1
        y = 0 - lower
    elif len(str(bin(lower))) > 13:
        print "error: greater than 11 bits for lower"
    else:
        y = lower

    mask = 0b1111100000000000
    upper = num & mask
    if len(str(bin(upper))) == 7:
        # perform two's compliment operator, then take the negative
        upper = upper ^ mask
        upper += 1
        n = 0 - upper
    elif len(str(bin(upper))) > 7:
        print "error: greater than 5 bits for upper"
    else:
        n = upper

    return (y * 2**n)

def lin16_to_dec(arg):
    # input will be 16-bit hex
    # output x = y * 2**n
    num = int(arg, 16)
    mask = 0b0000011111111111

    lower = num & mask
    if len(str(bin(lower))) == 13:
        # perform two's compliment operator, then take the negative
        lower = lower ^ mask
        lower += 1
        y = 0 - lower
    elif len(str(bin(lower))) > 13:
        print "error: greater than 11 bits for lower"
    else:
        y = lower

    mask = 0b1111100000000000
    upper = num & mask
    if len(str(bin(upper))) == 7:
        # perform two's compliment operator, then take the negative
        upper = upper ^ mask
        upper += 1
        n = 0 - upper
    elif len(str(bin(upper))) > 7:
        print "error: greater than 5 bits for upper"
    else:
        n = upper
        
    return (y * 2**n)

def disp_all_number_formats(arg):
    # takes a in a hexadecimal string, method prints all variants of the number
    integer = int(arg, 16)
    binary = bin(integer)
    lin11 = lin11_to_dec(arg)
    lin16 = lin16_to_dec(arg)
    print "    hexadecimal |   integer   |  linear11  |  linear16  |  binary"
    print "       %-12s %-12d %-12d %-12d %s" % (arg, integer, lin11, lin16, binary)

######################################################################
class device(object):
    ####################### Necessaries ####################
    def __init__(self, parent_bus, address, name, partnum):
        self.parent_bus = parent_bus
        self.address = address
        self.name = name
        self.partnum = partnum
        self.isPresent = False

    def __str__(self):
        if self.isPresent:
            return "    0x" + self.address + ":(+) " + self.name 
        else:
            return "    0x" + self.address + ":(-) " + self.name
    def __repr__(self):
        if self.isPresent:
            return "    0x" + self.address + ":(+) " + self.name 
        else:
            return "    0x" + self.address + ":(-) " + self.name 

    ###################### Getters/Setters ######################
    def setIsPresent(self, isPresent):
        self.isPresent = isPresent

    def getIsPresent(self):
        return self.isPresent

    def getAddr(self):
        return self.address

    ###################### Useful Methods #######################
    def printProperties(self, smw):
        pass #folder = smw.callCmd("ls " + )


######################################################################
class bus(object):
    ######################## Necessaries #####################
    def __init__(self, bus_number, bus_name, path):
        # Note everything is always in strings, not ints
        self.bus_number = bus_number
        self.bus_name = bus_name
        self.path = path
        self.devices = []
    
    def __str__(self):
        return self.bus_number + ": " + self.bus_name
    def __repr__(self):
        return self.bus_number + ": " + self.bus_name

    ###################### Device Printers ##########################
    def printDevices(self):
        print self.bus_number + ": " + self.bus_name
        for dev in self.devices:
            print `dev`
    def printPresentDevices(self):
        print self.bus_number + ": " + self.bus_name
        for dev in self.devices:
            if dev.getIsPresent():
                print `dev`
    def printMissingDevices(self):
        print self.bus_number + ": " + self.bus_name
        for dev in self.devices:
            if not dev.getIsPresent():
                print `dev`

    ####################### Useful Stuff ########################
    def setDevicePresences(self, addrs):
        for d in self.devices:
            if d.getAddr() in addrs:
                d.setIsPresent(True)
            else:
                d.setIsPresent(False)

    ###################### Getters/Setters ######################
    def addDevice(self, address, name, partnum):
        # only used as part of creating the class. Shouldn't be touched too much.
        self.devices.append(device(self.bus_number, address, name, partnum))
    
    def getDevice(self, addr):
        for dev in self.devices:
            if dev.getAddr() == str(addr):
                return dev
    
    def getMissingDevices(self, addrs):
        out = []
        found = False
        for a in addrs:
            for d in self.devices:
                if d.getAddr() == a:
                    found = True
                    break
            if not found:
                out.append(a)
        return out

    def getNum(self):
        return self.bus_number
    
    def getName(self):
        return self.bus_name
    
    def getPath(self):
        return self.path

    def getAddresses(self):
        out = []
        for d in self.devices:
            out.append(d.getAddr())
        return out


########################################################################
####################### Specific Device Classes ########################
class voltageRegulator(device):
    ##################### Lists and Dictionaries ########################
    #             cmd                        hex  #bytes willdisplay
    cmd = [ ["OPERATION",                   "01",   1,  False],
            ["ON_OFF_CONFIG",               "02",   1,  False],
            ["CLEAR_FAULTS",                "03",   1,  False],
            ["WRITE_PROTECT",               "10",   1,  False],
            ["STORE_USER_ALL",              "15",   1,  False],
            ["RESTORE_USER_ALL",            "16",   1,  False],
            ["CAPABILITY",                  "19",   1,  False],
            ["SMBALERT_MASK",               "1B",   1,  False],
            ["VOUT_COMMAND",                "21",   2,  False],
            ["VOUT_TRIM",                   "22",   2,  False],
            ["VOUT_MAX",                    "24",   2,  False],
            ["VOUT_MARGIN_HIGH",            "25",   2,  False],
            ["VOUT_MARGIN_LOW",             "26",   2,  False],
            ["VOUT_TRANSITION_RATE",        "27",   2,  False],
            ["VOUT_SCALE_LOOP",             "29",   2,  False],
            ["FREQUENCY_SWITCH",            "33",   2,  False],
            ["VIN_ON",                      "35",   2,  False],
            ["VIN_OFF",                     "36",   2,  False],
            ["IOUT_CAL_OFFSET",             "39",   2,  False],
            ["VOUT_OV_FAULT_LIMIT",         "40",   2,  False],
            ["VOUT_OV_FAULT_RESPONSE",      "41",   2,  False],
            ["VOUT_OV_WARN_LIMIT",          "42",   2,  False],
            ["VOUT_UV_WARN_LIMIT",          "43",   2,  False],
            ["VOUT_UV_FAULT_LIMIT",         "44",   2,  False],
            ["VOUT_UV_FAULT_RESPONSE",      "45",   1,  False],
            ["IOUT_OC_FAULT_LIMIT",         "46",   2,  False],
            ["IOUT_OC_FAULT_RESPONSE",      "47",   1,  False],
            ["IOUT_OC_WARN_LIMIT",          "4A",   2,  False],
            ["OT_FAULT_LIMIT",              "4F",   2,  False],
            ["OT_FAULT_RESPONSE",           "50",   1,  False],
            ["OT_WARN_LIMIT",               "51",   2,  False],
            ["VIN_OV_FAULT_LIMIT",          "55",   2,  False],
            ["VIN_OV_FAULT_RESPONSE",       "56",   1,  False],
            ["VIN_UV_WARN_LIMIT",           "58",   2,  False],
            ["POWER_GOOD_ON",               "5E",   2,  False],
            ["POWER_GOOD_OFF",              "5F",   2,  False],
            ["TON_DELAY",                   "60",   2,  False],
            ["TON_RISE",                    "61",   2,  False],
            ["TON_MAX_FAULT_LIMIT",         "62",   2,  False],
            ["TON_MAX_FAULT_RESPONSE",      "63",   1,  False],
            ["TOFF_DELAY",                  "64",   2,  False],
            ["TOFF_FALL",                   "65",   2,  False],
            ["STATUS BYTE",                 "78",   1,  True],
            ["STATUS WORD",                 "79",   2,  True],
            ["STATUS_VOUT",                 "7A",   1,  True],
            ["STATUS_IOUT",                 "7B",   1,  True],
            ["STATUS_INPUT",                "7C",   1,  True],
            ["STATUS_TEMPERATURE",          "7D",   1,  True],
            ["STATUS_CML",                  "7E",   1,  True],
            ["READ_VIN",                    "88",   2,  True],
            ["READ_VOUT",                   "8B",   2,  True],
            ["READ_IOUT",                   "8C",   2,  True],
            ["READ_TEMPERATURE",            "8D",   2,  True],
            ["READ_POUT",                   "96",   2,  True],
            ["PMBUS_REVISION",              "98",   1,  True],
            ["MFR_ID",                      "99",   4,  True],
            ["MFR_MODEL",                   "9A",   4,  True],
            ["MFR_REVISION",                "9B",   4,  True],
            ["IC_DEVICE_ID",                "AD",   4,  True],
            ["IC_DEVICE_REV",               "AE",   4,  True],
            ["MFR_READ_REG",                "D0",   8,  False],
            ["MFR_WRITE_REG",               "D1",   8,  False],
            ["MFR_I2C_ADDRESS",             "D6",   2,  True],
            ["MFR_TPGDLY",                  "D8",   2,  False],
            ["MFR_FCCM",                    "D9",   1,  False],
            ["MFR_VOUT_PEAK",               "DB",   2,  True],
            ["MFR_IOUT_PEAK",               "DC",   2,  True],
            ["MFR_TEMPERATURE_PEAK",        "DD",   2,  True],
        ]
    cmd_dict = {
        "STATUS BYTE":                 "78",
        "STATUS WORD":                 "79",
        "STATUS_VOUT":                 "7A",
        "STATUS_IOUT":                 "7B",
        "STATUS_INPUT":                "7C",
        "STATUS_TEMPERATURE":          "7D",
        "STATUS_CML":                  "7E",
        "READ_VIN":                    "88",
        "READ_VOUT":                   "8B",
        "READ_IOUT":                   "8C",
        "READ_TEMPERATURE":            "8D",
        "READ_POUT":                   "96",
        "PMBUS_REVISION":              "98",
        "MFR_ID":                      "99",
        "MFR_MODEL":                   "9A",
        "MFR_REVISION":                "9B",
        "IC_DEVICE_ID":                "AD",
        "IC_DEVICE_REV":               "AE",
        "MFR_I2C_ADDRESS":             "D6",
        "MFR_VOUT_PEAK":               "DB",
        "MFR_IOUT_PEAK":               "DC",
        "MFR_TEMPERATURE_PEAK":        "DD"
    }
    # Dictionary mapping input commands (from the command line) to the handler function
    valid_cmds = {
        "vout": get_vout,
        "status_vout": get_vout_status,
        "vin": get_vin,
        "iout": get_iout,
        "status_iout": get_iout_status,
        "get_status": get_status,   # one of the args will denote status byte vs word
        "status": get_status,
        "temp": get_temp,
        "temperature": get_temp,
        "temp_status": get_temp_status,
        "temperature_status": get_temp_status,
        "cml_status": get_cml_status,       # what the hell is this?
        "power": get_power,
        "power_out": get_power,
        "id": get_id,       # might lump MFR_MODEL/REVISION in with this
        "dev": get_id,
        # IC_DEVICE_ID?
        "watch": watch_regs,    # arguments for "watch vin/vout/iout/pout", or just spits all them out
        "raw": raw_cmd     # function that sends a hex value to the bus
        "raw_cmd": raw_cmd
    }
    
    ###################### Necessaries ########################
    def __init__(self, parent_bus, address, name, partnum):
        super(voltageRegulator, self).__init__(parent_bus, address, name, partnum)
    def __str__(self):
        pass        # this sucker is gonna be hefty
    def __repr__(self):
        pass        # copy __str__
    
    ##################### Useful Functions #####################
    def printAllCommands(self, print_size=False):
        for row in self.cmd:            
            if print_size:
                if row[2] == 1:
                    num_bytes = "byte"
                elif row[2] == 2:
                    num_bytes = "word"
                elif row[2] == 4:
                    num_bytes = "block"
                else:
                    num_bytes = "custom"
                outstr = "0x%s:(%s) %s" % (row[1], num_bytes, row[0])
            else:
                outstr = "0x%s: %s" % (row[1], row[0])
            print outstr
    
    def printCommands(self, print_size=False):
        for row in self.cmd:
            if row[3]:
                if print_size:
                    if row[2] == 1:
                        num_bytes = "byte"
                    elif row[2] == 2:
                        num_bytes = "word"
                    elif row[2] == 4:
                        num_bytes = "block"
                    else:
                        num_bytes = "custom"
                    outstr = "0x%s:(%s) %s" % (row[1], num_bytes, row[0])
                else:
                    outstr = "0x%s: %s" % (row[1], row[0])
                print outstr

    ##################### Cmd Handlers ############################
    def handleCommand(self, args):
        try:
            valid_cmds[args[0]](args[1:])
            return
        except:
            print args[0] + ": invalid command"
        try:
            if not raw_cmd(args[1:]):
                print args[0] + ": invalid command"
        except:
            print args[0] + ": invalid command"


     ######## args[0] will ALWAYS be the smw from here onward #########
    def get_vout(self, args):
        if self.address[0] == "1":
            # TODO: is there an actual formula for this...? This is really hacky
            self.address[0] == "4"
        smw = args[0]
        out = smw.callCmd("i2cget -y %s 0x%s 0x%s w" % (self.parent_bus, self.address, "8B"))
        out_num = lin11_to_dec(out)
        print "%d V" % (out_num)
    def get_vout_status(self, args):
        if self.address[0] == "1":
            # TODO: is there an actual formula for this...? This is really hacky
            self.address[0] == "4"
        smw = args[0]
        out = smw.callCmd("i2cget -y %s 0x%s 0x%s" % (self.parent_bus, self.address, "7A"))
        print out
    def get_vin(self, args):
        if self.address[0] == "1":
            # TODO: is there an actual formula for this...? This is really hacky
            self.address[0] == "4"
        smw = args[0]
        out = smw.callCmd("i2cget -y %s 0x%s 0x%s w" % (self.parent_bus, self.address, "88"))
        out_num = lin11_to_dec(out)
        print "%d V" % (out_num)
    def get_iout(self, args):
        if self.address[0] == "1":
            # TODO: is there an actual formula for this...? This is really hacky
            self.address[0] == "4"
        smw = args[0]
        out = smw.callCmd("i2cget -y %s 0x%s 0x%s w" % (self.parent_bus, self.address, "8C"))
        out_num = lin11_to_dec(out)
        print "%d A" % (out_num)
    def get_iout_status(self, args):
        if self.address[0] == "1":
            # TODO: is there an actual formula for this...? This is really hacky
            self.address[0] == "4"
        smw = args[0]
        out = smw.callCmd("i2cget -y %s 0x%s 0x%s" % (self.parent_bus, self.address, "7B"))
        print out
    def get_status(self, args):
        if self.address[0] == "1":
            # TODO: is there an actual formula for this...? This is really hacky
            self.address[0] == "4"
        smw = args[0]
        out = smw.callCmd("i2cget -y %s 0x%s 0x%s w" % (self.parent_bus, self.address, "79"))
        print out
    def get_temp(self, args):
        if self.address[0] == "1":
            # TODO: is there an actual formula for this...? This is really hacky
            self.address[0] == "4"
        smw = args[0]
        out = smw.callCmd("i2cget -y %s 0x%s 0x%s w" % (self.parent_bus, self.address, "8C"))
        out_num = lin11_to_dec(out)
        print "%d C" % (out_num)
    def get_temp_status(self, args):
        if self.address[0] == "1":
            # TODO: is there an actual formula for this...? This is really hacky
            self.address[0] == "4"
        smw = args[0]
        out = smw.callCmd("i2cget -y %s 0x%s 0x%s" % (self.parent_bus, self.address, "7D"))
        print out
    def get_cml_status(self, args):
        if self.address[0] == "1":
            # TODO: is there an actual formula for this...? This is really hacky
            self.address[0] == "4"
        smw = args[0]
        out = smw.callCmd("i2cget -y %s 0x%s 0x%s" % (self.parent_bus, self.address, "7E"))
        print out
    def get_power(self, args):
        if self.address[0] == "1":
            # TODO: is there an actual formula for this...? This is really hacky
            self.address[0] == "4"
        smw = args[0]
        out = smw.callCmd("i2cget -y %s 0x%s 0x%s w" % (self.parent_bus, self.address, "96"))
        out_num = lin11_to_dec(out)
        print "%d W" % (out_num)
    def get_id(self, args):
        if self.address[0] == "1":
            # TODO: is there an actual formula for this...? This is really hacky
            self.address[0] == "4"
        smw = args[0]
        # TODO: how do we get a block?
        out = smw.callCmd("i2cget -y %s 0x%s 0x%s k" % (self.parent_bus, self.address, "AD"))
        print out
    def watch_regs(self, args):
        if self.address[0] == "1":
            # TODO: is there an actual formula for this...? This is really hacky
            self.address[0] == "4"
        smw = args[0]
        # TODO: How can we update the same thing in the command line?
    def raw_cmd(self, args):
        if self.address[0] == "1":
            # TODO: is there an actual formula for this...? This is really hacky
            self.address[0] == "4"
        smw = args[0]
        command = args[1]
        for row in self.cmd:
            if command.upper() == row[0]:
                # need to issue the command and see what comes of it
                out = smw.callCmd("i2cget -y %s 0x%s 0x%s k" % (self.parent_bus, self.address, row[1]))
                print out
                return True
            elif command.upper() == row[1]:
                out = smw.callCmd("i2cget -y %s 0x%s 0x%s k" % (self.parent_bus, self.address, row[1]))
                print out
                return True
        return False
        



