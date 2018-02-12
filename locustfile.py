from locust import HttpLocust, TaskSet, task
import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (999999, 999999))


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def login(self):
        response = self.client.get('/user/login/')
        csrftoken = response.cookies['csrftoken']
        self.client.post('/user/login/',
                         {'email': 'siewml95@gmail.com', 'password': 'qwerty12'},
                         headers={'X-CSRFToken': csrftoken})
    @task
    def index(self):
        self.client.get("/")


    @task
    def profile(self):
      response = self.client.get("/user/profile/")
      csrftoken = response.cookies['csrftoken']
      self.client.post("/user/profile/",{"first_name":"siew"},headers={"X-CSRFToken": csrftoken})
class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 8000
    max_wait = 100000
