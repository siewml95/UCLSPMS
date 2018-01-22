from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,FormView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.core.mail import send_mail

from .models import  Interest, Profile,Invitation
from project.models import Project,Keyword
from project.forms import ProjectDetailFilterForm
from .forms import AuthenticationForm,PasswordResetForm,SetPasswordForm,UserResendActivationForm,CustomUserCreationForm, UserProfileForm ,UserProfilePasswordForm,InterestForm,UserProfilePreferenceForm, CustomUserStaffCreationForm, BugForm
from django.contrib.auth import login, authenticate,get_user,update_session_auth_hash
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q,Count
import itertools , operator, datetime,random,string
from  functools import reduce
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from cuser.models import CUser as User

def sendInterest(request):
    if request.user.is_authenticated and request.GET["id"]:
       if request.user.profile.is_verified == False:
           response = JsonResponse({"error" : "Must have a verified account!"})
           response.status_code = 403
           return response
       if request.user.profile.type == 3:
           response = JsonResponse({"error" : "Must hava a student account!"})
           response.status_code = 403
           return response
       try:
         project = Project.objects.get(pk=request.GET["id"])
         if project.created_by != request.user:
            flag = Interest.objects.get(user=request.user,project=project)
         else:
          response = JsonResponse({"error" : "Cannot be interest in your own project"})
          response.status_code = 403
          return response

       except Interest.DoesNotExist:
                 Interest.objects.create(user=request.user,project=project,description=request.GET["description"])
                 try :
                   send_notification(request)
                 except:
                    response = JsonResponse({"error" : "Error in sending mail!"})
                    response.status_code = 403
                    return response
                 count = Interest.objects.filter(project=request.GET["id"]).count()
                 return JsonResponse({"interest": [],"amount":count})
       except Project.DoesNotExist:
          response = JsonResponse({"error" : "The project do not exists"})
          response.status_code = 403
          return response
       response = JsonResponse({"error" : "You already done it"})
       response.status_code = 403
       return response
    else :
       response = JsonResponse({"error" : "Must be log in"})
       response.status_code = 403
       return response

def send_notification(request):
    if request.user.is_authenticated and (request.user.profile.type == 2 or request.user.profile.type == 1) :
        user = request.user
        project_id = request.GET["id"]
        project = Project.objects.all().get(pk=project_id)
        if project_id:
            subject = "You have received a notificaion from {}.".format("Notice Project")
            message = "Dear Sir/Madam\n I am writing this email to inform you that I am interested in this project\n\n Project Name : {} \n Email: {}\n".format(project.title,project.created_by.email)
            from_email = 'contact.dataspartan@gmail.com'
            to_email = [project.created_by.email]
            send_mail(subject,message,from_email,to_email,fail_silently=False)
        else:
            return None
    else:
        return None

def sendBug(request):
    if request.user.is_authenticated:
        user = request.user
        email = user.email
        content = request.GET["content"]
        if email:
            subject = "Contact : {}.".format(email)
            message = "Dear Sir/Madam\nemail: {}\ncontent : \n{}\n".format(email,content)
            from_email = 'contact.dataspartan@gmail.com'
            to_email = ['contact.dataspartan@gmail.com']
            send_mail(subject,message,from_email,to_email,fail_silently=False)
            return JsonResponse({})
        else:
              response = JsonResponse({"error" : "Some Error Occured"})
              response.status_code = 403
              return response
    else:
        content = request.GET["content"]
        email = request.GET["email"]
        if email:
            subject = "Contact : {}.".format(email)
            message = "Dear Sir/Madam\n Email: {}\n content : \n {}\n".format(email,content)
            from_email = 'contact.dataspartan@gmail.com'
            to_email = [user.email]
            send_mail(subject,message,from_email,to_email,fail_silently=False)
            return JsonResponse({})
        else:
            response = JsonResponse({"error" : "Some Error Occured"})
            response.status_code = 403
            return response
