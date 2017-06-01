from classes.util.AttendeeDao import AttendeeValidator
from classes.dao.AttendeeDao import AttendeeDao
from classes.exception.ValidationException import ValidationException
def UserFilter():

    def __init__ (self):
        # init DAO based on environment
        self.__inputValidator = AttendeeValidator()
        if os.environ['ENV'] == 'test':
            temp = importlib.import_module('test.classes.AttendeeDao')
            self.__attendee_dao = temp.AttendeeDao()
        else:
            temp = importlib.import_module('classes.dao.AttendeeDao')
            self.__attendee_dao = temp.AttendeeDao()

    def __create_new_user (self, req_body):
        # Get the creator or attendee name.
        attendee_name = ''
        if 'creator' in req_body.payload:
            attendee_name = req_body.payload['creator']
        elif 'name' in req_body.payload:
            attendee_name = req_body.payload['name']

        # If neither is found, then this is a bad request
        if not attendee_name:
            raise ValidationException(
                'Name for this user could not be located'
            )

        # create a new user with the provided name
        att = self.__attendee_dao.save_attendee({
            'name': attendee_name
        })

        # attach the user ID to the request
        req_body['id'] = att['id']
        return req_body

    def set_user_id (self, req_body):
        if 'id' in req_body and req_body['id']:
            # throws exception on failure
            self.__inputValidator.validate_attendee_id(req_body['id'])
            if self.__attendee_dao.attendee_exists(req_body['id']):
                return req_body
            else:
                # stale cookie. create new user and overwrite existing cookie
                return self.__create_new_user(req_body)
        else:
            return self.__create_new_user(req_body)