import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['GET', 'POST'])
def showSummary():
    email = request.form.get('email')
    club = next((c for c in clubs if c['email'] == email), None)

    if not club:
        flash('Invalid email or password. Please try again.', 'error')
        return redirect(url_for('index'))

    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)

    if not (foundClub and foundCompetition):
        flash("Invalid club or competition. Please try again.")
        return redirect(url_for('index'))

    competition_datetime = datetime.strptime(foundCompetition['date'], '%Y-%m-%d %H:%M:%S')
    if competition_datetime < datetime.now():
        flash("You cannot book places for a past competition.")
        return redirect(url_for('index'))

    return render_template('booking.html', club=foundClub, competition=foundCompetition)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    club_name = request.form.get('club')
    competition_name = request.form.get('competition')
    places_requested = request.form.get('places')

    if not places_requested or not places_requested.isdigit():
        flash("Please enter a valid number of places.")
        return redirect(url_for('index'))

    places_requested = int(places_requested)

    club = next((c for c in clubs if c['name'] == club_name), None)
    competition = next((c for c in competitions if c['name'] == competition_name), None)

    if not (club and competition):
        flash("Invalid club or competition. Please try again.")
        return redirect(url_for('index'))

    if places_requested > 12:
        flash("You cannot book more than 12 places at once.")
        return redirect(url_for('index'))

    if places_requested > int(club['points']):
        flash("Insufficient points to book places.")
        return redirect(url_for('index'))

    if places_requested > int(competition['numberOfPlaces']):
        flash("Insufficient places available for booking.")
        return redirect(url_for('index'))

    club['points'] = int(club['points']) - places_requested
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_requested

    flash('Great-booking complete!')
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


@app.route('/points')
def display_points():
    club_points = [{"name": club['name'], "points": int(club['points'])} for club in clubs]
    return render_template('points_display.html', club_points=club_points)


if __name__ == "__main__":
    app.run(debug=True)
