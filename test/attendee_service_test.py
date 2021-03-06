import os
import json
import unittest
import hashlib
import builtins
import test.classes.const as const
from test.classes.mock_request import MockRequest
from classes.service.attendee_service import AttendeeService
from classes.exception.service_exception import ServiceException

class AttendeeServiceTest(unittest.TestCase):

    def setUp (self):
        os.environ['TEST_DB_FAIL'] = 'False'
        self.__attendee_service = AttendeeService()

    def load_event_attendees_test (self):
        # test correct usage
        req = MockRequest(event_id=const.GOOD_EVENT_ID)
        ret = self.__attendee_service.load_event_attendees(req)
        data = json.loads(ret.json_body)
        self.assertEqual(len(data), 2)
        self.assertTrue('name' in data[0])
        self.assertTrue('id' in data[0])
        self.assertTrue('name' in data[1])
        self.assertTrue('id' in data[1])

        # test bad event id
        try:
            req = MockRequest(event_id='dasfasdfasdasf')
            ret = self.__attendee_service.load_event_attendees(req)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ServiceException))

        # test db exception
        os.environ['TEST_DB_FAIL'] = 'True'
        try:
            req = MockRequest(event_id=const.GOOD_EVENT_ID)
            self.__attendee_service.load_event_attendees(req)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ServiceException))

    def load_attendee_test (self):
        # test correct usage
        req = MockRequest(attendee_id=const.GOOD_USER_ID)
        ret = self.__attendee_service.load_attendee(req)
        data = json.loads(ret.json_body)
        self.assertEqual(len(data), 3)
        self.assertTrue('name' in data)
        self.assertTrue('id' in data)
        self.assertTrue('email' in data)

        # test bad event id
        try:
            req = MockRequest(attendee_id='()*^@#^)')
            ret = self.__attendee_service.load_attendee(req)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ServiceException))

        # test db exception
        os.environ['TEST_DB_FAIL'] = 'True'
        try:
            req = MockRequest(attendee_id=const.GOOD_USER_ID)
            self.__attendee_service.load_attendee(req)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ServiceException))

    def update_attendee_test (self):
        # test good field names
        post_body = {
            'id': const.GOOD_USER_ID,
            'name': 'New Name'
        }
        req = MockRequest(body=post_body)
        ret = self.__attendee_service.update_attendee(req)
        self.assertTrue('name' in ret.json_body)
        self.assertTrue('id' in ret.json_body)

        # test bad request names
        try:
            ret = self.__attendee_service.update_attendee({
                'name-o': 'idk some event',
                'creatGuy': 'timmy t i guess'
            })
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ServiceException))

    def update_attendee_availability_test (self):
        pass

    def create_attendee_test (self):
        # test good field names
        builtins.db_return_object = [['123abcd', 'Juan', 'juan@juan.esp']]
        post_body = {
            'name': 'New Name'
        }
        req = MockRequest(body=post_body, event_id=const.GOOD_EVENT_ID)
        ret = self.__attendee_service.create_attendee(req)
        self.assertTrue('name' in ret.json_body)
        self.assertTrue('id' in ret.json_body)

        # test bad request names
        try:
            ret = self.__attendee_service.create_attendee({
                'name-o': 'idk some event'
            })
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ServiceException))

    def remove_attendee_from_event_test (self):
        # test correct usage
        post_body = {
            'id': const.GOOD_USER_ID
        }
        req = MockRequest(
            body = post_body,
            event_id = const.GOOD_EVENT_ID
        )
        ret = self.__attendee_service.remove_attendee_from_event(req)

        # test bad event id
        try:
            post_body = {
                'id': '()*^@#^)'
            }
            req = MockRequest(
                body = post_body,
                event_id = const.GOOD_EVENT_ID
            )
            ret = self.__attendee_service.remove_attendee_from_event(req)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ServiceException))

        # test db exception
        os.environ['TEST_DB_FAIL'] = 'True'
        try:
            req = MockRequest(
                body = post_body,
                event_id = const.GOOD_EVENT_ID
            )
            self.__attendee_service.remove_attendee_from_event(req)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ServiceException))

    def add_attendee_to_event_test (self):
        # test correct usage
        post_body = {
            'id': const.GOOD_USER_ID,
            'name': 'Delete Me'
        }
        req = MockRequest(
            body = post_body,
            event_id = const.GOOD_EVENT_ID
        )
        ret = self.__attendee_service.add_attendee_to_event(req)

        # test bad event id
        try:
            post_body = {
                'id': '()*^@#^)',
                'name': ') DROP TABLE users'
            }
            req = MockRequest(
                body = post_body,
                event_id = const.GOOD_EVENT_ID
            )
            ret = self.__attendee_service.add_attendee_to_event(req)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ServiceException))

        # test db exception
        os.environ['TEST_DB_FAIL'] = 'True'
        try:
            req = MockRequest(
                body = post_body,
                event_id = const.GOOD_EVENT_ID
            )
            self.__attendee_service.add_attendee_to_event(req)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, ServiceException))
