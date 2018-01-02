from django.test import TestCase, RequestFactory

# Create your tests here.
from .models import Project,Keyword
from django.contrib.auth.models import User
from .forms import ProjectModelForm,ProjectFilterForm
from .views import ProjectUpdateView,ProjectCreateView
import datetime
from django.contrib.auth.models import User

class KeywordModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Keyword.objects.create(title="Test Keyword",type=1,status=True)

    def test_title_label(self):
        keyword = Keyword.objects.get(id=1)
        field_label = keyword._meta.get_field('title').verbose_name
        self.assertEquals(field_label,'title')

    def test_type_label(self):
        keyword = Keyword.objects.get(id=1)
        field_label = keyword._meta.get_field('type').verbose_name
        self.assertEquals(field_label,'type')

    def test_status_label(self):
        keyword = Keyword.objects.get(id=1)
        field_label = keyword._meta.get_field('status').verbose_name
        self.assertEquals(field_label,'status')


class ProjectModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create()
        Project.objects.create(title="Test Project",summary="testing project",slug="test-project",company="UCL",created_by=user,deadline=datetime.datetime.now())

    def test_title_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('title').verbose_name
        self.assertEquals(field_label,'title')

    def test_summary_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('title').verbose_name
        self.assertEquals(field_label,'title')

    def test_slug_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('slug').verbose_name
        self.assertEquals(field_label,'slug')


    def test_company_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('company').verbose_name
        self.assertEquals(field_label,'company')

    def test_created_by_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('created_by').verbose_name
        self.assertEquals(field_label,'created by')

    def test_updated_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('updated').verbose_name
        self.assertEquals(field_label,'updated')

    def test_timestamp_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('deadline').verbose_name
        self.assertEquals(field_label,'deadline')

    def test_keywords_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('keywords').verbose_name
        self.assertEquals(field_label,'keywords')

    def test_title_max_length(self):
        project = Project.objects.get(id=1)
        max_length = project._meta.get_field('title').max_length
        self.assertEquals(max_length,250)



class ProjectModelFormTest(TestCase):


    @classmethod
    def setUpTestData(cls):
        user = User.objects.create()
    def test_title_required(self):
        user = User.objects.get(id=1)

        form = ProjectModelForm(data={'summary':"test summary","slug":"test-summary","company":"UCL","created_by":user,"deadline":datetime.datetime.now()})
        self.assertEquals(form.is_valid(),False)

    def test_summary_required(self):
        user = User.objects.get(id=1)
        form = ProjectModelForm(data={'title':'test',"slug":"test-summary","company":"UCL","created_by":user,"deadline":datetime.datetime.now()})
        self.assertEquals(form.is_valid(),False)

    def test_company_required(self):
        user = User.objects.get(id=1)
        form = ProjectModelForm(data={'title':'test','summary':"test summary","slug":"test-summary","created_by":user,"deadline":datetime.datetime.now()})
        self.assertEquals(form.is_valid(),False)

    def test_deadline_required(self):
        user = User.objects.get(id=1)
        form = ProjectModelForm(data={'title':'test','summary':"test summary","slug":"test-summary","created_by":user,"company":"UCL"})
        self.assertEquals(form.is_valid(),False)



class ProjectListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create()
        number_of_projects = 13
        for project_num in range(number_of_projects):
            Project.objects.create(title="Test Project {}".format(project_num),summary="testing project",slug="test-project-{}".format(project_num),company="UCL",created_by=user,deadline=datetime.datetime.now())

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/project/')
        self.assertEqual(resp.status_code,200)

    def test_view_url_uses_correct_template(self):
        resp = self.client.get('/project/')
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp,"project/index.html")

    def test_pagination_is_ten(self):
        resp = self.client.get('/project/')
        self.assertEqual(resp.status_code,200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        print(resp.context['object_list'])
        self.assertTrue(len(resp.context['object_list']) == 10)

    def test_list_all_projects(self):
        resp = self.client.get('/project/?page=2',{})
        self.assertEqual(resp.status_code,200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['object_list']) == 3)


class ProjectCreateViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1',password='12345')
        test_user2 = User.objects.create_user(username='testuser2',password='12345')



        test_user1.save()
        test_user2.save()
        test_user1.profile.type = 1
        test_user1.profile.save()
        test_user2.profile.type = 3
        test_user2.profile.save()


    def test_redirect_if_not_logged_in(self):
        resp = self.client.get('/project/create/')
        self.assertRedirects(resp,'/user/login/?next=/project/create/')

    def test_redirect_if_is_student(self):
        login = self.client.login(username='testuser1', password='12345')
        print("login")
        resp = self.client.get('/project/create/')
        self.assertRedirects(resp,'/user/login/?next=/project/create/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='12345')
        user = User.objects.get(id=2)
        resp = self.client.get('/project/create/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(str(resp.context['user']), 'testuser2')
        self.assertTemplateUsed(resp, 'project/create.html')

    def test_post(self):
        login = self.client.login(username='testuser2', password='12345')
        user = User.objects.get(id=1)

        data = {
           'title' : 'Project',
           "summary":"testing project",
           "slug":"test-project",
           "company":"UCL",
           "deadline":datetime.date(year=2100, month=1,day=1),
        }
        response = self.client.post("/project/create/", data)
        print("response")
        print(response)
        self.assertEqual(response.status_code, 302)
        project = Project.objects.get(id=1)
        self.assertEqual(project.id,1)


class ProjectDetailViewTest(TestCase):
    def setUp(self):
        user = User.objects.create()
        Project.objects.create(title="Test Project",summary="testing project",slug="test-project",company="UCL",created_by=user,deadline=datetime.datetime.now())

    def test_get(self):
        resp = self.client.get('/project/single/test-project/')
        created_project = Project.objects.get(id=1)
        print("resp detail")
        project = resp.context[-1]["project"]
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'project/detail.html')
        self.assertEqual(project,project)

class ProjectUpdateViewTest(TestCase):
    def setUp(self):
            self.factory = RequestFactory()
            Keyword.objects.create(title="keyword",type=1)
            test_user1 = User.objects.create_user(username='testuser1',password='12345')
            test_user2 = User.objects.create_user(username='testuser2',password='12345')

            test_user1.save()
            test_user2.save()
            test_user1.profile.type = 3
            test_user1.profile.save()
            test_user2.profile.type = 3
            test_user2.profile.save()
            Project.objects.create(title="Test Project",summary="testing project",slug="test-project",company="UCL",created_by=test_user2,deadline=datetime.datetime.now())

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get('/project/1/update/')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp,'/user/login/?next=/project/1/update/')


    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='12345')
        user = User.objects.get(id=2)
        resp = self.client.get('/project/1/update/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'project/create.html')

    def test_redirect_if_not_creator(self):
        login = self.client.login(username='testuser1', password='12345')
        print("resp")
        try:
          resp = self.client.get('/project/1/update/')
          self.assertFalse(1,1)
        except TypeError:
          self.assertTrue(1,1)

    def test_post(self):
        login = self.client.login(username='testuser2', password='12345')
        user = User.objects.get(id=2)
        current_project = Project.objects.get(id=1)
        data = {
                   'title' : 'Project',
                   "summary":"testing project",
                   "company":"UCL",
                   "deadline":datetime.date(year=2100, month=1,day=1),
                   "keywords" : [1]
                }
        response = self.client.post("/project/1/update/", data)

        print(response)
        self.assertEqual(response.status_code, 302)
        project = Project.objects.get(id=1)
        print(project.title)
        self.assertFalse(project.title == current_project.title)
