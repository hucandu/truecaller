import names
import random
import json
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate
from user_management import views as user_views
from phonebook.v1 import views as phonebook_view
from phonebook.models import PhoneBook, PhoneNumberOwnerName


class TrueCallerTestCase(TestCase):

    def setUp(self):
        self.register_url = "/authentication/register/"
        self.login_url = "/authentication/user_login/"
        self.search_url = "/search"
        self.marK_spam_url = "/mark_spam/"
        self.username = "7777777777"
        self.email = "omega@gmail.com"
        self.password = "654321"
        self.name = names.get_first_name()
        for x in range(1000):
            random_number = random.randint(9870000000, 9870000010)
            phone_book, is_created = PhoneBook.objects.get_or_create(
                phone_number=random_number)
            phone_number_owner_name = PhoneNumberOwnerName(
                phone_number=phone_book, name=names.get_first_name())
            phone_number_owner_name.save()
        self.unregisterd_phone_number = PhoneBook.objects.first().phone_number
        self.spam_number = random.randint(9870000000, 9870000010)

    def test_registration(self):
        factory = APIRequestFactory()
        request = factory.post(self.register_url, {
            "name": self.name,
            "email": self.email,
            "phone_number": self.username,
            "password": self.password
        }, format='json')
        response = user_views.register(request)
        print(response.data)
        print("*" * 50)
        self.assertEqual(200, response.status_code)
        return response.data['access_token']

    def test_login(self):
        factory = APIRequestFactory()
        request = factory.post(self.login_url, {
            "username": self.username,
            "password": self.password
        }, format='json')
        response = user_views.token(request)
        print(response.data)
        print("*" * 50)
        self.assertEqual(200, response.status_code)

    def test_search_by_name(self):
        url = "{search_url}?name={name}".format(
            search_url=self.search_url, name="mary")
        factory = APIRequestFactory()
        access_token = self.test_registration()
        request = factory.get(
            url, HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
        force_authenticate(
            request, user=User.objects.get(username=self.username))
        search_view = phonebook_view.SearchView.as_view()
        response = search_view(request)
        print(response.data)
        print("*" * 50)
        self.assertEqual(200, response.status_code)

    def test_search_by_phone_number(self):
        print("UNREGISTERD NUMBER")
        url = "{search_url}?phone_number={phone}".format(
            search_url=self.search_url, phone=self.unregisterd_phone_number)
        factory = APIRequestFactory()
        access_token = self.test_registration()
        request = factory.get(
            url, HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
        force_authenticate(
            request, user=User.objects.get(username=self.username))
        search_view = phonebook_view.SearchView.as_view()
        response = search_view(request)
        print(response.data)
        print("*" * 50)
        self.assertEqual(200, response.status_code)
        self.assertIs(len(response.data['result']) > 1, True)
        print("REGISTERD NUMBER")
        url = "{search_url}?phone_number={phone}".format(
            search_url=self.search_url, phone=self.username)
        request = factory.get(
            url, HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
        force_authenticate(
            request, user=User.objects.get(username=self.username))
        search_view = phonebook_view.SearchView.as_view()
        response = search_view(request)
        print(response.data)
        print("*" * 50)
        self.assertEqual(200, response.status_code)
        self.assertIs(len(response.data['result']) == 1, True)

    def test_mark_as_spam(self):
        factory = APIRequestFactory()
        access_token = self.test_registration()
        request = factory.post(
            self.marK_spam_url, {"phone_number": self.spam_number}, format='json', HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
        force_authenticate(
            request, user=User.objects.get(username=self.username))
        mark_spam_view = phonebook_view.MarkSpamView.as_view()
        response = mark_spam_view(request)
        print(response.data)
        print("*" * 50)
        self.assertEqual(200, response.status_code)
