"""
Copyright (c) 2012 GONICUS GmbH
License: LGPL
Author: Konrad Kleine <kleine@gonicus.de>
"""
import json
from gerritevent.gerrit_objects import GerritApproval
from gerritevent.gerrit_objects import GerritChange
from gerritevent.gerrit_objects import GerritPatchSet
from gerritevent.gerrit_objects import GerritAccount
from gerritevent.gerrit_objects import GerritRefUpdate


class Error(Exception):
    """The basis for all error classes of this module."""
    pass


class DecodeError(Error):
    """Identifies an error when decoding any subclass of GerritEvent."""
    pass


class GerritEvent(object):
    """Represents a Gerrit event as emitted by the stream-events command.
    
    Each GerritEvent sublass consists of one ore more gerrit objects.
    """

    def __init__(self):
        """Creates a Gerrit Event object."""
        object.__init__(self)
    
    @classmethod
    def decode(cls, json_event):
        """Decodes and returns an event from ``json_event``.
        
        >>> event_string = '{"type":"patchset-created", ...}'
        >>> event = GerritEvent.decode(event_string)
        
        Args:
            dct: A dictionary from JSON
            
        Returns:
            Depending on the specific event type an object sublassed from
            GerritEvent is returned.
            
        Raises:
            gerrit_objects.DecodeError: If a GerritObject fails to decode.
            gerrit_events.DecodeError: If a GerritEvent fails to decode.
        """
        dct = json.loads(s=json_event)
        if dct['type'] == 'patchset-created':
            return GerritPatchSetCreatedEvent.decode(dct)
        elif dct['type'] == 'change-abandoned':
            return GerritChangeAbandonedEvent.decode(dct)
        elif dct['type'] == 'change-restored':
            return GerritChangeRestoredEvent.decode(dct)
        elif dct['type'] == 'change-merged':
            return GerritChangeMergedEvent.decode(dct)
        elif dct['type'] == 'comment-added':
            return GerritCommentAddedEvent.decode(dct)
        elif dct['type'] == 'ref-updated':
            return GerritRefUpdatedEvent.decode(dct)
        else:
            raise DecodeError('Failed to decode event.')


class GerritPatchSetCreatedEvent(GerritEvent):
    """Represents a patchset-created event in Gerrit."""
    
    def __init__(self, change, patch_set, uploader):
        """Creates a GerritPatchSetCreatedEvent object from given parameters.
        
        Args:
            change: The GerritChange object for which a patch-set was created
            patch_set: The GerritPatchSet object that was created
            uploader: The GerritAccount that uploaded the patch-set
        
        Returns:
            An instanciated GerritPatchSetCreatedEvent object
        
        Raises:
            ValueError: If any of the paramters have a wrong type
        """
        GerritEvent.__init__(self)
        self.change = change
        self.patch_set = patch_set
        self.uploader = uploader
    
    def __setattr__(self, name, value):
        """Sets the object's attribute ``name`` to ``value``.
        
        Args:
            name: A string representing the name of the attribute that's about
                to be changed
            value: The new value for the attribute
        
        Returns:
            -
        
        Raises:
            ValueError: If the attribute's value and type fails. 
        """
        if name == 'change' and type(value) != GerritChange:
            raise ValueError('%s must be a GerritChange' % name)
        elif name == 'patch_set' and type(value) != GerritPatchSet:
            raise ValueError('%s must be a GerritPatchSet' % name)
        elif name == 'uploader' and type(value) != GerritAccount:
            raise ValueError('%s must be a GerritAccount' % name)
        object.__setattr__(self, name, value)
    
    @classmethod
    def decode(cls, dct):
        """Returns a GerritPatchSetCreatedEvent object decoded from ``dct``.
        
        Args:
            dct: Dictionary with all values required to initalise a
                GerritPatchSetCreatedEvent object.
        
        Returns:
            A fully initialised GerritPatchSetCreatedEvent object.
            
        Raises:
            DecodeError: If ``dct`` does't contain all required keys
        """
        try:
            return GerritPatchSetCreatedEvent(change=GerritChange.decode(dct['change']),
                                              patch_set=GerritPatchSet.decode(dct['patchSet']),
                                              uploader=GerritAccount.decode(dct['uploader']))
        except KeyError, ex:
            raise DecodeError(ex)


