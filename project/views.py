import datetime
from project import app, db
from flask import render_template, url_for, request, redirect
from project.scripts.football_api import make_teams, trade_in_players

@app.route("/", methods=['GET'])
def index():
    """ Renders the home page

    :return: initialize business or home page
    """
    return render_template("index.html")

@app.route("/set_up_teams", methods=['GET', 'POST'])
def set_up_teams():
    """ Renders the home page

    :return: initialize business or home page
    """
    if request.method == "GET":
        redirect("/")
    num_teams = int(request.form["num_teams"])
    return render_template("set_up_teams.html", num_teams=num_teams)

@app.route("/view_teams", methods=['GET', 'POST'])
def view_teams():
    """ Renders the home page

    :return: initialize business or home page
    """
    if request.method == "GET":
        redirect("/")
    team_names = request.form.getlist("team_names")
    initial_teams = {}
    for team_name in team_names:
        initial_teams[team_name] = []
    teams = make_teams(initial_teams)
    print teams
    return render_template("view_teams.html", teams=teams)