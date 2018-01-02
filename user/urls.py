from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views


from .views import (
                    UserRegisterView,
                    UserProfileView,
                    UserProfileProjectView,
                    UserProfilePasswordView,
                    UserProjectListView,
                    getIndexRecommendations,
                    sendInterest,
                    sendBug,
                    UserProfilePreferenceView,
                    UserProfileInterestView,
                    UserProfileStaffInterestView,
                    UserStaffRegisterView,
                    UserStudentDetailView,
                   )
urlpatterns = [
   url(r'^register/$', UserRegisterView.as_view()),
   url(r'^login/$', auth_views.login, {'template_name': 'user/login.html'},name='login'),
   url(r'^logout/$', auth_views.logout, {'next_page': '/project'}, name='logout'),
   url(r'^single/(?P<pk>[-\w]+)/$',UserProjectListView.as_view()),
   url(r'^student/(?P<pk>[-\w]+)/$',UserStudentDetailView.as_view()),
   url(r'^invitation/(?P<pk>\b[0-9A-Fa-f]{8}\b(-\b[0-9A-Fa-f]{4}\b){3}-\b[0-9A-Fa-f]{12}\b)/$',UserStaffRegisterView.as_view()),

   url(r'^profile/$',UserProfileView.as_view()),

   url(r'^profile/preferences/$',UserProfilePreferenceView.as_view()),

   url(r'^profile/password-change/$',UserProfilePasswordView.as_view()),
   url(r'^profile/projects/$',UserProfileProjectView.as_view()),
   url(r'^profile/project-interests/$',UserProfileInterestView.as_view()),
   url(r'^profile/interests/$',UserProfileStaffInterestView.as_view()),

   url(r'^ajax/getIndexRecommendations/$',getIndexRecommendations),
   url(r'^ajax/sendInterest/$',sendInterest,name='sendInterest'),
   url(r'^ajax/sendBug/$',sendBug,name='sendBug')

]
