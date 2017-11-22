# Simple Fantasy Football API Functions
import datetime
import nflgame
import random

def get_players():
	""" Gets players with this year's combined stats

	:return: returns a list of the players
	"""
	now = datetime.datetime.now()
	games = nflgame.games(now.year)
	players = nflgame.combine_game_stats(games)
	return players

def make_teams(teams):
	""" Randomly selects players for each team.
	Keeps the starred player if there is one.

	:param teams: The information about the teams.
	"""
	players = get_players()
	qbs = get_random_qbs(num_teams, players)
	wrs = get_random_wrs(num_teams, players)
	rbs = get_random_rbs(num_teams, players)
	new_teams = []
	num_teams = len(teams)
	for i in range(num_teams):
		if len(teams[i]["starred"]) == 1:
			if "qb" in teams[i]["starred"]:
				qbs[i][0] = teams[i]["starred"]["qb"]
			if "wr" in teams[i]["starred"]:
				wrs[i][0] = teams[i]["starred"]["wr"]
			if "rb" in teams[i]["starred"]:
				rbs[i][0] = teams[i]["starred"]["rb"]
		team = {}
		team["QB"] = qbs[i]
		team["WRs"] = wrs[i]
		team["RBs"] = rbs[i]
		new_teams.append(team)
	return new_teams

def trade_in_players(trade_players):
	""" Randomly selects top players to replace the trade in players.

	:param trade_players: The players to be traded in.
	:return: new random players to replace the traded players
	"""
	players = get_players()
	new_players = {}
	for position in trade_players:
		if position == "qb":
			new_qbs = get_random_qbs(1, players)
			if len(trade_players["qbs"]) == 1:
				new_players["qb"] = new_qbs[0]
			else:
				new_players["qb"] = new_qbs
		elif position == "wr":
			new_wrs = get_random_wrs(1, players)
			if len(trade_players["wrs"]) == 1:
				new_players["wr"] = new_wrs[0]
			elif len(trade_players["wrs"]) == 2:
				new_players["wr"] = new_wrs[0:1]
			else:
				new_players["wr"] = new_wrs
		elif position == "rb":
			new_rbs = get_random_rbs(1, players)
			if len(trade_players["rbs"]) == 1:
				new_players["rb"] = new_rbs[0]
			elif len(trade_players["rbs"]) == 2:
				new_players["rb"] = new_rbs[0:1]
			else:
				new_players["rb"] = new_rbs
	return new_players

def get_random_qbs(num_teams, players):
	""" Randomly selects 1 top quarterbacks for each team.

	:param num_teams: The number of teams needed.
	:param players: Stats on players this season
	"""
	top_qbs = str(players.passing().sort('passing_yds').limit(num_teams * 4))
	top_qbs = top_qbs[1:-2].split(", ")
	qbs = []
	for i in range(num_teams):
		qb1 = random.choice(top_qbs)
		top_qbs.remove(qb1)
		qb2 = random.choice(top_qbs)
		top_qbs.remove(qb2)
		qbs.append([qb1, qb2])
	return qbs

def get_random_wrs(num_teams, players):
	""" Randomly selects 2 top wide receivers for each team.

	:param num_teams: The number of teams needed.
	:param players: Stats on players this season
	"""
	top_wrs = str(players.receiving().sort('receiving_yds').limit(num_teams * 6))
	top_wrs = top_wrs[1:-1].split(", ")
	wrs = []
	for i in range(num_teams):
		wr1 = random.choice(top_wrs)
		top_wrs.remove(wr1)
		wr2 = random.choice(top_wrs)
		top_wrs.remove(wr2)
		wr3 = random.choice(top_wrs)
		top_wrs.remove(wr3)
		wrs.append([wr1, wr2, wr3])
	return wrs

def get_random_rbs(num_teams, players):
	""" Randomly selects 2 top running backs for each team.

	:param num_teams: The number of teams needed.
	:param players: Stats on players this season
	"""
	top_rbs = str(players.rushing().sort('rushing_yds').limit(num_teams * 6))
	top_rbs = top_rbs[1:-1].split(", ")
	rbs = []
	for i in range(num_teams):
		rb1 = random.choice(top_rbs)
		top_rbs.remove(rb1)
		rb2 = random.choice(top_rbs)
		top_rbs.remove(rb2)
		rb3 = random.choice(top_rbs)
		top_rbs.remove(rb3)
		rbs.append([rb1, rb2, rb3])
	return rbs

teams = make_teams(5)
i = 1
for team in teams:
	print "------------------------------------------"
	print "Team %i" % i
	for position in team:
		print position, team[position]
	i += 1
print "------------------------------------------"