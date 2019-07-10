from phonebook.models import PhoneNumberOwnerName
from phonebook.models import PhoneBook
from itertools import chain


class SearchService():

    @classmethod
    def search_by_name(self, char):
        phone_number_owners_start_names = PhoneNumberOwnerName.objects.filter(name__startswith=char)
        phone_number_owners_start_names_id = phone_number_owners_start_names.values_list( "id", flat = True )
        phone_number_owners_contains = PhoneNumberOwnerName.objects.filter(name__icontains=char).exclude(id__in=phone_number_owners_start_names_id)
        return list(chain(phone_number_owners_start_names,phone_number_owners_contains))


    @classmethod
    def search_by_phone(self, number):
        phone_book_registerd = PhoneBook.objects.filter(phone_number=number).first()
        if phone_book_registerd:
            return phone_book_registerd.phonenumberownername_set.all()
        else:
            PhoneNumberOwnerName.objects.filter(phone_number=number)
