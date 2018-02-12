from django.contrib.auth.mixins import  UserPassesTestMixin
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.core.mail import send_mail
from .models import  Interest, Profile,Invitation
from project.models import Project,Keyword
from project.forms import ProjectDetailFilterForm
from .forms import AuthenticationForm,PasswordResetForm,SetPasswordForm,UserResendActivationForm,CustomUserCreationForm, UserProfileForm ,UserProfilePasswordForm,InterestForm,UserProfilePreferenceForm, CustomUserStaffCreationForm, BugForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q,Count
import itertools , operator, datetime,random,string
from  functools import reduce
from django.contrib import messages
from cuser.models import CUser as User
class UserPassesTestMixinCustom(UserPassesTestMixin):

    required_url = None
    has_failed = False
    error_message = "Some error occured"
    def get_required_url(self):
        """
        Override this method to override the login_url attribute.
        """
        required_url = self.required_url
        if not required_url:
            raise ImproperlyConfigured(
                '{0} is missing the required_url attribute. Define {0}.required_url, settings.REQUIRED_URL, or override '
                '{0}.get_required_url().'.format(self.__class__.__name__)
            )
        return str(required_url)
    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        if self.request.user.is_authenticated:
          messages.add_message(self.request, messages.ERROR, self.error_message)
          return redirect_to_login(self.request.get_full_path(), self.get_required_url(),"")
        else:
          return redirect_to_login(self.request.get_full_path(),self.get_login_url(),self.get_redirect_field_name())

class VerifiedRequiredMixin(UserPassesTestMixinCustom):
    error_message = "Activate your account first!."

    def test_func(self):
         try:
             print(self.request.user.profile.is_verified)
             return  self.request.user.profile.is_verified
         except:
             return False


class StudentVerifiedRequiredMixin(UserPassesTestMixinCustom):

      def test_func(self):
        try:
          user_type = self.request.user.profile.type
          if (user_type == 1 or user_type == 2 ) and self.request.user.profile.is_verified:
             return True
          elif not self.request.user.profile.is_verified :
             self.error_message = "Activate your account first!."
             return False
          else:
             self.error_message = "Must have a student account to access the page!"
             return False
        except:
         return False

class StaffVerifiedRequiredMixin(UserPassesTestMixinCustom):

      def test_func(self):
            try:
              user_type = self.request.user.profile.type
              print("staff required")
              print(user_type)
              if (user_type == 3 or user_type == 4) and self.request.user.profile.is_verified:
                 return True
              elif not self.request.user.profile.is_verified :
                   self.error_message = "Activate your account first!."
                   return False
              else:
                   self.error_message = "Must have a staff account to access the page!"
                   return False

            except:
             error_message = "Some Er"
             return False


class StudentRequiredMixin(UserPassesTestMixinCustom):
      error_message = "Must have a student account to access the page!"
      def test_func(self):
        try:
          user_type = self.request.user.profile.type
          if user_type == 1 or user_type == 2:
             return True
          else:
             return False
        except:
         return False

class StaffRequiredMixin(UserPassesTestMixinCustom):
      error_message = "Must have a staff account to access the page!"

      def test_func(self):
            try:
              user_type = self.request.user.profile.type
              print("staff required")
              print(user_type)
              if user_type == 3 or user_type == 4:
                 return True
              else:
                 return False
            except:
             return False
