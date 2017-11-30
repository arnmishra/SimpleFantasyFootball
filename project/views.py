import datetime
from project import app, db
from models import Team, Game
from flask import render_template, url_for, request, redirect
from project.scripts.football_api import make_teams, trade_in_players, get_games, get_player_scores

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

@app.route("/view_all_teams", methods=['GET', 'POST'])
def view_all_teams():
    """ Renders a view of the players on every team

    :return: view_all_teams
    """
    if request.method == "GET":
        redirect("/")
    team_names = request.form.getlist("team_names")
    game_name = request.form["game_name"]
    teams = []
    game = Game.query.filter_by(game_name=game_name).first()
    if not game:
        game = Game(game_name)
        db.session.add(game)
    for team_name in team_names:
        team = Team.query.filter_by(team_name=team_name).first()
        if not team:
            team = Team(game_name, team_name, "None")
            db.session.add(team)
        teams.append(team)
    make_teams(teams, game)
    db.session.commit()

    """
        Return all this week's games
    """
    games = get_games(13)
    print games
    return render_template("view_all_teams.html", game_name=game_name, teams=teams, games=games)

@app.route("/team/<game_name>/<team_name>", methods=['GET', 'POST'])
def view_team(game_name, team_name):
    """ Renders a page with only your team and their scores

    :return: view_team.html
    """
    team = Team.query.filter_by(game_name=game_name, team_name=team_name).first()
    game = Game.query.filter_by(game_name=game_name).first()
    if request.method == 'POST':
        if "star" in request.form:
            team.starred_position = request.form["star"]
        if "trade_players" in request.form:
            trade_players = request.form.getlist("trade_players")
            trade_in_players(team, game, trade_players)
    if request.method == 'GET':
        get_player_scores(team)
    db.session.commit()
    return render_template("view_team.html", team=team, game_name=game_name)
