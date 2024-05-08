from locust import HttpUser, TaskSet, task


class UserBehavior(TaskSet):

    @task(1)
    def show_summary(self):
        email = "john@simplylift.co"  # Remplacez par un email existant pour le test
        response = self.client.post("/showSummary", data={"email": email})
        if response.status_code != 200:
            response.failure("Failed to load summary")

    @task(2)
    def book_competition(self):
        competition_name = "Spring Festival"
        club_name = "Simply Lift"
        response = self.client.get(f"/book/{competition_name}/{club_name}")
        if response.status_code != 200:
            response.failure("Failed to book competition")

    @task(3)
    def purchase_places(self):
        data = {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": 2
        }
        response = self.client.post("/purchasePlaces", data=data)
        if response.status_code != 200:
            response.failure("Failed to purchase places")

    @task(4)
    def points_views(self):
        self.client.get(f"/points")


class WebsiteUser(HttpUser):
    tasks = {UserBehavior: 1}
    min_wait = 2000  # Temps d'attente minimum entre les requêtes (en millisecondes)
    max_wait = 5000  # Temps d'attente maximum entre les requêtes (en millisecondes)
