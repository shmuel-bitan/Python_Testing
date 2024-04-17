import json
from flask import Flask, render_template, request, redirect, flash, url_for


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


@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    club_name = request.form['club']
    competition_name = request.form['competition']
    places_requested = int(request.form['places'])

    # Find the club and competition
    club = next((c for c in clubs if c['name'] == club_name), None)
    competition = next((comp for comp in competitions if comp['name'] == competition_name), None)

    # Check if club and competition exist
    if not (club and competition):
        flash("Invalid club or competition. Please try again.")
        return redirect(url_for('index'))

    # Check if the club has anough points ( issue 2)
    if int(club['points']) < places_requested:
        flash("Insufficient points to book places.")
        return redirect(url_for('index'))
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_requested

    flash('Booking successful!')
    return redirect(url_for('index'))


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
