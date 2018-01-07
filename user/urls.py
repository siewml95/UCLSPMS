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
                    UserProfileAvatarView
                   )
urlpatterns = [
   url(r'^register/$', UserRegisterView.as_view()),
   url(r'^login/$', auth_views.login, {'template_name': 'user/login.html'},name='login'),
   url(r'^logout/$', auth_views.logout, {'next_page': '/project'}, name='logout'),
   url(r'^single/(?P<pk>[-\w]+)/$',UserProjectListView.as_view(),name="single"),
   url(r'^student/(?P<pk>[-\w]+)/$',UserStudentDetailView.as_view(),name="student"),
   url(r'^invitation/(?P<pk>\b[0-9A-Fa-f]{8}\b(-\b[0-9A-Fa-f]{4}\b){3}-\b[0-9A-Fa-f]{12}\b)/$',UserStaffRegisterView.as_view()),

   url(r'^profile/$',UserProfileView.as_view(),name="profile"),

   url(r'^profile/preferences/$',UserProfilePreferenceView.as_view(),name="preferences"),

   url(r'^profile/password-change/$',UserProfilePasswordView.as_view(),name="password-change"),
   url(r'^profile/projects/$',UserProfileProjectView.as_view(),name="projects"),
   url(r'^profile/project-interests/$',UserProfileInterestView.as_view(),name="project-interests"),
   url(r'^profile/interests/$',UserProfileStaffInterestView.as_view(),name="interests"),
   url(r'^profile/avatar/$',UserProfileAvatarView.as_view(),name="avatar"),

   url(r'^ajax/getIndexRecommendations/$',getIndexRecommendations),
   url(r'^ajax/sendInterest/$',sendInterest,name='sendInterest'),
   url(r'^ajax/sendBug/$',sendBug,name='sendBug')

]
