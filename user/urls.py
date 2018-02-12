from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from cuser.forms import AuthenticationForm

from .forms import PasswordResetForm,SetPasswordForm,AuthenticationForm
from .views import (
                    UserRegisterView,
                    UserProfileView,
                    UserProfileProjectView,
                    UserProfilePasswordView,
                    UserProjectListView,
                    getIndexRecommendations,
                    sendInterest,
                    sendBug,
                    UserActivationView,
                    UserProfilePreferenceView,
                    UserProfileInterestView,
                    UserProfileStaffInterestView,
                    UserStaffRegisterView,
                    UserStudentDetailView,
                    UserResendActivationView,
                   )

class CustomLoginView(auth_views.LoginView):
     def form_valid(self, form):
        """Security check complete. Log the user in."""
        print("CustomLoginView xxxxxxxxxxxxxxxxxxxxxxxx form_valid")
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())
     def form_invalid(self,form):
        print("CustomLoginView xxxxxxxxxxxxxxxxxxxxxxxx form_invalid")
        return super(CustomLoginView, self).form_invalid(form)
urlpatterns = [
   url(r'^register/$', UserRegisterView.as_view()),
   url(r'^login/$', CustomLoginView.as_view(authentication_form=AuthenticationForm, template_name='user/login.html'),name='login'),
   url(r'^logout/$', auth_views.logout, {'next_page': '/project'}, name='logout'),
   url(r'^password_reset/$',auth_views.PasswordResetView.as_view(form_class=PasswordResetForm,success_url = "/user/password_reset/done/"), name='password_reset'),
   url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
   url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
   url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(form_class = SetPasswordForm,success_url = "/user/reset/done/"), name='password_reset_confirm'),
   url(r'^single/(?P<pk>[-\w]+)/$',UserProjectListView.as_view(),name="single"),
   url(r'^student/(?P<pk>[-\w]+)/$',UserStudentDetailView.as_view(),name="student"),
   url(r'^invitation/(?P<pk>\b[0-9A-Fa-f]{8}\b(-\b[0-9A-Fa-f]{4}\b){3}-\b[0-9A-Fa-f]{12}\b)/$',UserStaffRegisterView.as_view()),
   url(r'^activation/(?P<key>[-\w]+)/$',UserActivationView.as_view()),
   url(r'^resend-activation/$',UserResendActivationView.as_view(),name="resend-activation"),
   url(r'^profile/$',UserProfileView.as_view(),name="profile"),

   url(r'^profile/preferences/$',UserProfilePreferenceView.as_view(),name="preferences"),

   url(r'^profile/password-change/$',UserProfilePasswordView.as_view(),name="password-change"),
   url(r'^profile/projects/$',UserProfileProjectView.as_view(),name="projects"),
   url(r'^profile/project-interests/$',UserProfileInterestView.as_view(),name="project-interests"),
   url(r'^profile/interests/$',UserProfileStaffInterestView.as_view(),name="interests"),

   url(r'^ajax/getIndexRecommendations/$',getIndexRecommendations),
   url(r'^ajax/sendInterest/$',sendInterest,name='sendInterest'),
   url(r'^ajax/sendBug/$',sendBug,name='sendBug')

]