class GerritChangeAbandonedEvent(GerritEvent):
    """Represents a change-abandoned event in Gerrit."""

    def __init__(self, change, abandoner, reason):
        """Creates a GerritChangeAbandonedEvent object from given parameters.
        
        Args:
            change: The GerritChange object that was abandoned
            abandoner: The GerritAccount object that abandoned the change
            reason: A string with the reason why the change was abandoned
        
        Returns:
            An instanciated GerritChangeAbandonedEvent object

        Raises:
            ValueError: If any of the paramters have a wrong type
        """
        GerritEvent.__init__(self)
        self.change = change
        self.abandoner = abandoner
        self.reason = reason
    
    def __setattr__(self, name, value):
        """Sets the object's attribute ``name`` to ``value``.
        
        Args:
            name: A string representing the name of the attribute that's about
                to be changed
            value: The new value for the attribute
        
        Returns:
            -
        
        Raises:
            ValueError: If the attribute's value and type fails. 
        """
        if name == 'change' and type(value) != GerritChange:
            raise ValueError('%s must be a GerritChange' % name)
        elif name == 'abandoner' and type(value) != GerritAccount:
            raise ValueError('%s must be a GerritAccount' % name)
        elif name == 'reason' and type(value) not in (str, unicode):
            raise ValueError('%s must be a string' % name)
        object.__setattr__(self, name, value)
        
    @classmethod
    def decode(cls, dct):
        """Returns a GerritChangeAbandonedEvent object decoded from ``dct``.
        
        Args:
            dct: Dictionary with all values required to initalise a
                GerritChangeAbandonedEvent object.
        
        Returns:
            A fully initialised GerritChangeAbandonedEvent object.
            
        Raises:
            DecodeError: If ``dct`` does't contain all required keys
        """
        try:
            return GerritChangeAbandonedEvent(change=GerritChange.decode(dct['change']), 
                                              abandoner=GerritAccount.decode(dct['abandoner']), 
                                              reason=dct['reason'])
        except KeyError, ex:
            raise DecodeError(ex)


class GerritChangeRestoredEvent(GerritEvent):
    """Represents a change-restored event in Gerrit."""

    def __init__(self, change, restorer, reason):
        """Creates a GerritChangeRestoredEvent object from given parameters.
        
        Args:
            change: The GerritChange object that was restored
            restorer: The GerritAccount object that restored the change
            reason: A string with the reason why the change was restored
        
        Returns:
            An instanciated GerritChangeRestoredEvent object

        Raises:
            ValueError: If any of the paramters have a wrong type
        """
        GerritEvent.__init__(self)
        self.change = change
        self.restorer = restorer
        self.reason = reason
    
    def __setattr__(self, name, value):
        """Sets the object's attribute ``name`` to ``value``.
        
        Args:
            name: A string representing the name of the attribute that's about
                to be changed
            value: The new value for the attribute
        
        Returns:
            -
        
        Raises:
            ValueError: If the attribute's value and type fails. 
        """
        if name == 'change' and type(value) != GerritChange:
            raise ValueError('%s must be a GerritChange' % name)
        elif name == 'restorer' and type(value) != GerritAccount:
            raise ValueError('%s must be a GerritAccount' % name)
        elif name == 'reason' and type(value) not in (str, unicode):
            raise ValueError('%s must be a string' % name)
        object.__setattr__(self, name, value)
    
    @classmethod
    def decode(cls, dct):
        """Returns a GerritChangeRestoredEvent object decoded from ``dct``.
        
        Args:
            dct: Dictionary with all values required to initalise a
                GerritChangeRestoredEvent object.
        
        Returns:
            A fully initialised GerritChangeRestoredEvent object.
            
        Raises:
            DecodeError: If ``dct`` does't contain all required keys
        """
        try:
            return GerritChangeRestoredEvent(change=GerritChange.decode(dct['change']),
                                             restorer=GerritAccount.decode(dct['restorer']),
                                             reason=dct['reason'])
        except KeyError, ex:
            raise DecodeError(ex)


class GerritChangeMergedEvent(GerritEvent):
    """Represents a change-merged event in Gerrit."""

    def __init__(self, change, patch_set, submitter):
        """Creates a GerritChangeMergedEvent object from given parameters.
        
        Args:
            change: The GerritChange object that was merged
            patch_set: The GerritPatchSet object that was merged
            submitter: The GerritAccount object naming the person who did
                the merge
        
        Returns:
            An instanciated GerritChangeMergedEvent object

        Raises:
            ValueError: If any of the paramters have a wrong type
        """
        GerritEvent.__init__(self)
        self.change = change
        self.patch_set = patch_set
        self.submitter = submitter
    
    def __setattr__(self, name, value):
        """Sets the object's attribute ``name`` to ``value``.
        
        Args:
            name: A string representing the name of the attribute that's about
                to be changed
            value: The new value for the attribute
        
        Returns:
            -
        
        Raises:
            ValueError: If the attribute's value and type fails. 
        """
        if name == 'change' and type(value) != GerritChange:
            raise ValueError('%s must be a GerritChange' % name)
        elif name == 'patch_ser' and type(value) != GerritPatchSet:
            raise ValueError('%s must be a GerritPatchSet' % name)
        elif name == 'submitter' and type(value) != GerritAccount:
            raise ValueError('%s must be a GerritAccount' % name)
        object.__setattr__(self, name, value)
        
    @classmethod
    def decode(cls, dct):
        """Returns a GerritChangeMergedEvent object decoded from ``dct``.
        
        Args:
            dct: Dictionary with all values required to initalise a
                GerritChangeMergedEvent object.
        
        Returns:
            A fully initialised GerritChangeMergedEvent object.
            
        Raises:
            DecodeError: If ``dct`` does't contain all required keys
        """
        try:
            return GerritChangeMergedEvent(change=GerritChange.decode(dct['change']),
                                           patch_set=GerritPatchSet.decode(dct['patchSet']),
                                           submitter=GerritAccount.decode(dct['submitter']))
        except KeyError, ex:
            raise DecodeError(ex)


