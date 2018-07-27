from csv import reader

class device(object):

    def __init__(self, address, name, partnum):
        self.address = address
        self.name = name
        self.partnum = partnum
        self.isPresent = False

    def __str__(self):
        out = "    0x" + self.address + ": " + self.name
        # if isPresent:
        #     out = out + "  not present"
        # else:
        #     out = out + "  present"

    def __repr__(self):
        return "    0x" + self.address + ": " + self.name 

    def setIsPresent(self, isPresent):
        self.isPresent = isPresent

    def getIsPresent(self):
        if(self.isPresent):
            print "device is active"
        else:
            print "device not found"

    def getAddr(self):
        return self.address



class bus(object):
    '''
        Class to handle a single bus
    '''
    def __init__(self, bus_number, bus_name, path):
        # So, could we have that csvmatrix or whatever be a global thing?
        #  We kinda need everyone to be able to access it
        self.bus_number = bus_number
        self.bus_name = bus_name
        self.path = path
        self.devices = []
    
    def __str__(self):
        return self.bus_number + ": " + self.bus_name + "\n\r"

    def printAll(self):
        print self.bus_number + ": " + self.bus_name + "\n\r"
        for dev in self.devices:
            print `dev` + "\n\r"

    def addDevice(self, address, name, partnum):
        # only used as part of creating the class. Shouldn't be touched too much.
        self.devices.append(device(address, name, partnum))
    
    def getDevice(self, addr):
        for dev in self.devices:
            if dev.getAddr() == str(addr):
                return dev


    def setDevicePresences(self, addrs):
        for d in self.devices:
            if d.getAddr() in addrs:
                d.setIsPresent(True)
            else:
                d.setIsPresent(False)
    
    def printDevices(self, onlyPresent=False):
        if onlyPresent:
            for dev in self.devices:
                if dev.getIsPresent():
                    print `dev` + "\n\r"
        else:
            for dev in self.devices:
                print `dev` + "\n\r"

    def getNum(self):
        return self.bus_number
    
    def getName(self):
        return self.bus_name

    



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
    L = 0
    R = len(bus_list) - 1
    while L < R:
        tracker = int((L+R)/2)
        if bus_list[tracker].getNum() > bus_num:
            L = tracker + 1
        elif bus_list[tracker].getNum() < bus_num:
            R = tracker - 1
        else:
            return tracker
    return -1

def check_bus(smw):
    pass


def check_device(smw):
    pass



