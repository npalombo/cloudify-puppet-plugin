__author__ = 'npalombo'

"""
Module for handling the Group endpoint of the Puppet Classification API
"""

import json

from client import HTTPClient, handle_response


class Group(object):
    """
    Class used to create Group JSON structure
    """

    def __init__(self, name, parent, rule, classes, variables=None, environment=None, environment_trumps=None, description=None):
        self.name               = name
        self.parent             = parent
        self.rule               = rule
        self.classes            = classes
        self.variables          = variables
        self.environment        = environment
        self.environment_trumps = environment_trumps
        self.description        = description

    def to_json(self):
        data = self.__dict__
        for key, val in data.items():
            if val is None:
                del data[key]
        return json.dumps(data)


class GroupClient(HTTPClient):
    """
    Handles the methods of the Group endpoint
    """

    def retrieve(self, group_id):
        """
        Retrieve a group by id.
        Response will be JSON dictionary.
        Raises an exception if HTTP 200 not received.
        """
        path = 'groups/%s' % group_id
        r = self._get(path)
        return handle_response(r)

    def retrieve_all(self, inherited=False):
        """
        Retrieve a all groups. Set inherited to True to retrieve all inherited classes in each group.
        Response will be a list of JSON dictionaries.
        Raises an exception if HTTP 200 not received.
        """
        path = 'groups'
        params = None
        if inherited:
            params = { 'inherited': True }
        r = self._get(path, params)
        return handle_response(r)

    def validate(self, group):
        """
        Validate Group object JSON without creating object in Puppet DB.
        Response will be JSON dictionary.
        Raises an exception if HTTP 200 not received.
        """
        path = 'validate/group'
        body = group.to_json()
        r = self._post(path, body)
        return handle_response(r)

    def create(self, group):
        """
        Create new group in Puppet DB from Group object JSON.
        Response will be JSON dictionary.
        Raises an exception if HTTP 200 not received.
        """
        path = 'groups'
        body = group.to_json()
        r = self._post(path, body)
        return handle_response(r)

    def update(self, group_delta, group_id):
        """
        Update group with given id in Puppet DB from differences in Group object JSON.
        Response will be JSON dictionary.
        Raises an exception if HTTP 200 not received.
        """
        path = 'groups/%s' % group_id
        if group_delta.has_key('rule'):
            del group_delta['rule']
        body = json.dumps(group_delta)
        r = self._post(path, body)
        return handle_response(r)

    def delete(self, group_id):
        """
        Delete group with given id from Puppet DB.
        Response will be empty string.
        Raises an exception if HTTP 200 not received.
        """
        path = 'groups/%s' % group_id
        r = self._delete(path)
        return handle_response(r)
