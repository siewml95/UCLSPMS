from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        #self.login()

    def post_profile(self):
          response = self.client.get("/user/profile/")
          csrftoken = response.cookies['csrftoken']

          self.client.post("/user/profile/",{"first_name":"siew"},headers={"X-CSRFToken": csrftoken})

    @task
    def index(self):
        self.client.get("/")


    @task
    def profile(self):
     ''' response = self.client.get("/user/profile/")
      csrftoken = response.cookies['csrftoken']

      self.client.post("/user/profile/",{"first_name":"siew"},headers={"X-CSRFToken": csrftoken})'''
      self.post_profile()
class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
