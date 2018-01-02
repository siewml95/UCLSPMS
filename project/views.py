from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import ProjectFilter
from .forms import ProjectModelForm, ProjectFilterForm
from .models import Project,Keyword
from user.models import Interest
from user.forms import InterestForm
from rake_nltk import Rake
# Create your views here.
from django.shortcuts import get_object_or_404
from django.db.models import Q,Count
from  functools import reduce
import operator,numbers
from django.contrib import messages
from user.views import StudentRequiredMixin,StaffRequiredMixin


def AjaxGetKeywords(request):
    keywords = list(Keyword.objects.order_by('title').values_list('title', flat=True).filter(type=1))
    return JsonResponse({"keywords" : keywords })

def AjaxGetDetailRecommendations(request):
        project = Project.objects.get(pk=request.GET["id"])
        q_expressions = [Q(keywords=keyword.id) for keyword in project.keywords.all()]
        if q_expressions != [] :
         q = Project.objects.filter(reduce(operator.or_, q_expressions)).exclude(pk=project.pk)
         k =  q.values("pk","slug","title").annotate(keyword_count=Count("keywords")).order_by('-keyword_count')[0:5]
         return JsonResponse({"keywords" : list(k)})

        else :
         return JsonResponse({"keywords" : []})


def ProjectGetKeywords(request):
    keyword = Keyword.objects.order_by('title').values_list('title', flat=True).filter(type=1)
    keyword = list(keyword)
    keyword2 = []
    for item in keyword:
       keyword2.append({"text":item,"id":item})
    return JsonResponse({"results":keyword2,"more":True})


def ProjectGetRequirements(request):
    keyword = Keyword.objects.order_by('title').values_list('title', flat=True).filter(type=2)
    keyword = list(keyword)
    keyword2 = []
    for item in keyword:
       keyword2.append({"text":item,"value":item})
    return JsonResponse({"keyword":keyword2})

def CheckKeywordExists(request):
    try:
     keyword = Keyword.objects.get(title=request.GET["keyword"])
    except Keyword.DoesNotExist:
        return JsonResponse({'exists' : False})
    print(keyword.__dict__)
    return JsonResponse({'exists' : True, 'id' : keyword.id, 'type' :keyword.type})


class ProjectDetailView(DetailView):
    model = Project
    template_name="project/detail.html"

    def get_context_data(self,**kwargs):
       context = super(ProjectDetailView, self).get_context_data(**kwargs)
       print(context)
       context["count"] = Interest.objects.filter(project=context["object"].id).count()
       context["modalForm"] = InterestForm()
       return context

class ProjectListView(ListView):
    model = Project
    template_name="project/index.html"
    formhelper_class = ProjectFilterForm
    filter_class = ProjectFilter
    paginate_by = '10'

    def get_queryset(self, **kwargs):
            qs = super(ProjectListView, self).get_queryset()
            self.filter = self.filter_class(self.request.GET, queryset=qs)
            self.filter.form.helper = self.formhelper_class()
            print(self.filter.qs)
            return self.filter.qs


    def get_context_data(self, **kwargs):
            context = super(ProjectListView, self).get_context_data(**kwargs)
            context["filter"] = self.filter
            if self.request.GET.get('submit') == 'Submit':
                context["submit"] = True
            if self.request.GET.get('strict_id_summary') == "1":
                context["strict_id_summary"] = False
            else:
                context["strict_id_summary"] = True
            if self.request.GET.get('strict_id_keywords') == "1":
                context["strict_id_keywords"] = False
            else:
                context["strict_id_keywords"] = True
            queries_without_page = self.request.GET.copy()
            if queries_without_page.get('page') :
                del queries_without_page['page']
            context['queries'] = queries_without_page
            print(self.request.user.is_authenticated())
            return context

class ProjectCreateView(LoginRequiredMixin,StaffRequiredMixin,CreateView):
    template_name="project/create.html"
    form_class = ProjectModelForm
    model = Project
    login_url = '/user/login/'
    success_url="/project/"

    def form_invalid(self, form):
        response = super(ProjectCreateView, self).form_invalid(form)
        print("bad")
        return response
    def form_valid(self,form):
         print("good")
         if self.request.user.is_authenticated():
             print("hello")
             title = self.request.POST["title"]
             summary = self.request.POST["summary"]
             company = self.request.POST["company"]
             keywords = self.request.POST.getlist("keywords")
             print(company)
             #requirements = self.request.POST["keywords_1"]
             deadline = self.request.POST["deadline"]
             project = Project.objects.create(title=title,summary=summary,deadline=deadline,created_by=self.request.user,company=company)
             array = []
             for item in keywords:
                 print(item)
                 if item.isdigit():
                   array.append(item)
                 else :
                   print("creating")
                   keyword = Keyword.objects.create(title=item,type=2)
                   array.append(keyword.pk)
             if isinstance(array, list):
                 project.keywords.add(*array)
             project.save()
             messages.add_message(self.request, messages.SUCCESS, 'Project Created!.')
             return HttpResponseRedirect("/project")
         else:
             return HttpResponseRedirect("/project")


class ProjectUpdateView(LoginRequiredMixin,StaffRequiredMixin,UpdateView):
    template_name="project/create.html"
    form_class = ProjectModelForm
    model = Project
    login_url = '/user/login/'
    success_url = "/user/profile/projects"

    #def get(self, request, *args, **kwargs):
    #    return super(ProjectUpdateView, self).get(request, *args, **kwargs)


    def form_valid(self,form):
         print("update form valid")
         project = Project.objects.get(pk=self.kwargs['pk'])
         if project.created_by == self.request.user:
             print("hello update view")
             title = self.request.POST["title"]
             summary = self.request.POST["summary"]
             company = self.request.POST["company"]
             keywords = self.request.POST.getlist("keywords")
             print(keywords)
             #requirements = self.request.POST["keywords_1"]
             deadline = self.request.POST["deadline"]
             array = []
             for item in keywords:
                 print(item)
                 if item.isdigit():
                   array.append(item)
                 else :
                   keyword = Keyword.objects.create(title=item,type=2)
                   array.append(keyword.pk)
             project.keywords.clear()
             if isinstance(array, list):
                  project.keywords.add(*array)
             project.title = title
             project.summary = summary
             project.company = company
             project.save(update_fields=['title','summary','company'])
             messages.add_message(self.request, messages.SUCCESS, 'Project Updated!.')

             return HttpResponseRedirect("/user/profile/projects")
         else:
             return HttpResponseRedirect("/project")

    def get_context_data(self, **kwargs):
            context = super(ProjectUpdateView, self).get_context_data(**kwargs)
            context["v"] = "update"
            project = get_object_or_404(Project,pk=self.kwargs['pk'])
            if self.request.user == project.created_by:
              return context
            else:
             return HttpResponseRedirect("/project")





class ProjectFilterView(LoginRequiredMixin,ListView):
    login_url = '/user/login/'
    template_name="project/filter.html"
    model = Project
    formhelper_class = ProjectFilterForm
    filter_class = ProjectFilter

    def get_queryset(self, **kwargs):
        qs = super(ProjectFilterView, self).get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs


    def get_context_data(self, **kwargs):
        context = super(ProjectFilterView, self).get_context_data(**kwargs)
        print(self.filter)
        context["filter"] = self.filter
        return context
