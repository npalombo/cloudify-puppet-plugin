import unittest
import os

from puppet_classifier.groups import GroupClient, Group


class TestGroups(unittest.TestCase):

    def setUp(self):
        puppet_endpoint_url = os.environ['puppet_endpoint_url']
        cert = os.environ.get('cert')
        key = os.environ.get('key')
        cacert = os.environ.get('cacert')
        self.group_client = GroupClient(puppet_endpoint_url, cert, key, cacert)

    def tearDown(self):
        pass

    def test_retrieve_all(self):
        status_code, groups = self.group_client.retrieve_all()
        self.assertEquals(status_code, 200)
        self.assertIsNotNone(groups)
        self.assertTrue(isinstance(groups, list))
        self.assertGreater(len(groups), 0)
        self.assertTrue(isinstance(groups[0], dict))
        self.assertTrue(groups[0].has_key('id'))

    def test_retrieve_all_inherited(self):
        status_code, groups = self.group_client.retrieve_all(inherited=True)
        self.assertEquals(status_code, 200)
        self.assertIsNotNone(groups)
        self.assertTrue(isinstance(groups, list))
        self.assertGreater(len(groups), 0)
        self.assertTrue(isinstance(groups[0], dict))
        self.assertTrue(groups[0].has_key('id'))

    def test_retrieve(self):
        status_code, groups = self.group_client.retrieve_all()
        self.assertEquals(status_code, 200)
        self.assertIsNotNone(groups)
        self.assertTrue(isinstance(groups, list))
        self.assertGreater(len(groups), 0)
        self.assertTrue(isinstance(groups[0], dict))
        self.assertTrue(groups[0].has_key('id'))
        group_id = groups[0]['id']

        status_code, group = self.group_client.retrieve(group_id)
        self.assertEquals(status_code, 200)
        self.assertIsNotNone(group)
        self.assertTrue(isinstance(group, dict))
        self.assertTrue(group.has_key('id'))

    def test_validate(self):
        status_code, groups = self.group_client.retrieve_all()
        self.assertEquals(status_code, 200)
        self.assertIsNotNone(groups)
        self.assertTrue(isinstance(groups, list))
        self.assertGreater(len(groups), 0)
        self.assertTrue(isinstance(groups[0], dict))
        self.assertTrue(groups[0].has_key('id'))
        parent_id = groups[0]['id']

        group = Group('validation_test', parent_id, ["and",["~","name","^apache.*$"]], {"apache": {}})
        status_code, valid_group = self.group_client.validate(group)
        self.assertEquals(status_code, 200)
        self.assertIsNotNone(valid_group)
        self.assertTrue(isinstance(valid_group, dict))
        self.assertTrue(valid_group.has_key('id'))

    def test_create(self):
        group_id = None
        try:
            status_code, groups = self.group_client.retrieve_all()
            self.assertEquals(status_code, 200)
            self.assertIsNotNone(groups)
            self.assertTrue(isinstance(groups, list))
            self.assertGreater(len(groups), 0)
            self.assertTrue(isinstance(groups[0], dict))
            self.assertTrue(groups[0].has_key('id'))
            parent_id = groups[0]['id']

            group = Group('create_test', parent_id, ["and",["~","name","^apache.*$"]], {"apache": {}})
            status_code, create_group = self.group_client.create(group)
            self.assertEquals(status_code, 200)
            self.assertIsNotNone(create_group)
            self.assertTrue(isinstance(create_group, dict))
            self.assertTrue(create_group.has_key('id'))
            group_id = create_group['id']
        finally:
            if group_id is not None:
                self.group_client.delete(group_id)

    def test_update(self):
        group_id = None
        try:
            status_code, groups = self.group_client.retrieve_all()
            self.assertEquals(status_code, 200)
            self.assertIsNotNone(groups)
            self.assertTrue(isinstance(groups, list))
            self.assertGreater(len(groups), 0)
            self.assertTrue(isinstance(groups[0], dict))
            self.assertTrue(groups[0].has_key('id'))
            parent_id = groups[0]['id']

            group = Group('update_test', parent_id, ["and",["~","name","^apache.*$"]], {"apache": {}})
            status_code, create_group = self.group_client.create(group)
            self.assertEquals(status_code, 200)
            self.assertIsNotNone(create_group)
            self.assertTrue(isinstance(create_group, dict))
            self.assertTrue(create_group.has_key('id'))
            group_id = create_group['id']
            self.assertTrue(create_group.has_key('classes'))
            classes = create_group['classes']
            self.assertTrue(classes.has_key('apache'))
            apache = classes['apache']
            apache['serveradmin'] = 'test@bankofamerica.com'

            status_code, update_group = self.group_client.update(create_group, group_id)
            self.assertEquals(status_code, 200)
            self.assertIsNotNone(update_group, group_id)
            self.assertTrue(isinstance(update_group, dict))
            self.assertTrue(update_group.has_key('classes'))
            classes = update_group['classes']
            self.assertTrue(classes.has_key('apache'))
            apache = classes['apache']
            self.assertTrue(apache.has_key('serveradmin'))
            serveradmin = apache['serveradmin']
            self.assertEquals(serveradmin, 'test@bankofamerica.com')
        finally:
            if group_id is not None:
                self.group_client.delete(group_id)

    def test_delete(self):
        status_code, groups = self.group_client.retrieve_all()
        self.assertEquals(status_code, 200)
        self.assertIsNotNone(groups)
        self.assertTrue(isinstance(groups, list))
        self.assertGreater(len(groups), 0)
        self.assertTrue(isinstance(groups[0], dict))
        self.assertTrue(groups[0].has_key('id'))
        parent_id = groups[0]['id']

        group = Group('create_test', parent_id, ["and",["~","name","^apache.*$"]], {"apache": {}})
        status_code, create_group = self.group_client.create(group)
        self.assertEquals(status_code, 200)
        self.assertIsNotNone(create_group)
        self.assertTrue(isinstance(create_group, dict))
        self.assertTrue(create_group.has_key('id'))
        group_id = create_group['id']

        status_code, body = self.group_client.delete(group_id)
        self.assertEquals(status_code, 204)
