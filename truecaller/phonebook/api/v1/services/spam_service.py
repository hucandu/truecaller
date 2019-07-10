from phonebook.models import PhoneBook, SpamMarker
from django.contrib.auth.models import User


class NumberSpamService():
	"""this is used to mark the given number as spam"""

	@classmethod
	def mark_given_number_as_spam(self, user, phone):
		user = PhoneBook.objects.filter(phone_number=user).first().user
		phone_book, created = PhoneBook.objects.get_or_create(
    		phone_number=phone,
    		defaults={'user': None},
		)
		spam_marker, created = SpamMarker.objects.get_or_create(
    		spammer=phone_book,
    		defaults={'marked_by': user},
		)
		if created:
			return True
		else:
			return False
