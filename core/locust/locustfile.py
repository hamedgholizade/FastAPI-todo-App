from locust import HttpUser, task, between


class QuickStartUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        response = self.client.post(
            "/users/login",
            json={"username": "hamed", "password": "H@med4471"}
            )
        access_token = response.json()["access"]
        self.client.headers = {"Authorization": f"Bearer {access_token}"}

    @task
    def get_list_tasks(self):
        self.client.get("/todo/tasks")

    @task
    def fetch_weather(self):
        self.client.get("/fetch-current-weather")

    @task
    def send_mail(self):
        self.client.get("/test-send-mail")

    @task
    def initiate_task(self):
        self.client.get("/initiate-task")

    @task
    def not_found(self):
        self.client.get("/not_found")
