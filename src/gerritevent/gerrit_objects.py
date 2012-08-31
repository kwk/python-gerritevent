"""
Copyright (c) 2012 GONICUS GmbH
License: LGPL
Author: Konrad Kleine <kleine@gonicus.de>
"""


class Error(Exception):
    """The basis for all error classes of this module."""
    pass


class DecodeError(Error):
    """Identifies an error when decoding any subclass of GerritObject."""
    pass


class GerritObject(object):
    """This is the base class for all Gerrit objects.
    
    Instances of GerritObject sublasses are composed as events
    (see. GerritEvent). 
    """
    
    def __init__(self):
        """Initializes a GerritObject object from the given parameters."""
        object.__init__(self)


class GerritAccount(GerritObject):
    """Represents any person type of object inside of Gerrit events.
    
    For instance an uploader, an abandoner, an owner, etc. all of these are
    represented using a GerritAccount` object
    (e.g uploader,    owner, abandoner, etc.).
    """

    def __init__(self, name, email):
        """Initializes a GerritAccount object from the given parameters."""
        GerritObject.__init__(self)
        self.name = name
        self.email = email

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
        if name == 'name' and type(value) not in (str, unicode):
            raise ValueError('%s must be a string' % name)
        elif name == 'email' and type(value) not in (str, unicode):
            raise ValueError('%s must be a string' % name)
        object.__setattr__(self, name, value)
        
    @classmethod
    def decode(cls, dct):
        """Returns a GerritAccount object decoded from ``dct``.
        
        Args:
            dct: Dictionary with all values required to initalise a
                GerritAccount object.
        
        Returns:
            A fully initialised GerritAccount object.
            
        Raises:
            DecodeError: If ``dct`` does't contain all required keys
        """
        try:
            return GerritAccount(name=dct['name'], email=dct['email'])
        except KeyError, ex:
            raise DecodeError(ex)


class GerritChange(GerritObject):
    """Represents a change in Gerrit."""

    def __init__(self, project, branch, change_id, number, subject, owner,
                 url):
        """Initializes a GerritChange object from the given parameters."""
        GerritObject.__init__(self)
        self.project = project
        self.branch = branch
        self.change_id = change_id
        self.number = number
        self.subject = subject
        self.owner = owner
        self.url = url
    
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
        if name == 'project' and type(value) not in (str, unicode):
            raise ValueError('%s must be a string' % name)
        elif name == 'branch' and type(value) not in (str, unicode):
            raise ValueError('%s must be a string' % name)
        elif name == 'change_id' and type(value) not in (str, unicode):
            raise ValueError('%s must be a string' % name)
        elif name == 'number':
            try:
                value = int(value)
            except ValueError:
                raise ValueError('%s must be an int' % name)
        elif name == 'subject' and type(value) not in (str, unicode):
            raise ValueError('%s must be a string' % name )
        elif name == 'owner' and type(value) != GerritAccount:
            raise ValueError('%s must be a GerritAccount' % name)
        elif name == 'url' and type(value) not in (str, unicode):
            raise ValueError('%s must be a string' % name)
        object.__setattr__(self, name, value)
    
    @classmethod
    def decode(cls, dct):
        """Returns a GerritChange object decoded from ``dct``.
        
        Args:
            dct: Dictionary with all values required to initalise a
                GerritChange object.
        
        Returns:
            A fully initialised GerritChange object.
            
        Raises:
            DecodeError: If ``dct`` does't contain all required keys
        """
        try:
            return GerritChange(project=dct['project'], branch=dct['branch'],
                                change_id=dct['id'], number=dct['number'],
                                subject=dct['subject'], url=dct['url'],
                                owner=GerritAccount.decode(dct['owner']))
        except KeyError, ex:
            raise DecodeError(ex)


