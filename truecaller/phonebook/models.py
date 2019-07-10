from django.db import models
from django.contrib.auth.models import User
from helpers.mixins import SafeDeleteMixinExtended,BaseMixin


class PhoneBook(SafeDeleteMixinExtended, BaseMixin):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=30, unique=True)


class PhoneNumberOwnerName(SafeDeleteMixinExtended, BaseMixin):
    phone_number = models.ForeignKey(PhoneBook, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    @property
    def get_profile(self):
        profile_dict = {
            "id":"",
            "name" : "",
            "email" : "",
            "phone_number" : "",
            "is_spam" : ""
        }
        profile_dict["id"] = self.id
        profile_dict["name"] = self.name
        if self.phone_number.user:
            profile_dict["email"] = self.phone_number.user.email
        else:
            profile_dict["email"] = ""
        profile_dict["phone_number"] = self.phone_number.phone_number
        try:
            self.phone_number.spammarker
            profile_dict["is_spam"] =  True
        except Exception as e:
            profile_dict["is_spam"] =  False
        return profile_dict


class SpamMarker(SafeDeleteMixinExtended, BaseMixin):
    marked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    spammer = models.OneToOneField(PhoneBook, on_delete=models.CASCADE)
