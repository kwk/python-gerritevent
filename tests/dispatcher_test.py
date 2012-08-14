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

This file tests the gerritevent.Dispatcher class.
"""
import gerritevent
import mock
import json
import sys
import unittest
import StringIO
if sys.version_info < (3, 0):
    from ConfigParser import ConfigParser
else:
    from configparser import ConfigParser


class DispatcherTest(unittest.TestCase):
    """
    This class tests the gerritevent.Dispatcher class.
    """
    def setUp(self):
        """
        Prepare the dispatcher object
        """
        print("--- Setting up Test ---")
        # Setup config file, so dispatcher can be instanciated
        config_contents = StringIO.StringIO("""[gerrit]
host: gerritserver
port: 29418
user: alice
ssh_private_key: /foo/bar
passphrase: tester
         """)
        self.config = ConfigParser()
        self.config.readfp(config_contents)
        # Create a bunch of handlers
        self.handler1 = mock.MagicMock(name="handler1")
        self.handler2 = mock.MagicMock(name="handler2")
        # Create a production dispatcher
        self.dispatcher = gerritevent.Dispatcher(
            config=self.config,
            handlers=[self.handler1, self.handler2],
            endless=False
        )
        # Assume, the connection to gerrit works
        self.dispatcher._connect_to_gerrit = mock.MagicMock(
            name="_connect_to_gerrit"
        )
        # Let the _connect_to_gerrit method return an object that mimics
        # the gerrit event stream with "light" events.
        self.client = mock.MagicMock()
        self.client.exec_command = mock.MagicMock(name="exec_command")
        self.client.exec_command.return_value = [
            # stdin
            None,
            # stdout (If we'd specify a string, the dispatcher would iterate
            #         over each character.)
            [
                json.dumps({"type":"patchset-created"}),
                json.dumps({"type":"change-abandoned"}),
                json.dumps({"type":"change-restored"}),
                json.dumps({"type":"change-merged"}),
                json.dumps({"type":"comment-added"}),
                json.dumps({"type":"ref-updated"})
            ],
            # stderr
            None
        ]
        self.dispatcher._connect_to_gerrit.return_value = self.client
        self.dispatcher._disconnect_from_gerrit = mock.MagicMock(
            name="_disconnect_from_gerrit"
        )
        # Mock the _dispatch_event method
        self.dispatcher._dispatch_event = mock.MagicMock(
            name="_dispatch_event"
        )
        # Now that we've configured the mocks, let's start the dispatcher
        self.dispatcher.start()
        self.dispatcher.join(10)
        print("--- Done Setting Up Test ---")

    def test__connect_to_gerrit(self):
        """
        Check that the connect method was called once.
        """
        self.dispatcher._connect_to_gerrit.assert_called_once()

    def test__dispatch_event(self):
        """
        Given a number of events test that _dispatch_event is called as
        expected.
        """
        calls = [
            (({u'type': u'patchset-created'},), {}),
            (({u'type': u'change-abandoned'},), {}),
            (({u'type': u'change-restored'},), {}),
            (({u'type': u'change-merged'},), {}),
            (({u'type': u'comment-added'},), {}),
            (({u'type': u'ref-updated'},), {})
        ]
        # print("Exp.: " + str(calls))
        # print("Real: " + str(self.dispatcher._dispatch_event.call_args_list))
        self.assertEquals(
            calls,
            self.dispatcher._dispatch_event.call_args_list,
            "_dispatch_event() calls not as expected"
        )

    def test_handler1_called(self):
        """
        Test that the appropriate methods of handler 1 were called.
        """
        self.handler1.patchset_created.assert_called_once()
        self.handler1.changed_abanoned.assert_called_once()
        self.handler1.changed_restored.assert_called_once()
        self.handler1.change_merged.assert_called_once()
        self.handler1.comment_added.assert_called_once()
        self.handler1.ref_updated.assert_called_once()

    def test_handler2_called(self):
        """
        Test that the appropriate methods of handler 2 were called.
        """
        self.handler2.patchset_created.assert_called_once()
        self.handler2.changed_abanoned.assert_called_once()
        self.handler2.changed_restored.assert_called_once()
        self.handler2.change_merged.assert_called_once()
        self.handler2.comment_added.assert_called_once()
        self.handler2.ref_updated.assert_called_once()

    def test__disconnect_from_gerrit(self):
        """
        Check that the disconnect method was called once.
        """
        self.dispatcher._disconnect_from_gerrit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
