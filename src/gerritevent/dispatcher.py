"""
Copyright (c) 2012 GONICUS GmbH

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Listens to a gerrit stream of events and dispatches events to handlers.
"""
import threading

class Dispatcher(threading.Thread):
    """
    Listens to a gerrit stream of events and dispatches events to handlers.
    All handler should implement at least a subset of the gerritevent.Handler
    methods.
    This class was inspired by http://code.google.com/p/gerritbot/
    """
    def __init__(self, config, handlers):
        """
        Constructs a dispatcher
        """
        threading.Thread.__init__(self)
        self.__host = config.get("gerrit", "host")
        self.__port = config.getint("gerrit", "port")
        self.__user = config.get("gerrit", "user")
        self.__ssh_private_key = config.get("gerrit", "ssh_private_key")
        self.__passphrase = config.get("gerrit", "passphrase")
        self.__handlers = handlers

    def run(self):
        """
        The main entry point when calling start() on the dispatcher object.
        This method calls the dispatch() method over and over again, to
        avoid the dispatcher to stop when an error occured.
        """
        import time
        while True:
            try:
                client = self.connect_to_gerrit()
                self.read_stream(client)
                self.disconnect_from_gerrit(client)
            except Exception, e:
                print((str(self)) + " Unexpected: " + str(e))
            print((str(self)) + " sleeping and wrapping around")
            time.sleep(5)

    def connect_to_gerrit(self):
        """
        SSH connects to the Gerrit server, using the credentials from the ctor.
        """
        import paramiko
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print((str(self)) + " Connecting to " + self.__host)
        client.connect(self.__host,
                       self.__port,
                       self.__user,
                       key_filename=self.__ssh_private_key,
                       password=self.__passphrase,
                       timeout=60)
        return client

    def dispatch_event(self, event):
        """
        Informs all registered handlers by invoking the correct event callback.
        The handler in turn can do stuff like writing into a ticket system,
        IRC, Jabber, Twitter, etc. You name it!
        """
        for handler in self.__handlers:
            mapping = {
                      'patchset-created': handler.patchset_created,
                      'change-abandoned': handler.change_abandoned,
                      'change-restored': handler.change_restored,
                      'change-merged': handler.change_merged,
                      'comment-added': handler.comment_added,
                      'ref-updated': handler.ref_updated
            }[event["type"]](event)
        

    def read_stream(self, client):
        """
        Read lines from event stream and dispatch them as events to handlers.
        """
        import json
        client.get_transport().set_keepalive(60)
        stdin, stdout, stderr = client.exec_command("gerrit stream-events")
        for line in stdout:
            print(line)
            try:
                event = json.loads(line)
                self.dispatch_event(event)
            except ValueError:
                pass

    def disconnect_from_gerrit(self, client):
        """
        Closes the SSH connection to the Gerrit server.
        """
        print((str(self))+" Disconnecting from "+str(self.__host))
        client.close()