def getIndexRecommendations(request):
    if request.user.is_authenticated:
      interests = Interest.objects.filter(user=request.user)
      preferences = request.user.profile.preferences.all()
      q_expressions = [[keyword.id for keyword in interest.project.keywords.all()] for interest  in interests]
      q_list =  set(itertools.chain.from_iterable(q_expressions))
      p_list = set([x.id for x in preferences])
      q_list_exclude = [x for x in q_list if x not in p_list]
      q_expressions = [Q(keywords=keyword) for keyword in q_list_exclude]
      p_expressions = [Q(keywords=keyword) for keyword in p_list]
      current_project_id = request.GET["id"]
      if current_project_id == 0 or current_project_id == "0":
        interested = [interest.project.id for interest in interests]
      else:
        interested = [interest.project.id for interest in interests]
        interested.append(current_project_id)
      if p_expressions != []:
       p = Project.objects.filter(reduce(operator.or_,p_expressions)).exclude(created_by=request.user).exclude(id__in=interested)
      else:
       p = []
      if q_expressions != []:
        q = Project.objects.filter(reduce(operator.or_,q_expressions)).exclude(created_by=request.user).exclude(id__in=interested)
      else:
        q = []
      if p != []:
        t = p.values("pk","slug","title").annotate(keyword_count=Count("keywords")).order_by('-keyword_count')[0:10]
      else:
        t = []
      if  q != []:
       k = q.values("pk","slug","title").annotate(keyword_count=Count("keywords")).order_by('-keyword_count')[0:10]
      else:
       k = []
      factor = 2
      final = []
      m = list(k)
      length = len(k) - 1
      if len(t) != 0 and len(k) == 0:
          for item in t:
              item['keyword_count'] *= factor
          k = t
      else:
          for index_t,item_t in enumerate(t):
             for index_k,item_k in enumerate(k):
                 if index_k == length:
                             final.append(item_t)
                             break
                 elif item_t['pk'] == item_k['pk']:
                             m[index_k]["keyword_count"] += item_t['keyword_count'] * factor
                             break
          k = (m + final)
      k = sorted(k,key=lambda x: x["keyword_count"],reverse=True)[0:10]
      return JsonResponse({"recommendations": list(k)})
    else :
      return JsonResponse({"recommendations": []})

def sendActivationEmail(activation_key,email_target):
        subject = "You have received a notificaion from {}.".format("Notice Project")
        message = "Dear Sir/Madam\n Please click on the link below \n localhost:8000/user/activation/{}".format(activation_key)
        from_email = 'contact.dataspartan@gmail.com'
        to_email = [email_target]
        send_mail(subject,message,from_email,to_email,fail_silently=False)


class UserResendActivationView(LoginRequiredMixin,FormView):
    template_name = "user/profile/tab.html"
    form_class = UserResendActivationForm
    success_url = "."

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
             sendActivationEmail(activation_key,email_target)
             return HttpResponseRedirect(".")
        else:
             messages.add_message(self.request, messages.ERROR, 'Account Already Verified!')
             return HttpResponseRedirect(".")

    def get_context_data(self,**kwargs):
        context = super(UserResendActivationView, self).get_context_data(**kwargs)
        context["page_name"] = 'resend'
        return context


class UserActivationView(TemplateView):
    template_name = "user/activation.html"

    def get_context_data(self,**kwargs):
        context = super(UserActivationView, self).get_context_data(**kwargs)
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


class UserStaffRegisterView(CreateView):
    template_name = "user/register.html"
    form_class = CustomUserStaffCreationForm
    model = User
    success_url="/user/profile"

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
        uuid = self.kwargs['pk']
        invitation = get_object_or_404(Invitation,id=uuid)
        currenttime = datetime.datetime.now(datetime.timezone.utc)
        diff =  currenttime - invitation.timestamp
        print(diff)
        if invitation.status == 1 and diff.seconds <= 3600:
            return context
        else:
            return HttpResponseRedirect('/project')




