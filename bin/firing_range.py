import csvlib as csvlib
import helperFunctions as helper 
import SMWClient as SMWClient
from copy import deepcopy

bus_list = csvlib.csv_to_bus_list("Device List.csv")

index = csvlib.find_index(14, bus_list)
bus = deepcopy(bus_list[index])
addresses = ['19', '20', '30', '4B', '4C', '70']

something = False

bus.addDevice('99', 'Test Thing', '100100100')
bus.printDevices()
bus_list[index].printDevices()

