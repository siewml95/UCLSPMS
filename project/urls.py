from django.conf.urls import url
from django.contrib import admin

from .views import (
                    ProjectListView,
                    ProjectCreateView,
                    ProjectUpdateView,
                    ProjectDetailView,
                    ProjectGetKeywords,
                    ProjectFilterView,
                    ProjectGetRequirements,
                    AjaxGetKeywords,
                    AjaxGetDetailRecommendations,
                    CheckKeywordExists
                   )
urlpatterns = [
    url(r'^$', ProjectListView.as_view()),
    url(r'^create/$', ProjectCreateView.as_view(),name="create"),
    url(r'^single/(?P<slug>[-\w]+)/$', ProjectDetailView.as_view(),name="single"),

    url(r'^(?P<pk>[-\w]+)/update/$', ProjectUpdateView.as_view(),name="update"),
    url(r'^list/$',ProjectFilterView.as_view(),name="project_list"),
    url(r'^ajax/$', ProjectGetKeywords),
    url(r'^ajax/getKeywords/$', AjaxGetKeywords),
    url(r'^ajax/getDetailRecommendations/$', AjaxGetDetailRecommendations),

    url(r'^ajax/requirements/$', ProjectGetRequirements),
    url(r'^CheckKeywordExists/$', CheckKeywordExists),

    #url(r'^filter/$', projectFilter),

]
