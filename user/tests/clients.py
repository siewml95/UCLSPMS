from django.test import TestCase, RequestFactory
from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from cuser.models import CUser as User
from project.models import Project,Organization
from ..models import Interest
from django.urls import reverse
import datetime,time,os

def load_driver():
    if os.environ.get("DRIVER") == "MOZILLA":
        return webdriver.Firefox()
    elif os.environ.get("DRIVER") == "PHANTOMJS":
        return webdriver.PhantomJS()
    else :
        return webdriver.Chrome()

def login(self,url,email,password):
    self.selenium.delete_all_cookies();
    self.client.login(email=email, password=password) #Native django test client
    cookie = self.client.cookies['sessionid']
    self.selenium.get('%s%s' % (self.live_server_url, url))
    self.selenium.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
    self.selenium.refresh() #need to update page for logged in user
    self.selenium.get('%s%s' % (self.live_server_url, url))
    print("login")


class ClientLoginTest(LiveServerTestCase):
    @classmethod
    def setUp(cls):
        user = User.objects.create_user(email="siewml95@gmail.com",password="qwerty12")

        cls.selenium = load_driver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        #super().tearDownClass()

    def test_login_wrong_credential(self):
        expected_url = self.live_server_url + "/user/login/"
        self.selenium.get('%s%s' % (self.live_server_url, '/user/login/'))
        username_input = self.selenium.find_element_by_name("email")
        username_input.send_keys('siewml95@gmail.com')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('qwerty123')
        resp = self.selenium.find_element_by_xpath('//input[@value="Submit"]').click()
        self.assertEquals(self.selenium.current_url,expected_url)

    def test_login(self):

        expected_url = self.live_server_url + "/project/"
        self.selenium.get('%s%s' % (self.live_server_url, '/user/login/'))
        username_input = self.selenium.find_element_by_name("email")
        username_input.send_keys('siewml95@gmail.com')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('qwerty12')
        resp = self.selenium.find_element_by_xpath('//input[@value="Submit"]').click()
        self.assertEquals(self.selenium.current_url,expected_url)


class ClientUserProfileTest(LiveServerTestCase):
    @classmethod
    def setUp(cls):
        user = User.objects.create_user(email="siewml95@gmail.com",password="qwerty12")
        user.profile.type = 3
        user.profile.is_verified = True
        user.profile.save()
        #super().setUpClass()
        cls.selenium = load_driver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        #super().tearDownClass()

    def test_post(self):

        expected_url = self.live_server_url + "/user/profile/"
        login(self,'/user/profile/','siewml95@gmail.com', 'qwerty12')
        #self.selenium.get('%s%s' % (self.live_server_url, '/project/create/'))

        first_name_input = self.selenium.find_element_by_name("first_name")
        first_name_input.send_keys('First Name')
        last_name_input = self.selenium.find_element_by_name("last_name")
        last_name_input.send_keys('Last Name')
        resp = self.selenium.find_element_by_xpath('//input[@value="Submit"]').click()
        updated_user = User.objects.get(id=1)
        self.assertEquals(updated_user.first_name,"First Name")


class ClientUserProfilePasswordTest(LiveServerTestCase):
    @classmethod
    def setUp(cls):
        user = User.objects.create_user(email="siewml951@gmail.com",password="qwerty12")
        user.save()
        user.profile.type = 1
        user.profile.is_verified = True
        user.profile.save()
        #super().setUpClass()
        cls.selenium = load_driver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        #super().tearDownClass()

    def test_post(self):

        expected_url = self.live_server_url + "/user/profile/"
        login(self,'/user/profile/password-change/','siewml951@gmail.com', 'qwerty12')
        #self.selenium.get('%s%s' % (self.live_server_url, '/project/create/'))

        passwordcurrent_input = self.selenium.find_element_by_name("passwordcurrent")
        passwordcurrent_input.send_keys('qwerty12')
        password1_input = self.selenium.find_element_by_name("password1")
        password1_input.send_keys('Qazwsx12')
        password2_input = self.selenium.find_element_by_name("password2")
        password2_input.send_keys('Qazwsx12')

        resp = self.selenium.find_element_by_xpath('//input[@value="Submit"]').click()
        updated_user = User.objects.get(email="siewml951@gmail.com")
        self.assertEquals(updated_user.check_password('Qazwsx12'),True)


class ClientUserProfileTest(LiveServerTestCase):
    @classmethod
    def setUp(cls):
        user = User.objects.create_user(email="siewml95@gmail.com",password="qwerty12")
        user.profile.type = 3
        user.profile.is_verified = True
        user.profile.save()
        #super().setUpClass()
        cls.selenium = load_driver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        #super().tearDownClass()

    def test_post(self):

        expected_url = self.live_server_url + "/user/profile/"
        login(self,'/user/profile/','siewml95@gmail.com', 'qwerty12')
        #self.selenium.get('%s%s' % (self.live_server_url, '/project/create/'))

        first_name_input = self.selenium.find_element_by_name("first_name")
        first_name_input.send_keys('First Name')
        last_name_input = self.selenium.find_element_by_name("last_name")
        last_name_input.send_keys('Last Name')
        resp = self.selenium.find_element_by_xpath('//input[@value="Submit"]').click()
        updated_user = User.objects.get(email="siewml95@gmail.com")
        self.assertEquals(updated_user.first_name,"First Name")


