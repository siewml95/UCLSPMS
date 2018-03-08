# Create your tests here.
from django.test import TestCase
from ..models import Profile,Invitation,Interest
from project.models import Keyword,Project
from cuser.models import CUser as User
import unittest

@unittest.skip("function")
def test_label(self,model,label,verbose_label):
     obj = model.objects.all()[0]
     field_label = obj._meta.get_field(label).verbose_name
     self.assertEquals(field_label,verbose_label)


class InvitationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        invitation = Invitation.objects.create(email="contact.dataspartan@gmail.com",status=1)
        invitation.save()


    def test_labels(self):
        labels = [{"label":"email","verbose_label":"email"},{"label":"timestamp","verbose_label":"timestamp"},{"label":"status","verbose_label":"status"}]
        for x in labels:
            test_label(self,Invitation,x["label"],x["verbose_label"])


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(email="12345")
        user.save()

    def test_labels(self):
        labels = [{"label":"type","verbose_label":"type"},{"label":"birth_date","verbose_label":"birth date"},
                     {"label":"preferences","verbose_label":"preferences"},{"label":"avatar","verbose_label":"avatar"},{"label":"linkedin","verbose_label":"linkedin"}]
        for x in labels:
            print(x)
            test_label(self,Profile,x["label"],x["verbose_label"])
