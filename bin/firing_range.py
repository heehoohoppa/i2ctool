import csvlib as csvlib

bus_list = csvlib.csv_to_bus_list("Device List.csv")

for item in bus_list:
    print item

