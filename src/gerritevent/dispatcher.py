"""
Copyright (c) 2012 Konrad Kleine

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
import simplejson


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
        self.__config = config
        self.__host = self.__config.get("gerrit", "host")
        self.__port = self.__config.getint("gerrit", "port")
        self.__user = self.__config.get("gerrit", "user")
        self.__ssh_private_key = self.__config.get("gerrit", "ssh_private_key")
        self.__handlers = handlers

    def run(self):
        """
        The main entry point when calling start() on the dispatcher object.
        This method calls the dispatch() method over and over again, to
        avoid the dispatcher to stop when an error occured.
        """
        import time
        while True:
            self.dispatch()
            print((str(self)) + " sleeping and wrapping around")
            time.sleep(5)

    def dispatch(self):
        """
        Connects to gerrit event stream and dispatches events all handlers.
        The handler in turn can do stuff like writing into a ticket system,
        IRC, Jabber, Twitter, etc. You name it!
        """
        import paramiko
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            print((str(self)) + " connecting to " + self.__host)
            client.connect(self.__host,
                           self.__port,
                           self.__user,
                           # password='tester',  # TODO (kwk): replace test pw
                           key_filename=self.__ssh_private_key,
                           timeout=60)
            client.get_transport().set_keepalive(60)
            stdin, stdout, stderr = client.exec_command("gerrit stream-events")
            for line in stdout:
                print(line)
                try:
                    event = simplejson.loads(line)
                    for handler in self.__handlers:
                        mapping = {
                                  'patchset-created': handler.patchset_created,
                                  'change-abandoned': handler.change_abandoned,
                                  'change-restored': handler.change_restored,
                                  'change-merged': handler.change_merged,
                                  'comment-added': handler.comment_added,
                                  'ref-updated': handler.ref_updated
                        }[event["type"]](event)
                except ValueError:
                    pass
            client.close()
        except Exception, e:
            print((str(self)) + " unexpected " + str(e))
