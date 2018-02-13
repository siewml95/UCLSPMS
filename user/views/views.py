from .mixins import *
from .utils import sendActivationEmail
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,FormView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.core.mail import send_mail
from ..models import  Interest, Profile,Invitation
from project.models import Project,Keyword
from project.forms import ProjectDetailFilterForm
from ..forms import AuthenticationForm,PasswordResetForm,SetPasswordForm,UserResendActivationForm,CustomUserCreationForm, UserProfileForm ,UserProfilePasswordForm,InterestForm,UserProfilePreferenceForm, CustomUserStaffCreationForm, BugForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q,Count
import itertools , operator, datetime,random,string
from  functools import reduce
from django.contrib import messages
from cuser.models import CUser as User
from django.contrib.auth import login, authenticate,get_user,update_session_auth_hash

class UserResendActivationView(LoginRequiredMixin,FormView):
    template_name = "user/profile/tab.html"
    form_class = UserResendActivationForm
    success_url = "."
    title = "Resend Activation Link"

    def form_valid(self,form):
        profile = self.request.user.profile
        email_target = self.request.user.email
        key_expires = profile.key_expires
        if profile.is_verified == False:
             activation_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))
             profile.activation_key = activation_key
             profile.key_expires = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
             profile.save()
             messages.add_message(self.request, messages.SUCCESS, 'Resend Activation Email')
             activation_key = self.request.get_host() + "/user/activation/" + activation_key
             sendActivationEmail(activation_key,email_target)
             return HttpResponseRedirect(".")
        else:
             messages.add_message(self.request, messages.ERROR, 'Account Already Verified!')
             return HttpResponseRedirect(".")

    def get_context_data(self,**kwargs):
        context = super(UserResendActivationView, self).get_context_data(**kwargs)
        context["page_name"] = 'resend'
        context["title"] = self.title
        return context


class UserActivationView(TemplateView):
    template_name = "user/activation.html"
    title = "Activating Account"
    def get_context_data(self,**kwargs):
        context = super(UserActivationView, self).get_context_data(**kwargs)
        context["title"] = self.title
        activation_key = self.kwargs['key']
        activation_expired = False
        already_active = False
        profile = get_object_or_404(Profile,activation_key=activation_key)
        if profile.is_verified == False:
           if datetime.datetime.now(datetime.timezone.utc) <= profile.key_expires:
              profile.is_verified = True
              profile.save()
              messages.add_message(self.request, messages.SUCCESS, 'Account Verified!.')
              print("success")
              context["success"] = True
              return context
           else:
              context["success"] = False
              return context
        else :
          print("already activated")
          context["success"] = False
          return context


class UserRegisterView(CreateView):
    template_name="user/register.html"
    form_class = CustomUserCreationForm
    model = User
    success_url="/user/register"
    title = "Register Student Account"

    def form_valid(self,form):
        print("form-valid")
        print(self.request.POST)

        obj = form.save(commit=True)
        raw_password = form.cleaned_data.get('password1')
        print(User.objects.all().filter(email=obj.email))
        user = authenticate(self.request,email=obj.email, password=raw_password)
        print(user.__dict__)
        login(self.request, user)
        print(self.request.user.is_authenticated())
        activation_key = self.request.get_host() + "/user/activation/" + obj.profile.activation_key
        sendActivationEmail(activation_key,obj.email)
        messages.add_message(self.request, messages.SUCCESS, 'Account Created!. Please verify email')
        return HttpResponseRedirect("/user/profile")

    def get_context_data(self, **kwargs):
          context = super(UserRegisterView, self).get_context_data(**kwargs)
          context["title"] = self.title
          return context

class UserProfileView(LoginRequiredMixin,UpdateView):
    template_name="user/profile/tab.html"
    model = Profile
    form_class = UserProfileForm
    success_url = "/project/"
    login_url = "/user/login/"
    title = "Profile"
    def get_object(self):
      return self.request.user.profile
    def get_context_data(self, *args,**kwargs):
          context = super(UserProfileView, self).get_context_data(**kwargs)
          context["title"] = self.title
          print(self.request.user.profile.__dict__)
          print(context)
          context["page_name"] = 'profile'
          return context

    def form_valid(self,form):
        print("form_valid")
        obj = super(UserProfileView,self).form_valid(form)
        print(form.__dict__)
        messages.add_message(self.request, messages.SUCCESS, 'Profile Saved!.')
        return HttpResponseRedirect("/user/profile/")


