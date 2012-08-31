"""
Copyright (c) 2012 GONICUS GmbH
License: LGPL
Author: Konrad Kleine <kleine@gonicus.de>
"""
import threading


class Dispatcher(threading.Thread):
    """
    Listens to a Gerrit stream of events and dispatches events to handlers.
    All handler should implement at least a subset of the gerritevent.Handler
    methods. If "endless" is True the dispatcher continuously re-connects to
    the Gerrit server and parses requests when an error occured.
    This class was inspired by http://code.google.com/p/gerritbot/
    """
    def __init__(self, config, handlers, endless=False):
        """
        Constructs a dispatcher.
        """
        threading.Thread.__init__(self)
        self.__host = config.get("gerrit", "host")
        self.__port = config.getint("gerrit", "port")
        self.__user = config.get("gerrit", "user")
        self.__ssh_private_key = config.get("gerrit", "ssh_private_key")
        self.__passphrase = config.get("gerrit", "passphrase")
        self.__handlers = handlers
        self.__endless = endless

    def run(self):
        """
        The main entry point when calling start() on the dispatcher object.
        If "self.__endless" is True this method continuously re-connects to
        the Gerrit server and parses requests when an error occurred.
        Configure the "endless" parameter with the constructor.
        """
        import time
        while True:
            try:
                client = self._connect_to_gerrit()
                self._read_stream(client)
                self._disconnect_from_gerrit(client)
            except Exception, ex:
                print((str(self)) + " Unexpected: " + str(ex))
            # End the loop if not in endless mode
            if not self.__endless:
                break
            print((str(self)) + " sleeping and wrapping around")
            time.sleep(5)

    def _connect_to_gerrit(self):
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
        client.get_transport().set_keepalive(60)
        return client

    def _dispatch_event(self, event):
        """
        Informs all registered handlers by invoking the correct event callback.
        The handler in turn can do stuff like writing into a ticket system,
        IRC, Jabber, Twitter, etc. You name it!
        """
        for handler in self.__handlers:
            _mapping = {
                      'patchset-created': handler.patchset_created,
                      'change-abandoned': handler.change_abandoned,
                      'change-restored': handler.change_restored,
                      'change-merged': handler.change_merged,
                      'comment-added': handler.comment_added,
                      'ref-updated': handler.ref_updated
            }[event["type"]](event)

    def _read_stream(self, client):
        """
        Read lines from event stream and dispatch them as events to handlers.
        """
        import json
        _stdin, stdout, _stderr = client.exec_command("gerrit stream-events")
        for line in stdout:
            print(line)
            try:
                event = json.loads(line)
                self._dispatch_event(event)
            except ValueError:
                pass

    def _disconnect_from_gerrit(self, client):
        """
        Closes the SSH connection to the Gerrit server.
        """
        print((str(self)) + " Disconnecting from " + str(self.__host))
        client.close()
