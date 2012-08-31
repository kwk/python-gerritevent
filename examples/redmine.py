"""
Copyright (c) 2012 GONICUS GmbH
License: LGPL
Author: Konrad Kleine <kleine@gonicus.de>
"""
import gerritevent
import sys
if sys.version_info < (3, 0):
    from ConfigParser import ConfigParser
else:
    from configparser import ConfigParser


def main():
    """
    Reads a config an starts dispatching gerrit events.
    TODO (kwk): Add signal interrupt handling
    """
    config = ConfigParser()
    config.read("config.conf")
    handler = gerritevent.RedmineHandler(config)
    dispatcher = gerritevent.Dispatcher(config, handlers=[handler])
    dispatcher.start()

if __name__ == "__main__":
    main()
