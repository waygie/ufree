import re
import datetime

class ApiInputValidator:

	#just letters, numbers, and spaces
	__event_name_pattern = {}
	__event_name_length = 50
	__event_creator_pattern = {}
	__event_creator_length = 25

	def validate_event(self, eventObject):
		'''
		Validates each field of the event object.

		Returns a list of error messages or an empty list if none found.
		'''

		error_messages = []

		# Validate name field
		if 'name' in eventObject:
			if not isinstance(eventObject['name'], str):
				error_messages.append('Name must be a string')

			if len(eventObject['name']) > self.__event_name_length:
				message = 'Name must be less than {0} characters'.format(
					self.__event_name_length
				)
				error_messages.append()

			if re.search(self.__event_name_pattern , eventObject['name']):
				error_messages.append('Name must only contain letters or numbers')
		else:
			error_messages.append('Name is blank. A value for name is required')

		# Validate creator field
		if 'creator' in eventObject:
			if not isinstance(eventObject['creator'], str):
				error_messages.append('Creator must be a string')

			if len(eventObject['creator']) > self.__event_creator_length:
				message = 'Creator must be less than {0} characters'.format(
					self.__event_creator_length
				)
				error_messages.append(message)

			if re.search(self.__event_creator_pattern, eventObject['creator']):
				error_messages.append('Creator must only contain letters or numbers')
		else:
			error_messages.append('Creator is blank. A value for creator is required')

		return error_messages