class GerritRefUpdatedEvent(GerritEvent):
    """Represents a ref-updated event in Gerrit."""

    def __init__(self, ref_update):
        """Creates a GerritRefUpdatedEvent object from given parameters.
        
        Args:
            ref_update: The GerritRefUpdate object containing the update
                information.
        
        Returns:
            An instanciated GerritRefUpdatedEvent object

        Raises:
            ValueError: If any of the paramters have a wrong type
        """
        GerritEvent.__init__(self)
        self.ref_update = ref_update
    
    def __setattr__(self, name, value):
        """Sets the object's attribute ``name`` to ``value``.
        
        Args:
            name: A string representing the name of the attribute that's about
                to be changed
            value: The new value for the attribute
        
        Returns:
            -
        
        Raises:
            ValueError: If the attribute's value and type fails. 
        """
        if name == 'ref_update' and type(value) != GerritRefUpdate:
            raise ValueError('%s must be a GerritRefUpdate' % name)
        object.__setattr__(self, name, value)
    
    @classmethod
    def decode(cls, dct):
        """Returns a GerritRefUpdatedEvent object decoded from ``dct``.
        
        Args:
            dct: Dictionary with all values required to initalise a
                GerritRefUpdatedEvent object.
        
        Returns:
            A fully initialised GerritRefUpdatedEvent object.
            
        Raises:
            DecodeError: If ``dct`` does't contain all required keys
        """
        try:
            return GerritRefUpdatedEvent(ref_update=GerritRefUpdate.decode(dct['refUpdate']))
        except KeyError, ex:
            raise DecodeError(ex)


class GerritCommentAddedEvent(GerritEvent):
    """Represents a comment-added event in Gerrit.
    
    A comment-added event is emitted when somebody reviews a change and
    publishes her comments.
    """

    def __init__(self, approvals, comment, change, author, patch_set):
        """Creates a GerritCommentAddedEvent object from given parameters.
        
        Args:
            approvals: A list of GerritApproval objects containing 
                information about the codereview and verification status.
            comment: The actual comment as a string. This is the text entered
                in "Cover Message" text field when doing a review in Gerrit.
            change: The GerritChange object that the comment refers to
            author: The GerritAccount object of the author that posted the
                comment
            patch_set: The GerritPatchSet object that was reviews by the author 
        
        Returns:
            An instanciated GerritCommentAddedEvent object

        Raises:
            ValueError: If any of the paramters have a wrong type
        """
        GerritEvent.__init__(self)
        self.approvals = approvals
        self.comment = comment
        self.change = change
        self.author = author
        self.patch_set = patch_set
    
    def __setattr__(self, name, value):
        """Sets the object's attribute ``name`` to ``value``.
        
        Args:
            name: A string representing the name of the attribute that's about
                to be changed
            value: The new value for the attribute
        
        Returns:
            -
        
        Raises:
            ValueError: If the attribute's value and type fails. 
        """
        if name == 'approvals':
            if type(value) != list:
                raise ValueError('% must be a list' % name)
            for approval in value:
                if type(approval) != GerritApproval:
                    raise ValueError('each approval must be a GerritApproval')
        elif name == 'comment' and type(value) not in (str, unicode):
            raise ValueError('%s must be a string' % name)
        elif name == 'change' and type(value) != GerritChange:
            raise ValueError('%s must be a GerritChange' % name)
        elif name == 'author' and type(value) != GerritAccount:
            raise ValueError('%s must be a GerritAccount' % name)
        elif name == 'patch_set' and type(value) != GerritPatchSet:
            raise ValueError('%s must be a GerritPatchSet' % name)
        object.__setattr__(self, name, value)
    
    @classmethod
    def decode(cls, dct):
        """Returns a GerritCommentAddedEvent object decoded from ``dct``.
        
        Args:
            dct: Dictionary with all values required to initalise a
                GerritCommentAddedEvent object.
        
        Returns:
            A fully initialised GerritCommentAddedEvent object.
            
        Raises:
            DecodeError: If ``dct`` does't contain all required keys
        """
        try:
            obj = GerritCommentAddedEvent(approvals=GerritApproval.decode(dct['approvals']),
                                          comment=dct['comment'],
                                          change=GerritChange.decode(dct['change']),
                                          author=GerritAccount.decode(dct['author']),
                                          patch_set=GerritPatchSet.decode(dct['patchSet']))
            return obj
        except KeyError, ex:
            raise DecodeError(ex)

