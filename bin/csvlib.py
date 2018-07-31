from csv import reader
from copy import deepcopy

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
########################################################################
########################### Other Functions ############################

def csv_to_bus_list(filename):
    bus_list = []
    current_bus = '-1'
    with open(filename, 'rb') as csvfile:       # 'rb'?
        iterable = reader(csvfile)
        iterable.next()
        for row in iterable:
            if(row[0] != current_bus):
                bus_list.append(bus(row[0], row[1], row[5]))
                bus_list[len(bus_list)-1].addDevice(row[2], row[3], row[4])
                current_bus = row[0]
            else:
                bus_list[len(bus_list)-1].addDevice(row[2], row[3], row[4])
    return bus_list


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

def check_bus(smw):
    pass

def check_device(smw):
    pass



