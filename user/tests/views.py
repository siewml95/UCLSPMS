from django.test import TestCase
import datetime,json
from ..models import Profile,Invitation,Interest
from project.models import Keyword,Project
from ..views import UserProfilePasswordView
from cuser.models import CUser as User

class UserStaffRegisterViewTest(TestCase):
    @classmethod
    def setUp(self):
        invitation = Invitation.objects.create(email="contact.dataspartan@gmail.com",status=1)
        invitation.save()

    def test_get(self):
        obj = Invitation.objects.all()[0]
        resp = self.client.get('/user/invitation/{}/'.format(obj.id))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "user/register.html")

    def test_post(self):
        '''obj = Invitation.objects.all()[0]
        data = {"email":"trying@gmail.com","first_name":"First","last_name":"Last","password1":"1","password2":"1"}
        resp = self.client.post('/user/invitation/{}/'.format(obj.id),data)
        print(resp)
        self.assertEqual(resp.status_code, 200)
        user = User.objects.get(id=1)
        print(user.id)
        self.assertTrue(user.id == 1)
        self.assertTrue(user.profile.type == 3)'''

class UserRegisterViewTest(TestCase):

    def test_get(self):
        resp = self.client.get('/user/register/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "user/register.html")

    def test_post(self):
        '''data = {"email":"trying@gmail.com","first_name":"First","last_name":"Last","password1":"1","password2":"1"}
        resp = self.client.post('/user/register/',data)
        print(resp)
        self.assertEqual(resp.status_code, 200)
        user = User.objects.get(id=1)
        print(user.id)
        self.assertTrue(user.id == 1)
        self.assertTrue(user.profile.type == 1)'''
        pass



class UserProfileViewTest(TestCase):
    @classmethod
    def setUp(self):
        user = User.objects.create_user(email="testuser1",password="12345")
        user.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get('/user/profile/')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp,'/user/login/?next=/user/profile/')

    def test_get(self):
        login = self.client.login(email='testuser1', password='12345')
        print("test_get")
        print(login)
        resp = self.client.get('/user/profile/')
        print(resp)
        self.assertEqual(resp.status_code, 200)

    def test_post(self):
        login = self.client.login(email='testuser1', password='12345')
        print(login)
        data = {"first_name":"First","last_name":"Last"}
        user = User.objects.get(id=1)
        resp = self.client.post('/user/profile/',data)
        print("test_post")
        print(resp)
        updated_user = User.objects.get(id=1)
        self.assertEqual(resp.status_code, 200)
        #self.assertTrue(user.first_name != updated_user.first_name)

class UserProfilePasswordViewTest(TestCase):
    @classmethod
    def setUp(self):
        user = User.objects.create_user(email="testuser1",password="12345")
        user.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get('/user/profile/password-change/')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp,'/user/login/?next=/user/profile/password-change/')

    def test_get(self):
        login = self.client.login(email='testuser1', password='12345')
        print("test_get")
        print(login)
        resp = self.client.get('/user/profile/password-change/')
        print(resp)
        self.assertEqual(resp.status_code, 200)

    def test_post(self):
        print("UserProfilePasswordViewTest")

        '''login = self.client.login(email='testuser1', password='12345')
        print(login)
        data = {"passwordcurrent":"12345","password1":"1234","password2":"1234"}
        user = User.objects.get(id=1)
        current = user.password
        resp = self.client.post('/user/profile/password-change/',data)
        print("test_post")
        print(resp)
        updated_user = User.objects.get(id=1)
        print(updated_user.password)
        print(current)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(current != updated_user.password)'''
        pass

class UserProfilePreferenceViewTest(TestCase):
    @classmethod
    def setUp(self):
        user = User.objects.create_user(email="testuser1",password="12345")
        user.save()
        Keyword.objects.create(title="keyword 1",type=1)
        Keyword.objects.create(title="keyword 2",type=1)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get('/user/profile/preferences/')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp,'/user/login/?next=/user/profile/preferences/')

    def test_get(self):
        login = self.client.login(email='testuser1', password='12345')
        print("test_get")
        print(login)
        resp = self.client.get('/user/profile/preferences/')
        print(resp)
        self.assertEqual(resp.status_code, 200)

    def test_post(self):
        login = self.client.login(email='testuser1', password='12345')
        data = {"preferences":[1,2]}
        resp = self.client.post('/user/profile/preferences/',data)
        self.assertEqual(resp.status_code, 302)
        user = User.objects.get(id=1)
        print("getting prefrences")
        print(user.profile.preferences)


class UserProfileProjectViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(email='testuser1', password='12345')
        user.save()
        user.profile.type = 3
        user.profile.save()
        user2 = User.objects.create_user(email='testuser2', password='12345')
        user2.save()
        number_of_projects = 13
        for project_num in range(number_of_projects):
            Project.objects.create(title="Test Project {}".format(project_num),summary="testing project",slug="test-project-{}".format(project_num),company="UCL",created_by=user,deadline=datetime.datetime.now())


    def test_must_be_logged_in(self):
        resp = self.client.get('/user/profile/projects/')
        self.assertEqual(resp.status_code,302)

    def test_must_be_staff(self):
       login = self.client.login(email='testuser2', password='12345')
       resp = self.client.get('/user/profile/projects/')
       self.assertEqual(resp.status_code,302)

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(email='testuser1', password='12345')
        print("UserProfileProjectViewTest")
        print(login)
        print(User.objects.get(id=1).profile.type)
        resp = self.client.get('/user/profile/projects/')
        self.assertEqual(resp.status_code,200)

    def test_view_url_uses_correct_template(self):
        login = self.client.login(email='testuser1', password='12345')
        resp = self.client.get('/user/profile/projects/')
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp,"user/profile/projects.html")

    def test_pagination_is_ten(self):
        login = self.client.login(email='testuser1', password='12345')
        resp = self.client.get('/user/profile/projects/')
        self.assertEqual(resp.status_code,200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        print(resp.context['object_list'])
        self.assertTrue(len(resp.context['object_list']) == 10)

    def test_list_all_projects(self):
        login = self.client.login(email='testuser1', password='12345')
        resp = self.client.get('/user/profile/projects/?page=2')
        self.assertEqual(resp.status_code,200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['object_list']) == 3)

class UserProfileInterestViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(email='testuser1', password='12345')
        user.save()
        user.profile.type = 3
        user.profile.save()
        user2 = User.objects.create_user(email='testuser2', password='12345')
        user2.save()
        number_of_projects = 13
        number_of_interests = 13
        for project_num in range(number_of_projects):
            Project.objects.create(title="Test Project {}".format(project_num),summary="testing project",slug="test-project-{}".format(project_num),company="UCL",created_by=user,deadline=datetime.datetime.now())
        for interest_num in range(number_of_interests):
            Interest.objects.create(project=Project.objects.get(id=(interest_num + 1)),user=user2)

    def test_must_be_logged_in(self):
        resp = self.client.get('/user/profile/project-interests/')
        self.assertEqual(resp.status_code,302)

    def test_must_be_student(self):
       login = self.client.login(email='testuser1', password='12345')
       resp = self.client.get('/user/profile/project-interests/')
       self.assertEqual(resp.status_code,302)

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(email='testuser2', password='12345')
        resp = self.client.get('/user/profile/project-interests/')
        self.assertEqual(resp.status_code,200)

    def test_view_url_uses_correct_template(self):
        login = self.client.login(email='testuser2', password='12345')
        resp = self.client.get('/user/profile/project-interests/')
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp,"user/profile/project_interests.html")

    def test_pagination_is_ten(self):
        login = self.client.login(email='testuser2', password='12345')
        resp = self.client.get('/user/profile/project-interests/')
        self.assertEqual(resp.status_code,200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        print(resp.context['object_list'])
        self.assertTrue(len(resp.context['object_list']) == 10)

    def test_list_all_projects(self):
        login = self.client.login(email='testuser2', password='12345')
        resp = self.client.get('/user/profile/project-interests/?page=2')
        self.assertEqual(resp.status_code,200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['object_list']) == 3)


class UserProfileStaffInterestViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(email='testuser1', password='12345')
        user.save()
        user.profile.type = 3
        user.profile.save()
        user2 = User.objects.create_user(email='testuser2', password='12345')
        user2.save()
        number_of_projects = 13
        number_of_interests = 13
        for project_num in range(number_of_projects):
            Project.objects.create(title="Test Project {}".format(project_num),summary="testing project",slug="test-project-{}".format(project_num),company="UCL",created_by=user,deadline=datetime.datetime.now())
        for interest_num in range(number_of_interests):
            Interest.objects.create(project=Project.objects.get(id=(interest_num + 1)),user=user2)

    def test_must_be_logged_in(self):
        resp = self.client.get('/user/profile/interests/')
        self.assertEqual(resp.status_code,302)

    def test_must_be_staff(self):
       login = self.client.login(email='testuser2', password='12345')
       resp = self.client.get('/user/profile/interests/')
       self.assertEqual(resp.status_code,302)

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(email='testuser1', password='12345')
        resp = self.client.get('/user/profile/interests/')
        self.assertEqual(resp.status_code,200)

    def test_view_url_uses_correct_template(self):
        login = self.client.login(email='testuser1', password='12345')
        resp = self.client.get('/user/profile/interests/')
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp,"user/profile/interests.html")

    def test_pagination_is_ten(self):
        login = self.client.login(email='testuser1', password='12345')
        resp = self.client.get('/user/profile/interests/')
        self.assertEqual(resp.status_code,200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        print(resp.context['object_list'])
        self.assertTrue(len(resp.context['object_list']) == 10)

    def test_list_all_projects(self):
        login = self.client.login(email='testuser1', password='12345')
        resp = self.client.get('/user/profile/interests/?page=2')
        self.assertEqual(resp.status_code,200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['object_list']) == 3)

class UserProjectListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(email='testuser1', password='12345')
        user.save()
        user.profile.type = 3
        user.profile.save()
        number_of_projects = 13
        for project_num in range(number_of_projects):
            Project.objects.create(title="Test Project {}".format(project_num),summary="testing project",slug="test-project-{}".format(project_num),company="UCL",created_by=user,deadline=datetime.datetime.now())

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/user/single/1/')
        self.assertEqual(resp.status_code,200)

    def test_view_url_uses_correct_template(self):
        resp = self.client.get('/user/single/1/')
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp,"user/project-list.html")

    def test_pagination_is_ten(self):
        resp = self.client.get('/user/single/1/')
        self.assertEqual(resp.status_code,200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        print(resp.context['object_list'])
        self.assertTrue(len(resp.context['object_list']) == 10)

    def test_list_all_projects(self):
        resp = self.client.get('/user/single/1/?page=2')
        self.assertEqual(resp.status_code,200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['object_list']) == 3)

class UserStudentDetailViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(email='testuser1', password='12345')
        user.save()
        user.profile.type = 3
        user.profile.save()
        user2 = User.objects.create_user(email='testuser2', password='12345')
        user2.save()
        Project.objects.create(title="Test Project",summary="testing project",slug="test-project",company="UCL",created_by=user,deadline=datetime.datetime.now())


    def test_must_be_logged_in(self):
        resp = self.client.get('/user/student/2/')
        self.assertEqual(resp.status_code,302)

    def test_must_be_staff(self):
       login = self.client.login(email='testuser2', password='12345')
       resp = self.client.get('/user/student/2/')
       self.assertEqual(resp.status_code,302)

    #some proble here
    def test_can_view_student_only(self):
         login = self.client.login(email='testuser1', password='12345')
         resp = self.client.get('/user/student/1/')
         self.assertEqual(resp.status_code,200)
    def test_get(self):
        login = self.client.login(email='testuser1', password='12345')

        resp = self.client.get('/user/student/2/')
        student = User.objects.get(id=2)

        context_student = resp.context["object"]
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'user/student/detail.html')
        self.assertEqual(student,context_student)


class getIndexRecommendationsTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(email="username",password="qwerty12")
        user2 = User.objects.create_user(email="username2",password="qwerty12")
        self.user2 = user2

        Keyword.objects.create(title="Test Keyword",type=1,status=True)
        Keyword.objects.create(title="Test Keyword 2",type=1,status=True)
        Keyword.objects.create(title="Test Keyword 3",type=1,status=True)
        Keyword.objects.create(title="Test Keyword 4",type=1,status=True)
        Keyword.objects.create(title="Test Keyword 5",type=1,status=True)
        Keyword.objects.create(title="Test Keyword 6",type=1,status=True)
        Keyword.objects.create(title="Test Keyword 7",type=1,status=True)
        self.projects = []
        project = Project.objects.create(title="Test Project",summary="testing project",slug="test-project",company="UCL",created_by=user,deadline=datetime.datetime.now())
        project.keywords = [1,2]
        print(project)
        project.save()
        self.projects.append(project)
        project = Project.objects.create(title="Test Project2",summary="testing project",slug="test-project-2",company="UCL",created_by=user,deadline=datetime.datetime.now())
        project.keywords = [1,2,3]

        project.save()
        self.projects.append(project)

        self.project = project
        project = Project.objects.create(title="Test Project",summary="testing project",slug="test-project-3",company="UCL",created_by=user,deadline=datetime.datetime.now())
        project.keywords = [3,4]

        project.save()
        self.projects.append(project)

        project_interested = Project.objects.create(title="Test Project",summary="testing project",slug="test-project-412",company="UCL",created_by=user,deadline=datetime.datetime.now())
        project_interested.keywords = [1,2,3,5]

        project_interested.save()
        self.project_interested = project_interested
        self.projects.append(project_interested)

        project =Project.objects.create(title="Test Project",summary="testing project",slug="test-project-4",company="UCL",created_by=user,deadline=datetime.datetime.now())
        project.keywords = [1,2,5]
        project.save()
        self.projects.append(project)

        project =Project.objects.create(title="Test Project",summary="testing project",slug="test-project-5",company="UCL",created_by=user,deadline=datetime.datetime.now())
        project.keywords = [2,3,5]
        project.save()
        self.projects.append(project)

        project =Project.objects.create(title="Test Project",summary="testing project",slug="test-project-6",company="UCL",created_by=user,deadline=datetime.datetime.now())
        project.keywords = [2,3,4]

        project.save()
        self.projects.append(project)

        project = Project.objects.create(title="Test Project",summary="testing project",slug="test-project-7",company="UCL",created_by=user,deadline=datetime.datetime.now())
        project.keywords = [2,3,5]
        project.save()
        self.projects.append(project)


    def test_preferences_empty_interests_empty(self):
        print("test_preferences_empty_interests_empty")
        login = self.client.login(email='username2', password='qwerty12')
        resp = self.client.get('/user/ajax/getIndexRecommendations/?id=0')
        obj = json.loads(((resp._container)[0]).decode('utf-8'))
        print(obj)
        projects = obj["recommendations"]
        self.assertEqual(len(projects),0)


    def test_preferences_not_empty_interests_empty(self):
        print("test_preferences_not_empty_interests_empty")

        self.user2.profile.preferences = [3]
        self.user2.profile.save()
        login = self.client.login(email='username2', password='qwerty12')
        resp = self.client.get('/user/ajax/getIndexRecommendations/?id=0')
        obj = json.loads(((resp._container)[0]).decode('utf-8'))
        print(obj)
        projects = obj["recommendations"]
        self.assertEqual(len(projects),6)

    def test_preferences_empty_interests_not_empty(self):
        print("test_preferences_empty_interests_not_empty")
        Interest.objects.create(user=self.user2,project=self.project_interested)
        login = self.client.login(email='username2', password='qwerty12')
        resp = self.client.get('/user/ajax/getIndexRecommendations/?id=0')
        obj = json.loads(((resp._container)[0]).decode('utf-8'))
        print(obj)
        projects = obj["recommendations"]
        self.assertEqual(len(projects),7)


    def test_preferences_not_empty_interests_not_empty(self):
        print("test_preferences_not_empty_interests_not_empty")

        self.user2.profile.preferences = [3]
        self.user2.profile.save()
        Interest.objects.create(user=self.user2,project=self.project_interested)
        login = self.client.login(email='username2', password='qwerty12')
        resp = self.client.get('/user/ajax/getIndexRecommendations/?id=0')
        obj = json.loads(((resp._container)[0]).decode('utf-8'))
        print(obj)
        print("test_preferences_empty_interests_empty")
        projects = obj["recommendations"]
        self.assertEqual(len(projects),8)
