# -*- coding: UTF-8 -*-

# --------------------------------------------------------------------
#
# Copyright 2014-2018 Cray Inc. All Rights Reserved.
#
# These coded instructions, statements, and computer programs contain
# unpublished proprietary information of Cray Inc., and are protected
# by Federal copyright law.  They may not be disclosed to third
# parties or copied or duplicated in any form, in whole or in part,
# without the prior written consent of Cray Inc.
#
# --------------------------------------------------------------------

"""
Low-level driver for Out Of Band (OOB) JTAG Debug via VLOC FPGA
core memory-mapped I/O interface, client and server code.
Transports primitives between client and server (or itself).
(Originated from eITP itpclient.py and vloctest.py)
"""

import os
import subprocess
import errno
import socket
import time
import traceback


from CrayHssLib.oob.oobtransport import OOBTransport as _OOBTransport


class OOBClient(_OOBTransport):
    """Client-specific code for transport of OOB python
    functions and data.
    """
    def __init__(self, remoteHost=None, retries=2):
        super(OOBClient, self).__init__()
        self._tracePrefix = "OOBClient--: "
        # How many failures opening VLOC to put up with...
        self._retries = retries

        # If a remote hostname/ipaddr has NOT been designated, we
        # are operating "locally" on the BC.
        self._remoteHost = remoteHost
        if 'OOBREMOTE' in os.environ and len(os.environ['OOBREMOTE']) != 0:
            self._remoteHost = os.environ['OOBREMOTE']

        # Driver is assmued closed
        self._isOpen = False

        # Utility functions
        self.funcBuild("killServer")
        self.funcBuild("hello")
        self._serverProc = None

    def callCmd(self, cmd, grabOutput=False):
        """Issue a silent command to remote host, checking numerical result.
        """
        self.trace("command: {0:s}".format(' '.join(cmd)))
        try:
            if grabOutput:
                output = subprocess.check_output(
                            cmd,
                            stderr=subprocess.STDOUT)
            else:
                subprocess.check_call(
                            cmd,
                            stderr=subprocess.STDOUT)
                output = None
        except subprocess.CalledProcessError as cpe:
            raise EnvironmentError(
                cpe.returncode,
                "Command FAILED: \"{0:s}\"".format(' '.join(cmd)))
        return output

    def getServerModNames(self):
        """Virtual method for server to get a list of give its modules
        so they can be copied up to remote host.  The first module in
        the list is the main module (to import).
        Should return:
          os.path.abspath(__file__).  That can't be done here.
        """
        raise EnvironmentError(
                errno.EFAULT,
                "getServerModNames() needs to be defined in a child class")

    def runServer(self):
        """Copy up python, this file, and any necessary python libraries
        to the remote host. Then run the server
        """
        # Local operation. Do nothing.
        if self._remoteHost is None:
            return

        # Is Server already running?
        try:
            answer = self._client("hello")
            if not answer in ["Howdy!", "Hello!"]:
                raise EnvironmentError(
                        errno.EINVAL,
                        "ERROR: Incorrect answer from OOB Server.")
            self.trace("OOB Server already running")
            # Set to something besides None or a Popen() object
            self._serverProc = answer
            return
        except:
            #self.trace(traceback.format_exc())
            self.trace("OOB Server not running. Starting...")

        # Determine architecture of server
        remoteArch = self.callCmd(
            ["rsh", "-l", "root", self._remoteHost, "uname -m"],
            grabOutput=True).rstrip()
        
        # Copy appropriate bcpython and libraries to BC
        self.callCmd(
            ["rcp", "-r", "/opt/cray/itp/{0:s}_bc/".format(remoteArch),
             "root@{0:s}:/".format(self._remoteHost)])

        # (Set up to) Copy up the transport and server module.
        serverModDir = os.path.dirname(os.path.abspath(__file__))
        serverModList = [
            os.path.join(serverModDir, "oobtransport.py"),
            os.path.join(serverModDir, "oobserver.py")]

        # (Set up to) Copy the server (child class of this) up
        serverModList.extend(self.getServerModNames())

        # Copy the server mods
        self.callCmd(
            ["rcp"] +
            serverModList +
            ["root@{0:s}:/var/lib/python2.7".format(self._remoteHost)])

        # Run the server
        try:
            self._devnull = open(os.devnull, 'r')
            self._serverProc = subprocess.Popen(
                ["rsh", "-l", "root", self._remoteHost,
                 "{0:s}/var/tmp/bcpython {1:s}".format(
                    "OOBTRACE=1 " if self._traceOn == True else "",
                    os.path.join("/var/lib/python2.7",
                                 os.path.basename(
                                    self.getServerModNames()[0])))],
                stdin=self._devnull,
                close_fds=True)
        except OSError as oe:
            raise EnvironmentError(
                    errno.EHOSTDOWN,
                    "Failure running remote server/bcpython")
        time.sleep(1.0)

    def cleanupServer(self):
        """(Stop and) Remove anything copied up to the remote
        host by runServer() method.
        """
        if self._serverProc is not None:
            self._client("killServer")
            if isinstance(self._serverProc, subprocess.Popen):
                self._serverProc.communicate()
                self._devnull.close()
            self.callCmd(
                ["rsh", "-l", "root", self._remoteHost,
                 "rm -rf /var/tmp/bcpython /var/lib/python2.7"])
            self._serverProc = None

    def _killClient(self):
        """Terminates a client connection
        """
        if None in [self._remoteHost, self._sock]:
            return
        self._sock.close()
        self._sock = None

    def _client(self, funcName, parmList=[]):
        """Inner function to convert a function to a list, then pickle it for
        transmisson to the server.
        Returns the result of the operation (not an error code).
        Errors are raised with EnvironmentError.
        """
        libFuncName = "self.{0:s}".format(funcName)
        if self._remoteHost is None:
            # Local non-client/server operation.  Call the primitive directly.
            if funcName == "killServer":
                # Local: no server to kill
                return None
            if funcName == "hello":
                # Local always answers
                return "Hello!"
            if funcName == "_gatherTrace":
                raise EnvironmentError(
                        errno.EINVAL,
                        "_gatherTrace() for remote use only!")
            return self._invokeOOBDirective([libFuncName] + parmList,
                                            raiseErrors=True)

        # Remote:
        # Start the client and send the OOB primitive to server
        if self._sock is not None:
            self._killClient()
        # Batch all errors into ENOTCONN to be flagged as a failure
        # to connect to the Server
        try:
            self._sock = socket.socket(socket.AF_INET,
                                       socket.SOCK_STREAM)
        except:
            self.trace(traceback.format_exc())
            raise EnvironmentError(
                    errno.ENOTCONN,
                    "Failure opening OOB server socket!")
        if self._sock is None:
            raise EnvironmentError(
                    errno.ENOTCONN,
                    "Remote OOB server socket cannot be opened!")
        connectRetries = self._retries
        while True:
            try:
                self._sock.connect((self._remoteHost,
                                    self.OOB_TCPPORT))
                break
            except:
                time.sleep(1)
                connectRetries -= 1
                if connectRetries == 0:
                    if self._traceOn:
                        traceback.print_exc()
                    raise EnvironmentError(
                        errno.ENOTCONN,
                        "Timed out attempting to connect to OOB server!")

        self._sendObj(self._sock, [libFuncName] + parmList)
        self._delayTrace = True
        recvObj = self._recvObj(self._sock)
        self._delayTrace = False
        self._killClient()
        if funcName == "killServer":
            # killServer command sends back the trace buffer as it's
            # return object.
            self.trace(recvObj)
            return None
        if funcName != "_gatherTrace":
            # Recurse, gather, and report the trace info from server
            if self._traceOn == True:
                self._traceOn = False
                serverTraceStr = self._client("_gatherTrace")
                self._traceOn = True
                if isinstance(serverTraceStr, EnvironmentError):
                    # Errors from the server-side oob get raised
                    raise serverTraceStr
                self.trace(serverTraceStr, "--OOBServer: ")
                self.flushTrace()
        if isinstance(recvObj, EnvironmentError):
            # Errors from the server-side oob get raised
            raise recvObj
        return recvObj

    def funcBuild(self, funcName, parms=[]):
        """Build an entry point, either local or for server, using a
        closure/nested function, giving some typechecking and robustness.
        The nested function raises EnvironmentError exceptions when things go
        bad.
        """
        def fn(self, *args):
            # Check for parameter integrity can be done here

            # Issue the client command
            if len(args) != 0:
                return self._client(funcName, list(args))
            return self._client(funcName)

        # (Not part of fn... back into funcBuild)
        # Check for function name integrity and
        # set the attribute in this instance (self).
        if not isinstance(funcName, basestring):
            raise EnvironmentError(
                    errno.EINVAL,
                    "funcName should be a string type.")
        setattr(self.__class__, funcName, fn)

    def getattrBuild(self, attrName):
        """Build a getattr transportable method, either local or for server,
        using a closure/nested function, giving some typechecking and robustness.
        The nested function raises EnvironmentError exceptions when things go
        bad.
        """
        def fn(self):
            # Issue the client command
            return self._client("__getattr__", [attrName])

        # (Not part of fn... back into getattrBuild)
        # Check for attribute name integrity and
        # set the attribute in this instance (self).
        if not isinstance(attrName, basestring):
            raise EnvironmentError(
                    errno.EINVAL,
                    "attrName should be a string type.")
        setattr(self.__class__, attrName, property(fget=fn))

    def setattrBuild(self, attrName):
        """Build a setattr transportable method, either local or for server,
        using a closure/nested function, giving some typechecking and robustness.
        The nested function raises EnvironmentError exceptions when things go
        bad.
        """
        def fn(self, value):
            # Issue the client command
            return self._client("__setattr__", [attrName, value])

        # (Not part of fn... back into setattrBuild)
        # Check for attribute name integrity and
        # set the attribute in this instance (self).
        if not isinstance(attrName, basestring):
            raise EnvironmentError(
                    errno.EINVAL,
                    "attrName should be string type.")
        setattr(self.__class__, attrName, property(fset=fn))