class ClientUserRegisterTest(LiveServerTestCase):
    @classmethod
    def setUp(cls):
        #super().setUpClass()
        cls.selenium = load_driver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        #super().tearDownClass()

    def test_post(self):

        expected_url = self.live_server_url + "/user/register/"
        #self.selenium.get('%s%s' % (self.live_server_url, '/project/create/'))
        self.selenium.get('%s%s' % (self.live_server_url, '/user/register/'))

        email_input = self.selenium.find_element_by_name("email")
        email_input.send_keys('siewml951@gmail.com')
        password_input = self.selenium.find_element_by_name("password1")
        password_input.send_keys('qwerty12')
        password2_input = self.selenium.find_element_by_name("password2")
        password2_input.send_keys('qwerty12')
        first_name_input = self.selenium.find_element_by_name("first_name")
        first_name_input.send_keys('First')
        last_name_input = self.selenium.find_element_by_name("last_name")
        last_name_input.send_keys('Last')
        self.selenium.find_element_by_xpath('//input[@value="Submit"]').click()
        try:
           user = User.objects.get(email="siewml951@gmail.com")
           self.assertEquals(user.email,"siewml951@gmail.com")
           self.assertEquals(user.first_name,'First')
           self.assertEquals(user.last_name,'Last')
        except:
           self.assertEquals(True,False)

class ClientUserProfileStudentInterestTest(LiveServerTestCase):
    @classmethod
    def setUp(cls):
        staff = User.objects.create_user(email="try@gmail.com",password="qwerty12")
        staff.profile.type = 3
        staff.profile.is_verified = True
        staff.profile.save()
        user = User.objects.create_user(email="siewml95@gmail.com",password="qwerty12")
        user.profile.type = 1
        user.profile.is_verified = True
        user.profile.save()
        cls.users = []
        cls.projects = []
        cls.organization = Organization.objects.create(title="UCL",status=True)
        cls.organization.save()
        for x in range(1,12):
            print(x)
            project = Project.objects.create(title="Test Project {}".format(x),summary="testing project",slug="test-project-{}".format(x),organization=cls.organization,created_by=staff,deadline=datetime.datetime.now())
            cls.projects.append(project)

        for x in range(1,12):
            Interest.objects.create(user=user,project=cls.projects[x-1])
        cls.selenium = load_driver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()


    def test_pagination(self):
        print("pagination")
        #login(self,'/user/profile/projects/?page=2','siewml95@gmail.com', 'qwerty12')
        login(self,'/user/profile/project-interests/?page=2','siewml95@gmail.com', 'qwerty12')
        print("pageination2")
        table = self.selenium.find_element_by_tag_name("table")
        tbody = table.find_element(By.TAG_NAME,"tbody")

        rows = tbody.find_elements(By.TAG_NAME, "tr")
        for index,row in enumerate(rows):
            print(row)
            cols = row.find_elements(By.TAG_NAME, "td")  # note: index start from 0, 1 is col 2
            if len(cols) >= 2 :
                  self.assertEquals(cols[0].text,self.projects[0].title)
                  #self.assertEquals(href.get_attribute("href"),'%s%s' % (self.live_server_url, '/project/{}/update/'.format(project.id)))

            else :
                 self.assertEquals(True,False)
        self.selenium.close()

    def test_get(self):

        #self.selenium.get('%s%s' % (self.live_server_url, '/project/create/'))
        login(self,'/user/profile/project-interests/','siewml95@gmail.com', 'qwerty12')
        table = self.selenium.find_element_by_tag_name("table")
        tbody = table.find_element(By.TAG_NAME,"tbody")

        rows = tbody.find_elements(By.TAG_NAME, "tr")
        for index,row in enumerate(rows):
            cols = row.find_elements(By.TAG_NAME, "td")  # note: index start from 0, 1 is col 2
            if len(cols) >= 2 :
                 self.assertEquals(cols[0].text,self.projects[10-index].title)
                 #self.assertEquals(href.get_attribute("href"),'%s%s' % (self.live_server_url, '/project/{}/update/'.format(project.id)))

            else :
                 self.assertEquals(True,False)
        self.selenium.close()

