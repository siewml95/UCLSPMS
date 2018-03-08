from django.contrib.auth.mixins import  UserPassesTestMixin
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from django_tables2 import SingleTableView
from django_tables2.config import RequestConfig

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
              print(user_type)
              if user_type == 3 or user_type == 4:
                 return True
              else:
                 return False
            except:
             return False

class StaffNotRequiredMixin(UserPassesTestMixinCustom):
      error_message = "You Already Have a Staff Account!"

      def test_func(self):
            try:
              if self.request.user.is_authenticated :
                    user_type = self.request.user.profile.type
                    if user_type == 3:
                      return False
                    else:
                      return True
              else:
                 return True
            except:
             return False

class StudentNotRequiredMixin(UserPassesTestMixin):
      def test_func(self):
            try:
              if self.request.user.is_authenticated :
                    user_type = self.request.user.profile.type
                    if user_type == 1 or user_type == 2:
                      return False
                    else:
                      return True
              else:
                 return True
            except:
             return False


class PagedFilteredTableView(SingleTableView):
   filter_class = None
   formhelper_class = None
   context_filter_name = 'filter'

   def get_queryset(self,**kwargs):
       qs = super(PagedFilteredTableView,self).get_queryset(**kwargs)
       self.filter = self.filter_class(self.request.GET,queryset=qs)
       self.filter.form.helper = self.formhelper_class()
       return self.filter.qs

   def get_context_data(self,**kwargs):
       context = super(PagedFilteredTableView,self).get_context_data(**kwargs)
       context[self.context_filter_name] = self.filter
       return context
