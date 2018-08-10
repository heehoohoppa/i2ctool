import subprocess

class SMWClient(object):
    ''' Class to handle interacting with the BC. Creating a SMWClient object just
        stores the cname we're interacting with, then the methods use the stored
        cname to actually do I/O with the BC
    '''
    def __init__(self, cname):
        # TODO: find the directory of all the devices upon initialization. Maybe have
        #       it be part of the checkCname.
        self.cname = cname

    def callCmd(self, cmd):
        ''' Send a silent command to the remote host (cname), dump the output to a text file
            on the BC, bring the text file back to the SMW, and print the textfile's output
        '''
        cmd = "rsh -l root " + str(self.cname) + " " + cmd
        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
        out = p.stdout.read()
        
        # rsh -l root c0-0c0s2 cat /sys/bus/i2c/devices/131-0044/0x88-89/read_vin
        # call(["rcp", "-r", 
        #     "root@" + self.cname + ":/tmp/i2ctemp.txt",
        #     "."])
        #     # we now have the output in a local textfile
        # f = open("./i2ctemp.txt", "r")
        # out = f.read()
        # f.close()
        return out


    def checkCname(self):
        # try:
        #     self.callCmd("ls")
        #     return 1
        # except:
        #     return 0
        output = self.callCmd("ls ../..")
        if len(output) <= 0:
            print "Cannot connect to " + self.cname
            return 0
        return 1






