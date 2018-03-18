from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import ProjectFilter
from .forms import ProjectModelForm, ProjectFilterForm,ProjectDetailFilterForm,ProjectModelUpdateForm
from .models import Project,Keyword,Organization
from user.models import Interest
from user.forms import InterestForm
from rake_nltk import Rake
# Create your views here.
from django.shortcuts import get_object_or_404
from django.db.models import Q,Count
from  functools import reduce
import operator,numbers,datetime
from django.contrib import messages
from user.views import StudentRequiredMixin,StaffRequiredMixin,StaffVerifiedRequiredMixin


def AjaxGetKeywords(request):
    keywords = list(Keyword.objects.order_by('title').values_list('title', flat=True).filter(type=1,status=True))
    return JsonResponse({"keywords" : keywords })

def AjaxGetDetailRecommendations(request):
        project = Project.objects.get(pk=request.GET["id"])
        q_expressions = [Q(keywords=keyword.id) for keyword in project.keywords.active()]
        if q_expressions != [] :
         q = Project.objects.published().filter(reduce(operator.or_, q_expressions)).exclude(pk=project.pk)
         k =  q.values("pk","slug","title").annotate(keyword_count=Count("keywords")).order_by('-keyword_count')[0:5]
         return JsonResponse({"keywords" : list(k)},status=200)
        else :
         return JsonResponse({"keywords" : list(k)},status=200)


def ProjectGetKeywords(request):
    keyword = Keyword.objects.active().order_by('title').values_list('title', flat=True).filter(type=1)
    keyword = list(keyword)
    keyword2 = []
    for item in keyword:
       keyword2.append({"text":item,"id":item})
    return JsonResponse({"results":keyword2,"more":True})


def ProjectGetRequirements(request):
    keyword = Keyword.objects.active().order_by('title').values_list('title', flat=True).filter(type=2)
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
    if keyword.status == True:
       return JsonResponse({'exists' : True, "active" : True,'id' : keyword.id, 'type' :keyword.type})
    else:
       return JsonResponse({'exists' : True, "active": False,'id' : keyword.id, 'type' :keyword.type})


class ProjectDetailView(DetailView):
    model = Project
    template_name="project/detail.html"
    form_class = ProjectDetailFilterForm


    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except:
            return HttpResponseRedirect("/")
        context = self.get_context_data(object=self.object)
        if context["object"].status == 1:
            return HttpResponseRedirect("/")
        return self.render_to_response(context)

    def get_context_data(self,**kwargs):
       context = super(ProjectDetailView, self).get_context_data(**kwargs)
       print(context)
       context["count"] = Interest.objects.filter(project=context["object"].id).count()
       context["modalForm"] = InterestForm()
       context["form"] = ProjectDetailFilterForm()
       context["strict_id_summary"] = True
       context["strict_id_keywords"] = True
       context["deadline_not_passed"] = context["object"].deadline >= datetime.date.today()
       context["title"] = context["object"].title
       return context


class ProjectListView(ListView):
    model = Project
    template_name="project/index.html"
    formhelper_class = ProjectFilterForm
    filter_class = ProjectFilter
    paginate_by = '10'

    def get_queryset(self, **kwargs):
            qs = super(ProjectListView, self).get_queryset()
            print(self.request.GET)
            print(self.request.GET.getlist("status"))
            if self.request.GET.getlist("status") == []:
                print("qs")
                print(qs)
                qs = qs.published()
                print(qs)
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

class ProjectCreateView(LoginRequiredMixin,StaffVerifiedRequiredMixin,CreateView):
    template_name="project/create.html"
    form_class = ProjectModelForm
    model = Project
    login_url = '/user/login/'
    success_url="/project/"
    required_url = "/user/profile/"
    title = "Create Project"

    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        context["title"] = self.title
        return context

    def form_invalid(self, form):
        response = super(ProjectCreateView, self).form_invalid(form)
        print("bad")
        print(form.__dict__)
        return response


    def form_valid(self,form):
         print("good")
         if self.request.user.is_authenticated():

             project = form.save(created_by=self.request.user)
             print("hello")
             organization = self.request.POST["organization"]
             if organization.isdigit():
                 old_organization = Organization.objects.get(pk=organization)
                 project.organization = old_organization
             else:
                new_organization = Organization.objects.create(title=organization,type=2,status=True)
                project.organization = new_organization


             keywords = self.request.POST.getlist("keywords")
             array = []
             for item in keywords:
                 print(item)
                 if item.isdigit():
                   array.append(item)
                 else :
                   try:
                     keyword = Keyword.objects.get(title=item)
                   except Keyword.DoesNotExist:
                     keyword = Keyword.objects.create(title=item,type=2,status=True)
                     array.append(keyword.pk)
             if isinstance(array, list):
                 project.keywords.add(*array)
             project.save()
             print(project.keywords.all())
             messages.add_message(self.request, messages.SUCCESS, 'Project Created!.')
             return HttpResponseRedirect("/project")
         else:
             return HttpResponseRedirect("/project")


class ProjectUpdateView(LoginRequiredMixin,StaffVerifiedRequiredMixin,UpdateView):
    template_name="project/create.html"
    form_class = ProjectModelUpdateForm
    model = Project
    login_url = '/user/login/'
    success_url = "/user/profile/projects"
    required_url = "/user/profile/"
    #def get(self, request, *args, **kwargs):
    #    return super(ProjectUpdateView, self).get(request, *args, **kwargs)
    title = "Update Project"

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdateView, self).get_context_data(**kwargs)
        context["title"] = self.title
        return context

    def form_valid(self,form):
         print("update form valid")
         project = Project.objects.get(pk=self.kwargs['pk'])
         if project.created_by == self.request.user:
             keywords = self.request.POST.getlist("keywords")
             project = form.save(created_by=self.request.user)
             print('project')
             print(project.__dict__)
             #requirements = self.request.POST["keywords_1"]
             array = []
             for item in keywords:
                 print(item)
                 if item.isdigit():
                   array.append(item)
                 else :
                   try:
                     keyword = Keyword.objects.get(title=item)
                   except Keyword.DoesNotExist:
                     keyword = Keyword.objects.create(title=item,type=2,status=True)
                     array.append(keyword.pk)
             project.keywords.clear()
             if isinstance(array, list):
                  project.keywords.add(*array)
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