class GerritPatchSet(GerritObject):
    """Represents a patch-set in Gerrit."""

    def __init__(self, number, revision, ref, uploader, created_on):
        """Initializes a GerritPatchSet object from the given parameters."""
        GerritObject.__init__(self)
        self.number = number
        self.revision = revision
        self.ref = ref
        self.uploder = uploader
        self.created_on = created_on
        
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
        if name == 'number':
            try:
                value = int(value)
            except ValueError:
                raise ValueError('%s must be an int' % name)
        elif name == 'revision' and type(value) not in (str, unicode):
            raise ValueError('%s must be a string' % name)
        elif name == 'ref' and type(value) not in (str, unicode):
            raise ValueError('%s must be a string' % name)
        elif name == 'uploader' and type(value) != GerritAccount:
            raise ValueError('%s must be a GerritAccount' % name)
        elif name == 'created_on' and type(value) != int:
            raise ValueError('%s must be a string' % name)
        object.__setattr__(self, name, value)
    
    @classmethod
    def decode(cls, dct):
        """Returns a GerritPatchSet object decoded from ``dct``.
        
        Args:
            dct: Dictionary with all values required to initalise a
                GerritPatchSet object.
        
        Returns:
            A fully initialised GerritPatchSet object.
            
        Raises:
            DecodeError: If ``dct`` does't contain all required keys
        """
        try:
            return GerritPatchSet(number=dct['number'],
                                  ref=dct['ref'],
                                  revision=dct['revision'],
                                  uploader=GerritAccount.decode(dct['uploader']),
                                  created_on=dct['createdOn'])
        except KeyError, ex:
            raise DecodeError(ex)


class GerritRefUpdate(GerritObject):
    """Represents a refUpdate in Gerrit."""

    def __init__(self, old_rev, new_rev, ref_name, project):
        """Initializes a GerritRefUpdate object from the given parameters."""
        GerritObject.__init__(self)
        self.old_rev = old_rev
        self.new_rev = new_rev
        self.ref_name = ref_name
        self.project = project
    
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
        if name == 'old_rev' and type(value) not in (str, unicode):
            raise ValueError('%s must be a string' % name)
        elif name == 'new_rev' and type(value) not in (str, unicode):
            raise ValueError('%s must be a string' % name)
        elif name == 'ref_name' and type(value) not in (str, unicode):
            raise ValueError('%s must be a string' % name)
        elif name == 'project' and type(value) not in (str, unicode):
            raise ValueError('%s must be a string' % name)
        object.__setattr__(self, name, value)
    
    @classmethod
    def decode(cls, dct):
        """Returns a GerritRefUpdate object decoded from ``dct``.
        
        Args:
            dct: Dictionary with all values required to initalise a
                GerritRefUpdate object.
        
        Returns:
            A fully initialised GerritRefUpdate object.
            
        Raises:
            DecodeError: If ``dct`` does't contain all required keys
        """
        try:
            return GerritRefUpdate(old_rev=dct['oldRev'],
                                   new_rev=dct['newRev'],
                                   ref_name=dct['refName'],
                                   project=dct['project'])
        except KeyError, ex:
            raise DecodeError(ex)


class GerritApproval(GerritObject):
    """Represents an approval in Gerrit.
    TODO(kleine): Add documentation for CODEREVIEW and VERIFIED strings.
    """

    CODEREVIEW = 'CRVW'

    VERIFIED = 'VRIF'
    
    types = [CODEREVIEW, VERIFIED]

    def __init__(self, value, _type, description):
        """Initializes a GerritApproval object from the given parameters."""
        GerritObject.__init__(self)
        self.value = value
        self._type = _type
        self.description = description
    
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
        if name == 'value':
            try:
                value = int(value)
            except ValueError:
                raise ValueError('%s must be an int' % name)
        elif name == '_type' and value not in GerritApproval.types:
            raise ValueError('%s must be in GerritApproval.types' % name)
        elif name == 'description' and type(value) not in (str, unicode):
            raise ValueError('%s must be a string' % name)
        object.__setattr__(self, name, value)
    
    @classmethod
    def decode(cls, lst):
        """Returns a list of GerritApproval objects decoded from ``lst``.
        
        Args:
            dct: List of dictionaries. Each dictionary must have all keys
                required to initalise a GerritAppproval object.
        
        Returns:
            A list of fully initialised GerritApproval objects.
            
        Raises:
            DecodeError: If ``dct`` does't contain all required keys
        """
        approvals = []
        for dct in lst:
            try:
                approval = GerritApproval(value=dct['value'],
                                          _type=dct['type'],
                                          description=dct['description'])
            except KeyError, ex:
                raise DecodeError(ex)
            approvals.append(approval)
        return approvals
