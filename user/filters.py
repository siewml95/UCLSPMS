import django_filters
from project.models import Project
from .models import Interest
from django.db.models import Q,Count

class UserProfileProjectFilter(django_filters.FilterSet):
    class  Meta:
        model = Project
        fields = ['title']
        order_by = ['-timestamp']
    title = django_filters.CharFilter(method="title_contains")

    def title_contains(self,queryset,name,value):
        return queryset.filter(title__icontains=value)

class UserProfileStaffInterestFilter(django_filters.FilterSet):
    class  Meta:
        model = Interest
        fields = ['project']
        order_by = ['-timestamp']
    project = django_filters.CharFilter(method="project_contains")

    def project_contains(self,queryset,name,value):
        return queryset.filter(Q(project__title__icontains=value) | Q(user__email__icontains=value))


class UserProfileInterestFilter(django_filters.FilterSet):
    class  Meta:
        model = Interest
        fields = ['project']
        order_by = ['-timestamp']
    project = django_filters.CharFilter(method="project_contains")

    def project_contains(self,queryset,name,value):
        return queryset.filter(project__title__icontains=value)
