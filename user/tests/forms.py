from django.test import TestCase
from cuser.models import CUser as User
from ..forms import CustomUserStaffCreationForm,CustomUserCreationForm,BugForm
import unittest

@unittest.skip("function")
def func_test_required(self,data,form,label):
    del data[label]
    form = form(data)
    self.assertEquals(form.is_valid(),False)

class CustomUserStaffCreationFormTest(TestCase):
      @classmethod
      def setUpTestData(cls):
          user = User.objects.create_user(email="12345")
          user.save()

      def test_requireds(self):
          data = {"email":"trying@gmail.com","first_name":"First","last_name":"Last","password1":"1","password2":"1"}
          requireds = ["email","password1","password2"]
          print("test_requireds")

          for x in requireds:
              func_test_required(self,data,CustomUserStaffCreationForm,x)

class CustomUserCreationFormTest(TestCase):
      @classmethod
      def setUpTestData(cls):
          user = User.objects.create_user(email="12345")
          user.save()

      def test_requireds(self):
          print("test_requireds")
          data = {"email":"trying@gmail.com","first_name":"First","last_name":"Last","password1":"1","password2":"1"}
          requireds = ["email","password1","password2"]
          for x in requireds:
              func_test_required(self,data,CustomUserCreationForm,x)

class BugFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email="testuser1",password="12345")
        user.save()

    def test_requireds(self):
        login = self.client.login(email='testuser1', password='12345')

        data = {'content':"content"}
        requireds = ["content"]
        print("test_requireds")

        for x in requireds:
            func_test_required(self,data,BugForm,x)
