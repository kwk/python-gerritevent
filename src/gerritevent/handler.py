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

A handler method gets called upon a dispatched gerrit event.
"""


class Handler(object):
    """
    Base class for classes that want to handle gerrit events.
    Please have a look at this URL, to see the attributes available for each
    event:
    http://gerrit.googlecode.com/svn/documentation/2.1.2/cmd-stream-events.html
    """
    def __init__(self, config):
        """
        Constructs a Handler object.
        """
        object.__init__(self)
        self.__comment_added_template = config.get("redmine",
                                                   "comment_added_template")

    def patchset_created(self, event):
        """
        Gets called when a patchset was created in gerrit.
        """
        pass

    def change_abandoned(self, event):
        """
        Gets called when a change was abandoned in gerrit.
        """
        pass

    def change_restored(self, event):
        """
        Gets called when a change was restored in gerrit.
        """
        pass

    def change_merged(self, event):
        """
        Gets called when a change was merged in gerrit.
        """
        pass

    def comment_added(self, event):
        """
        Gets called when a comment was added in gerrit.
        """
        pass

    def ref_updated(self, event):
        """
        Gets called when a reference was updated in gerrit.
        """
        pass

    def _prepare_comment_added_template(self, event):
        """
        Returns formatted "comment-added" template with substituted values.
        """
        from string import Template
        tpl = Template(self.__comment_added_template)
        return tpl.substitute(
            comment_author_name=event["author"]["name"],
            comment_author_email=event["author"]["email"],
            comment=event["comment"],
            change_url=event["change"]["url"],
            change_subject=event["change"]["subject"],
            approvals_verified_value=event["approvals"][0]["value"],  # FIX idx
            approvals_review_value=event["approvals"][1]["value"],  # FIX idx
            change_owner_name=event["change"]["owner"]["name"],
            change_owner_email=event["change"]["owner"]["email"],
            change_number=event["change"]["number"],
            change_project=event["change"]["project"],
            change_id=event["change"]["id"],
            change_branch=event["change"]["branch"],
            patchset_uploader_name=event["patchSet"]["uploader"]["name"],
            patchset_uploader_email=event["patchSet"]["uploader"]["email"],
            patchset_revision=event["patchSet"]["revision"],
            patchset_number=event["patchSet"]["number"],
            patchset_ref=event["patchSet"]["ref"],
            patchset_created_on=event["patchSet"]["createdOn"]
        )


class RedmineHandler(Handler):
    """
    Translates gerrit events into Redmine REST API calls.
    For instance the cover message of a gerrit review will automatically
    create a comment in the tickets named by either the cover message
    or the subject of the change to be reviewed.
    See: http://www.redmine.org/
    See: http://www.redmine.org/projects/redmine/wiki/Rest_api
    """
    def __init__(self, config):
        """
        Constructs a RedmineHandler object
        """
        Handler.__init__(self, config)
        self.__issue_url = config.get("redmine", "issue_url")
        self.__api_key = config.get("redmine", "api_key")

    def __get_issue_ids(self, string):
        """
        Returns as list of issue ID that occured in the string.
        An issue ID is characterized by a "#" follow by a number ranging
        from 1 to 99999999999999999999. Should be enough, eh?!
        """
        import re
        matches = re.findall(r"#(\d{1,20})", string, re.MULTILINE)
        return matches

    def __add_comment(self, issue_id, comment):
        """
        Adds the comment to the Redmine issue with ID issueID.
        """
        import httplib2
        http = httplib2.Http()        
        response, content = http.request(
             uri=self.__issue_url % int(issue_id),
             method='PUT',
             body=comment,
             headers={
                'X-Redmine-API-Key': self.__api_key,
                'Content-type': 'application/json'
             }
        )
        print(response)
        print(content)

    def comment_added(self, event):
        """
        Translates gerrit comment event into Redmine issue comment.
        """
        import json
        comment = str(event["comment"])
        author_name = str(event["author"]["name"])
        change_url = str(event["change"]["url"])
        change_subject = str(event["change"]["subject"])
        comment = json.dumps({
            "issue": {
              "notes":  self._prepare_comment_added_template(event)
            }
        })
        # get a unique list of issue IDs
        subject_issue_ids = self.__get_issue_ids(change_subject)
        comment_issue_ids = self.__get_issue_ids(comment)
        issue_ids = list(set(subject_issue_ids + comment_issue_ids))
        for issue_id in issue_ids:
            self.__add_comment(issue_id, comment)
