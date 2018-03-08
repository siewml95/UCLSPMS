from .mixins import *
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,FormView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from ..models import  Interest, Profile,Invitation
from project.models import Project,Keyword
from project.forms import ProjectDetailFilterForm
from ..forms import AuthenticationForm,PasswordResetForm,SetPasswordForm,UserResendActivationForm,CustomUserCreationForm, UserProfileForm ,UserProfilePasswordForm,InterestForm,UserProfilePreferenceForm, CustomUserStaffCreationForm, BugForm,UserProfileProjectForm,UserProfileStaffInterestForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q,Count
import itertools , operator, datetime,random,string
from  functools import reduce
from django.contrib import messages
from cuser.models import CUser as User
from django.contrib.auth import login, authenticate,get_user,update_session_auth_hash
from django.contrib import messages
from ..tables import UserProfileProjectTable,UserProfileStaffInterestTable
from ..filters import UserProfileProjectFilter,UserProfileStaffInterestFilter




class UserStaffRegisterView(CreateView):
    template_name = "user/register.html"
    form_class = CustomUserStaffCreationForm
    model = User
    success_url="/user/profile"
    title = "Register Staff Account"
    def form_valid(self,form):
        obj = form.save(commit=True)
        uuid = self.kwargs['pk']
        invitation = get_object_or_404(Invitation,id=uuid)
        invitation.status = 3
        invitation.save()
        raw_password = form.cleaned_data.get('password1')
        print(User.objects.all().filter(email=obj.email))
        user = authenticate(self.request,email=obj.email, password=raw_password)
        print(user.__dict__)
        login(self.request, user)
        print(self.request.user.is_authenticated())
        messages.add_message(self.request, messages.SUCCESS, 'Account Created!.')

        return HttpResponseRedirect("/user/profile")
    def get_context_data(self,**kwargs):
        context = super(UserStaffRegisterView, self).get_context_data(**kwargs)
        context["title"] = self.title
        uuid = self.kwargs['pk']
        invitation = get_object_or_404(Invitation,id=uuid)
        currenttime = datetime.datetime.now(datetime.timezone.utc)
        diff =  currenttime - invitation.timestamp
        print(diff)
        if invitation.status == 1 and diff.seconds <= 3600:
            return context
        else:
            return HttpResponseRedirect('/project')

class UserProfileProjectView(LoginRequiredMixin,StaffRequiredMixin,PagedFilteredTableView):
    template_name="user/profile/tab.html"
    model = Project
    table_class = UserProfileProjectTable
    ordering = ['-timestamp']
    filter_class = UserProfileProjectFilter
    formhelper_class = UserProfileProjectForm
    login_url = '/user/login/'
    required_url = '/user/profile/'
    paginate_by = '10'
    title = "Profile - Projects"

    def get_queryset(self,**kwargs):
        qs = super(UserProfileProjectView, self).get_queryset()
        qs = qs.filter(created_by=self.request.user).order_by("-timestamp")
        return qs

    def get_context_data(self, **kwargs):
          context = super(UserProfileProjectView, self).get_context_data(**kwargs)
          search_query = self.get_queryset()
          table = self.table_class(search_query)
          RequestConfig(self.request,paginate={'per_page': self.paginate_by}).configure(table)
          context['table'] = table
          context["page_name"] = "project"
          context["title"] = self.title
          context["today"] = datetime.date.today()
          return context

class UserProfileStaffInterestView(LoginRequiredMixin,StaffRequiredMixin,PagedFilteredTableView):
    template_name="user/profile/tab.html"
    model = Interest
    table_class = UserProfileStaffInterestTable
    ordering = ['-timestamp']
    filter_class = UserProfileStaffInterestFilter
    formhelper_class = UserProfileStaffInterestForm
    login_url = '/user/login/'
    required_url = '/user/profile/'
    title = "Profile - Interests By Students"
    paginate_by = '10'

    def get_queryset(self,**kwargs):
        qs = super(UserProfileStaffInterestView,self).get_queryset(**kwargs)
        qs = qs.filter(project__created_by=self.request.user)
        return qs
    def get_context_data(self, **kwargs):
          context = super(UserProfileStaffInterestView, self).get_context_data(**kwargs)
          search_query = self.get_queryset()
          table = self.table_class(search_query)
          RequestConfig(self.request,paginate={'per_page': self.paginate_by}).configure(table)
          context['table'] = table
          context["page_name"] = "staff_interest"
          context["title"] = self.title
          return context


class UserStudentDetailView(LoginRequiredMixin,StaffRequiredMixin,DetailView):
    template_name="user/student/detail.html"
    model = User
    login_url = "/user/login"
    required_url = '/user/profile/'
