from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(5, 15)
    
    def on_start(self):
        self.client.post("http://localhost:8000/", {
            "username": "",
            "password": ""
        })
    
    @task
    def index(self):
        self.client.get("http://localhost:8000/")

    @task
    def elemets(self):
        self.client.get("http://localhost:8000/elements/42")