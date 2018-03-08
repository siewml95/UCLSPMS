from django.test import TestCase, RequestFactory
from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver
from cuser.models import CUser as User
from .models import Project
from django.urls import reverse
import datetime
from selenium.webdriver.common.by import By

def login(self,url,email,password):
    self.client.login(email=email, password=password) #Native django test client
    cookie = self.client.cookies['sessionid']
    self.selenium.get('%s%s' % (self.live_server_url, url))
    self.selenium.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
    self.selenium.refresh() #need to update page for logged in user
    self.selenium.get('%s%s' % (self.live_server_url, url))

class ClientProjectTest(LiveServerTestCase):
     @classmethod
     def setUp(cls):
         user = User.objects.create_user(email="siewml95@gmail.com",password="qwerty12")
         user.save()
         user.profile.type = 3
         user.profile.is_verified = True
         user.profile.save()
         #super().setUpClass()
         cls.users = []
         cls.projects = []
         for x in range(1,12):
            print(x)
            project = Project.objects.create(title="Test Project {}".format(x),summary="testing project",slug="test-project-{}".format(x),company="UCL",created_by=user,status=2,deadline=(datetime.datetime.now() + datetime.timedelta(days=1)))
            cls.projects.append(project)

         cls.selenium = webdriver.Chrome()
         cls.selenium.implicitly_wait(10)

     @classmethod
     def tearDownClass(cls):
         cls.selenium.quit()
         #super().tearDownClass()

     def test_pagination(self):
         self.selenium.get('%s%s' % (self.live_server_url, '/project/?page=2'))
         #login(self,'/user/profile/projects/?page=2','siewml95@gmail.com', 'qwerty12')
         table = self.selenium.find_element(By.TAG_NAME,"section")

         rows = table.find_elements(By.TAG_NAME, "article")
         for index,row in enumerate(rows):
            title = row.find_element(By.CLASS_NAME,"title")
            self.assertEquals(title.text,self.projects[0].title)

         self.selenium.close()

     def test_get(self):
         self.selenium.get('%s%s' % (self.live_server_url, '/project/'))

         #self.selenium.get('%s%s' % (self.live_server_url, '/project/create/'))
         table = self.selenium.find_element(By.TAG_NAME,"section")

         rows = table.find_elements(By.TAG_NAME, "article")
         for index,row in enumerate(rows):
             title = row.find_element(By.CLASS_NAME,"title")
             self.assertEquals(title.text,self.projects[10-index].title)

         self.selenium.close()

class ClientCreateProjectTest(LiveServerTestCase):
    @classmethod
    def setUp(cls):
        user = User.objects.create_user(email="siewml95@gmail.com",password="qwerty12")
        user.save()
        user.profile.type = 3
        user.profile.is_verified = True
        user.profile.save()

        #super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        #super().tearDownClass()

    def test_create_project(self):

        expected_url = self.live_server_url + "/project/"
        login(self,'/project/create/','siewml95@gmail.com', 'qwerty12')
        #self.selenium.get('%s%s' % (self.live_server_url, '/project/create/'))


        title_input = self.selenium.find_element_by_name("title")
        title_input.send_keys('Project 1')
        summary_input = self.selenium.find_element_by_name("summary")
        summary_input.send_keys('Summary 1')
        company_input = self.selenium.find_element_by_name("company")
        company_input.send_keys('Company')
        deadline_input = self.selenium.find_element_by_name('deadline')
        #deadline_input.send_keys(datetime.datetime.now())
        deadline_input.send_keys("01012020")
        status_input = self.selenium.find_element_by_name('status')
        for option in status_input.find_elements_by_tag_name('option'):
          if option.text == "Active":
            option.click()
        resp = self.selenium.find_element_by_xpath('//input[@value="Submit"]').submit()
        self.selenium.implicitly_wait(1000000)

        self.assertEquals(self.selenium.current_url,expected_url)


class ClientUpdateProjectTest(LiveServerTestCase):
    @classmethod
    def setUp(cls):
        user = User.objects.create_user(email="siewml95@gmail.com",password="qwerty12")
        user.save()
        user.profile.type = 3
        user.profile.is_verified = True
        user.profile.save()
        project = Project.objects.create(id=100,title="Test Project",summary="testing project",slug="test-project",company="UCL",created_by=user,deadline=datetime.datetime.now())
        project.save()
        #super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        #super().tearDownClass()

    def test_create_project(self):

        expected_url = self.live_server_url + "/user/profile/projects/"
        login(self,'/project/100/update/','siewml95@gmail.com', 'qwerty12')
        #self.selenium.get('%s%s' % (self.live_server_url, '/project/create/'))
        title_input = self.selenium.find_element_by_name("title")
        title_input.send_keys('Project 1')
        summary_input = self.selenium.find_element_by_name("summary")
        summary_input.send_keys('Summary 1')
        company_input = self.selenium.find_element_by_name("company")
        company_input.send_keys('Company')
        deadline_input = self.selenium.find_element_by_name('deadline')
        deadline_input.send_keys("01012020")
        status_input = self.selenium.find_element_by_name('status')

        for option in status_input.find_elements_by_tag_name('option'):
                  if option.text == "Draft":
                    option.click()
        resp = self.selenium.find_element_by_xpath('//input[@value="Submit"]').submit()
        self.assertEquals(self.selenium.current_url,expected_url)