class ClientUserProfileStaffInterestTest(LiveServerTestCase):
    @classmethod
    def setUp(cls):
        user = User.objects.create_user(email="siewml95@gmail.com",password="qwerty12")
        user.profile.type = 3
        user.profile.is_verified = True
        user.profile.save()
        cls.organization = Organization.objects.create(title="UCL",status=True)
        cls.organization.save()
        cls.project = Project.objects.create(title="Test Project",summary="testing project",slug="test-project",organization=cls.organization,created_by=user,deadline=datetime.datetime.now())
        cls.users = []

        for x in range(1,12):
            user = User.objects.create_user(email="siewml95{}@gmail.com".format(x),password="qwerty12")
            user.profile.type = 1
            user.profile.is_verified = True
            user.profile.save()
            cls.users.append(user)
            Interest.objects.create(user=user,project=cls.project)
        cls.selenium = load_driver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()


    def test_pagination(self):
        print("pagination")
        #login(self,'/user/profile/projects/?page=2','siewml95@gmail.com', 'qwerty12')
        login(self,'/user/profile/interests/?page=2','siewml95@gmail.com', 'qwerty12')
        print("pageination2")
        table = self.selenium.find_element_by_tag_name("table")
        tbody = table.find_element(By.TAG_NAME,"tbody")

        rows = tbody.find_elements(By.TAG_NAME, "tr")
        for index,row in enumerate(rows):
            print(row)
            cols = row.find_elements(By.TAG_NAME, "td")  # note: index start from 0, 1 is col 2
            href = cols[0].find_element(By.TAG_NAME,"a")
            if len(cols) >= 2 :
                  self.assertEquals(cols[0].text,self.users[index].first_name + self.users[index].last_name )
                  #self.assertEquals(href.get_attribute("href"),'%s%s' % (self.live_server_url, '/project/{}/update/'.format(project.id)))
                  self.assertEquals(cols[1].text,self.project.title)

            else :
                 self.assertEquals(True,False)
        self.selenium.close()

    def test_get(self):

        #self.selenium.get('%s%s' % (self.live_server_url, '/project/create/'))
        login(self,'/user/profile/interests/','siewml95@gmail.com', 'qwerty12')

        table = self.selenium.find_element_by_tag_name("table")
        tbody = table.find_element(By.TAG_NAME,"tbody")

        rows = tbody.find_elements(By.TAG_NAME, "tr")
        for index,row in enumerate(rows):
            cols = row.find_elements(By.TAG_NAME, "td")  # note: index start from 0, 1 is col 2
            href = cols[0].find_element(By.TAG_NAME,"a")
            if len(cols) >= 2 :
                 self.assertEquals(cols[0].text,self.users[index].first_name + self.users[index].last_name )
                 #self.assertEquals(href.get_attribute("href"),'%s%s' % (self.live_server_url, '/project/{}/update/'.format(project.id)))
                 self.assertEquals(cols[1].text,self.project.title)

            else :
                 self.assertEquals(True,False)
        self.selenium.close()


class ClientUserProfileProjectTest(LiveServerTestCase):
    @classmethod
    def setUp(cls):
        user = User.objects.create_user(email="siewml95@gmail.com",password="qwerty12")
        user.profile.type = 3
        user.profile.is_verified = True
        user.profile.save()
        cls.projects = []
        cls.organization = Organization.objects.create(title="UCL",status=True)
        cls.organization.save()
        for x in range(1,12):
            time.sleep(0.1)
            project = Project.objects.create(title="Test Project {}".format(x),summary="testing project",slug="test-project-{}".format(x),organization=cls.organization,created_by=user,deadline=datetime.datetime.now())
            cls.projects.append(project)
        print(cls.projects)
        cls.selenium = load_driver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()


    def test_pagination(self):

        print("pagination")
        #login(self,'/user/profile/projects/?page=2','siewml95@gmail.com', 'qwerty12')
        login(self,'/user/profile/projects/?page=2','siewml95@gmail.com', 'qwerty12')
        print("pageination2")
        table = self.selenium.find_element_by_tag_name("table")
        tbody = table.find_element(By.TAG_NAME,"tbody")

        rows = tbody.find_elements(By.TAG_NAME, "tr")
        for index,row in enumerate(rows):
            print(row)
            cols = row.find_elements(By.TAG_NAME, "td")  # note: index start from 0, 1 is col 2
            project = self.projects[0]
            href = cols[1].find_element(By.TAG_NAME,"a")
            if len(cols) >= 2 :
                  self.assertEquals(cols[1].text,project.title)
                  self.assertEquals(href.get_attribute("href"),'%s%s' % (self.live_server_url, '/project/{}/update/'.format(project.id)))
            else :
                 self.assertEquals(True,False)
        self.selenium.close()

    def test_get(self):

        #self.selenium.get('%s%s' % (self.live_server_url, '/project/create/'))
        login(self,'/user/profile/projects/','siewml95@gmail.com', 'qwerty12')

        table = self.selenium.find_element_by_tag_name("table")
        tbody = table.find_element(By.TAG_NAME,"tbody")

        rows = tbody.find_elements(By.TAG_NAME, "tr")
        for index,row in enumerate(rows):
            cols = row.find_elements(By.TAG_NAME, "td")  # note: index start from 0, 1 is col 2
            project = self.projects[10-index]
            href = cols[1].find_element(By.TAG_NAME,"a")
            print(href.get_attribute("href"))
            if len(cols) >= 2 :
                  print("cols " + cols[1].text)
                  self.assertEquals(cols[1].text,project.title)
                  self.assertEquals(href.get_attribute("href"),'%s%s' % (self.live_server_url, '/project/{}/update/'.format(project.id)))
            else :
                 self.assertEquals(True,False)
        self.selenium.close()
