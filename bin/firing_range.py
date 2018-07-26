f = open('i2ctemp.txt', 'r')
text_holder = f.read()

index = text_holder.find("\n")

while index != -1:
    
# for line in var:
#     try:
#         print int(line[4:7])
#     except:
#         print int(line[4:6])

f.close()