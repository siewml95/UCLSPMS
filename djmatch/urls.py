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

from django.conf.urls import url

from .views import NewView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^project/', include('project.urls',namespace="project")),
    url(r'^user/', include('user.urls',namespace="user")),
    url(r'^uclapi/', include('uclapi.urls',namespace="uclapi")),

    url(r"^select2/fields/auto.json$",
        NewView.as_view(), name="django_select2-json"),

]
