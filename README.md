This [library] [1] connects the code review tool [Gerrit] [2] in a loose
fashion to any number of issue trackers or messaging services. It does
this by parsing the live output of Gerrit events and dispatching them into
handlers.

For instance, the ```examples/redmine.py``` file illustrates how to connect
Gerrit to a [Redmine] [3] project management website. You just need to load a
```config.conf``` file, instanciate a ```gerritevent.RedmineHandler``` and
pass it to the ```gerritevent.Dispatcher``` instances before you start
the dispatcher.

You can of have multiple handlers that all receive Gerrit events. Simply pass
the handlers as a list to the ```handlers``` parameter of the Dispatcher's
constructor. This way you can for instance update your issure tracker and
post a comment in your IRC room.

If you're looking for a handler that hasn't been implemented yet, you might
want to add a class to the ```gerritevent.handler``` [module] [4] that
implements everything you need. Please author a pull request if you want
your class to be included in the official *python-gerritevent* module.

In compact, extending gerritevent is as easy as this:

    """
    This handler connects Gerrit to my ticket system.
    """
    from gerritevent import Handler
    
    
    class MyHandler(gerritevent.Handler):
        """
        Overwrite callbacks from parent class. 
        """
        def __init__(self, config):
            """
            Parse your config options in the "myhandler" section.
            """
            self.__my_option = config.get("myhandler", "my_option")
    
        def comment_added(self, event):
            """
            Analyse the event object and translate the content to your target
            system. You can for instance do a REST-API call or something,
            depending you favor and what your system supports. 
            """
            pass


[1]: https://github.com/kwk/python-gerritevent "pyhthon-gerritevent"
[2]: http://code.google.com/p/gerrit/ "Gerrit"
[3]: http://www.redmine.org/ "Redmine"
[4]: https://github.com/kwk/python-gerritevent/blob/master/src/gerritevent/handler.py "Handler module"
