"""djmatch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url,include
from django.contrib import admin
from django.conf.urls.static import static

from django.conf.urls import url
from django.conf import settings

from .views import NewView,sign_s3,IndexView
from project.views import ProjectListView

from django_nose_qunit.views import test_index,run_qunit_tests
urlpatterns = [
    url(r'^$', IndexView.as_view(),name="index"),
    url(r'^admin/', admin.site.urls),
    url(r'^sign_s3/',sign_s3),
    url(r'^project/', include('project.urls',namespace="project")),
    url(r'^user/', include('user.urls',namespace="user")),
    url(r'^uclapi/', include('uclapi.urls',namespace="uclapi")),
    url(r"^select2/fields/auto.json$",
        NewView.as_view(), name="django_select2-json"),
    url(r'^qunit/$', test_index,name= 'django-nose-qunit-list'),
    url(r'^qunit/test/$', run_qunit_tests, name='django-nose-qunit-test')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
