import server
from server import app

class TestMorePointsThanAllowed:
    # Initialisation du client de test
    client = app.test_client()

    # Données de test pour la compétition et le club
    competition = [
        {
            "name": "Test",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": 25
        }
    ]
    club = [
        {
            "name": "Test club",
            "email": "test_club@email.com",
            "points": 10
        }
    ]

    def setup_method(self):
        # Configuration des données de test dans le serveur
        server.competitions = self.competition
        server.clubs = self.club

    def test_points_within_allowed(self):
        # Envoyer une requête POST pour acheter un nombre de places valide
        self.client.post(
            "/purchasePlaces",
            data={
                "places": 5,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        # Vérifier que le nombre de points du club reste positif ou nul après l'achat
        assert int(self.club[0]["points"]) >= 0

    def test_more_points_than_allowed(self):
        # Envoyer une requête POST pour acheter un nombre de places supérieur aux points du club
        self.client.post(
            "/purchasePlaces",
            data={
                "places": 100,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        # Vérifier que le nombre de points du club reste positif ou nul après l'achat
        assert int(self.club[0]["points"]) >= 0


