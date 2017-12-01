import datetime
from project import app, db
from models import Team, League
from flask import render_template, url_for, request, redirect
from project.scripts.football_api import make_teams, trade_in_players, get_games, get_player_scores, get_high_scores

@app.route("/", methods=['GET'])
def index():
    """ Renders the home page

    :return: index.html
    """
    return render_template("index.html")

@app.route("/set_up_new_game", methods=['GET'])
def set_up_new_game():
    """ Renders a page to set up a new game

    :return: index.html
    """
    return render_template("set_up_new_game.html")

@app.route("/set_up_teams", methods=['GET', 'POST'])
def set_up_teams():
    """ Renders a form to submit team names

    :return: set_up_teams.html
    """
    if request.method == "GET":
        redirect("/")
    num_teams = int(request.form["num_teams"])
    return render_template("set_up_teams.html", num_teams=num_teams)

@app.route('/view_all_teams', defaults={'league_name': None}, methods=['GET', 'POST'])
@app.route("/view_all_teams/<league_name>", methods=['GET', 'POST'])
def view_all_teams(league_name):
    """ Renders a view of the players on every team

    :return: view_all_teams
    """
    if request.method == "GET":
        redirect("/")
    if "team_names" in request.form:
        team_names = request.form.getlist("team_names")
    else:
        team_names = []
    if "league_name" in request.form:
        league_name = request.form["league_name"]
    teams = []
    league = League.query.filter_by(league_name=league_name).first()
    new_league = False
    if not league:
        league = League(league_name)
        db.session.add(league)
        new_league = True
    for team_name in team_names:
        team = Team.query.filter_by(team_name=team_name).first()
        if not team:
            team = Team(league_name, team_name, "None")
            db.session.add(team)
        teams.append(team)
    if new_league:
        make_teams(teams, league)
    else:
        teams = Team.query.filter_by(league_name=league_name).all()
    db.session.commit()

    """
        Return all this week's games
    """
    games = get_games(13)
    high_scores = get_high_scores(teams)
    return render_template("view_all_teams.html", league_name=league_name, teams=teams, games=games, high_scores=high_scores)

@app.route("/team/<league_name>/<team_name>", methods=['GET', 'POST'])
def view_team(league_name, team_name):
    """ Renders a page with only your team and their scores

    :return: view_team.html
    """
    team = Team.query.filter_by(league_name=league_name, team_name=team_name).first()
    league = League.query.filter_by(league_name=league_name).first()
    if request.method == 'POST':
        if "star" in request.form:
            team.starred_position = request.form["star"]
        if "trade_players" in request.form:
            trade_players = request.form.getlist("trade_players")
            trade_in_players(team, league, trade_players)
    if request.method == 'GET':
        get_player_scores(team)
    db.session.commit()
    return render_template("view_team.html", team=team, league_name=league_name)

@app.route("/view_existing_league", methods=['POST'])
def view_existing_league():
    """ Redirects to an existing page with league info

    :return: view_all_teams.html
    """
    league_name = request.form["league_name"]
    return redirect("/view_all_teams/" + league_name)