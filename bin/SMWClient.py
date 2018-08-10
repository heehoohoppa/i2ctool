import subprocess

class SMWClient(object):
    ''' Class to handle interacting with the BC. Creating a SMWClient object just
        stores the cname we're interacting with, then the methods use the stored
        cname to actually do I/O with the BC
    '''
    def __init__(self, cname):
        self.cname = cname

    def callCmd(self, cmd):
        ''' Send a silent command to the remote host (cname), dump the output to a text file
            on the BC, bring the text file back to the SMW, and print the textfile's output
        '''
        cmd = "rsh -l root " + str(self.cname) + " " + cmd
        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
        out = p.stdout.read()
        return out


    def checkCname(self):
        output = self.callCmd("ls ../..")
        if len(output) <= 0:
            print "Cannot connect to " + self.cname
            return 0
        return 1