class UserRegisterView(CreateView):
    template_name="user/register.html"
    form_class = CustomUserCreationForm
    model = User
    success_url="/user/register"

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
        sendActivationEmail(obj.profile.activation_key,obj.email)
        messages.add_message(self.request, messages.SUCCESS, 'Account Created!. Please verify email')
        return HttpResponseRedirect("/user/profile")

    def get_context_data(self, **kwargs):
          context = super(UserRegisterView, self).get_context_data(**kwargs)
          print("reload")
          return context

class UserProfileView(LoginRequiredMixin,UpdateView):
    template_name="user/profile/tab.html"
    model = Profile
    form_class = UserProfileForm
    success_url = "/project/"
    login_url = "/user/login/"

    def get_object(self):
      return self.request.user.profile
    def get_context_data(self, *args,**kwargs):
          context = super(UserProfileView, self).get_context_data(**kwargs)
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


    def get_context_data(self,**kwargs):
          context = super(UserProfilePasswordView, self).get_context_data(**kwargs)
          context["page_name"] = 'password'
          return context
    def get_object(self):
      return self.request.user

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

    def get_context_data(self, **kwargs):
          context = super(UserProfilePreferenceView, self).get_context_data(**kwargs)
          context["page_name"] = "preference"
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
               print("creating")
               keyword = Keyword.objects.create(title=item,type=2)
               keyword.save()
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
class UserProfileProjectView(LoginRequiredMixin,StaffRequiredMixin,ListView):
    template_name="user/profile/tab.html"
    model = Project
    login_url = '/user/login/'
    required_url = '/user/profile/'
    paginate_by = '10'

    def get_queryset(self,**kwargs):
        qs = super(UserProfileProjectView, self).get_queryset()
        qs = qs.filter(created_by=self.request.user).order_by("-timestamp")
        return qs
    def get_context_data(self, **kwargs):
          context = super(UserProfileProjectView, self).get_context_data(**kwargs)
          context["page_name"] = "project"
          return context

class UserProfileInterestView(LoginRequiredMixin,StudentRequiredMixin,ListView):
    template_name="user/profile/tab.html"
    model = Interest
    login_url = '/user/login/'
    required_url = '/user/profile/'

    paginate_by = '10'

    def get_queryset(self,**kwargs):
        qs = super(UserProfileInterestView,self).get_queryset()
        qs = qs.filter(user=self.request.user).order_by("-timestamp")
        return qs

    def get_context_data(self, **kwargs):
          context = super(UserProfileInterestView, self).get_context_data(**kwargs)
          context["page_name"] = "interest"
          return context


class UserProfileStaffInterestView(LoginRequiredMixin,StaffRequiredMixin,ListView):
    template_name="user/profile/tab.html"
    model = Interest
    login_url = '/user/login/'
    required_url = '/user/profile/'

    paginate_by = '10'

    def get_queryset(self,**kwargs):
        qs = super(UserProfileStaffInterestView,self).get_queryset()
        qs = qs.filter(project__created_by=self.request.user)
        return qs
    def get_context_data(self, **kwargs):
          context = super(UserProfileStaffInterestView, self).get_context_data(**kwargs)
          context["page_name"] = "staff_interest"
          return context

class UserProjectListView(ListView):
    template_name = "user/project-list.html"
    model = Project
    paginate_by = '10'

    def get_queryset(self,**kwargs):
        projects = Project.objects.filter(created_by=self.kwargs['pk']).order_by("-timestamp")
        return projects

    def get_context_data(self, **kwargs):
            context = super(UserProjectListView, self).get_context_data(**kwargs)
            user = get_object_or_404(User,pk=self.kwargs['pk'])
            context["first_name"] = user.first_name
            context["last_name"] = user.last_name
            context["filterForm"] = ProjectDetailFilterForm
            return context

class UserStudentDetailView(LoginRequiredMixin,StaffRequiredMixin,DetailView):
    template_name="user/student/detail.html"
    model = User
    login_url = "/user/login"
    required_url = '/user/profile/'
