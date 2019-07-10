import re
from rest_framework import serializers
from django.contrib.auth.models import User
from .constants import PHONE_NUMBER_REGEX, PASSWORD_REGEX
from phonebook.models import PhoneBook, PhoneNumberOwnerName, SpamMarker
from rest_framework import serializers, exceptions


class CreateUserSerializer(serializers.Serializer):
    phone_number = serializers.RegexField(re.compile(
        PHONE_NUMBER_REGEX), max_length=20, min_length=6, allow_blank=False, required=True)
    name = serializers.CharField(max_length=30)
    email = serializers.EmailField(max_length=30, required=False, allow_blank=False)
    password = serializers.RegexField(re.compile(
        PASSWORD_REGEX), max_length=20, min_length=6, allow_blank=False)

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                validated_data['phone_number'], validated_data['email'], validated_data['password'])
        except Exception as e:
            raise exceptions.ValidationError("Unable to register user")

        phone_book = None
        try:
            phone_book = PhoneBook.objects.get(
                phone_number=validated_data['phone_number'])
        except PhoneBook.DoesNotExist:
            phone_book = PhoneBook(
                phone_number=validated_data['phone_number'], user=user)
            phone_book.save()

        phone_book_owner_name = PhoneNumberOwnerName(
            phone_number=phone_book, name=validated_data['name'])
        phone_book_owner_name.save()
        return user



class LoginUserSerializer(serializers.Serializer):
    username = serializers.RegexField(re.compile(
        PHONE_NUMBER_REGEX), max_length=20, min_length=6, allow_blank=False)
    password = serializers.RegexField(re.compile(
        PASSWORD_REGEX), max_length=20, min_length=6, allow_blank=False)
