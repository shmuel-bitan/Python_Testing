import server
from server import app


class TestDeductClubPoints:
    client = app.test_client()
    competition = [
        {
            "name": "Test",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        }
    ]

    club = [
        {
            "name": "Test club",
            "email": "test_club@email.com",
            "points": "10"
        }
    ]

    def setup_method(self):
        server.competitions = self.competition
        server.clubs = self.club

    def test_deduct_points(self):
        club_points_before = int(self.club[0]["points"])
        places_booked = 3

        result = self.client.post(
            "/purchasePlaces",
            data={
                "places": places_booked,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }, follow_redirects=True
        )

        points_after = int(self.club[0]["points"])
        assert points_after == club_points_before - places_booked, "Points deduction is incorrect"
        assert b"Great-booking complete!" in result.data
        assert int(self.club[0]["points"]) == club_points_before - places_booked

    def test_empty_field(self):
        places_booked = ""  # Empty string for places_booked

        result = self.client.post(
            "/purchasePlaces",
            data={
                "places": places_booked,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            },
            follow_redirects=True  # Ensure we follow redirects
        )

        assert result.status_code == 200
        assert b"Please enter a valid number of places." in result.data