class UserProfilePasswordView(LoginRequiredMixin,UpdateView):
    template_name="user/profile/tab.html"
    model = User
    form_class = UserProfilePasswordForm
    login_url = "/user/login/"
    title = "Password Change"

    def get_context_data(self,**kwargs):
          context = super(UserProfilePasswordView, self).get_context_data(**kwargs)
          context["page_name"] = 'password'
          context["title"] = self.title
          return context
    def get_object(self):
      return self.request.user

    def form_invalid(self,form):
        print("invalid")
        print(self.__dict__)
        print(form.__dict__)
    def form_valid(self,form):
     print("form_valid")
     try:
       obj = form.save(commit=True)
       update_session_auth_hash(self.request, self.request.user)
       messages.add_message(self.request, messages.SUCCESS, 'Password Saved!.')

       return HttpResponseRedirect(".")
     except:
       messages.add_message(self.request, messages.ERROR, 'Error Occured!.')
       return HttpResponseRedirect(".")


    def get_form_kwargs(self):
        kw = super(UserProfilePasswordView, self).get_form_kwargs()
        kw['user'] = self.request.user # the trick!
        return kw
class UserProfilePreferenceView(LoginRequiredMixin,StudentRequiredMixin,UpdateView):
    template_name="user/profile/tab.html"
    model = Profile
    login_url = '/user/login/'
    required_url = '/user/profile/'
    form_class = UserProfilePreferenceForm
    title = "Preferences"
    def get_context_data(self, **kwargs):
          context = super(UserProfilePreferenceView, self).get_context_data(**kwargs)
          context["page_name"] = "preference"
          context["title"] = self.title
          return context
    def get_object(self):
        return get_user(self.request).profile

    def form_valid(self,form):
     print("good")
     if self.request.user.is_authenticated():
         user = get_user(self.request)
         print('berfore')
         preferences = self.request.POST.getlist("preferences")
         array = []
         #requirements = self.request.POST["keywords_1"]
         for item in preferences:
             print(item)
             if item.isdigit():
               array.append(item)
             else :
               try:
                 keyword = Keyword.objects.get(title=item)
               except Keyword.DoesNotExist:
                 keyword = Keyword.objects.create(title=item,type=2,status=True)
                 array.append(keyword.pk)
               array.append(keyword.pk)
         if isinstance(array, list):
             user.profile.preferences.clear()
             print(array)
             user.profile.preferences.add(*array)
             print(user.profile.preferences)

             user.profile.save()
             print(user.profile.preferences)
             messages.add_message(self.request, messages.SUCCESS, 'Preference Saved!.')

         return HttpResponseRedirect("/user/profile/preferences/")
     else:
         return HttpResponseRedirect("/user/profile/preferences/")


class UserProfileInterestView(LoginRequiredMixin,StudentRequiredMixin,ListView):
    template_name="user/profile/tab.html"
    model = Interest
    login_url = '/user/login/'
    required_url = '/user/profile/'
    title = "Profile - Interests"
    paginate_by = '10'

    def get_queryset(self,**kwargs):
        qs = super(UserProfileInterestView,self).get_queryset()
        qs = qs.filter(user=self.request.user).order_by("-timestamp")
        return qs

    def get_context_data(self, **kwargs):
          context = super(UserProfileInterestView, self).get_context_data(**kwargs)
          context["page_name"] = "interest"
          context["title"] = self.title
          return context



class UserProjectListView(ListView):
    template_name = "user/project-list.html"
    model = Project
    paginate_by = '10'
    title = "Profile - Projects"
    def get_queryset(self,**kwargs):
        projects = Project.objects.filter(created_by=self.kwargs['pk']).order_by("-timestamp")
        return projects

    def get_context_data(self, **kwargs):
            context = super(UserProjectListView, self).get_context_data(**kwargs)
            user = get_object_or_404(User,pk=self.kwargs['pk'])
            context["first_name"] = user.first_name
            context["last_name"] = user.last_name
            context["filterForm"] = ProjectDetailFilterForm
            context["title"] = self.title
            return context
