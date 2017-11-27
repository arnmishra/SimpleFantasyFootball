# Simple Fantasy Football API Functions
import datetime
import nflgame
import random
from threading import Thread

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
	get_random_qbs(teams, players)
	get_random_wrs(teams, players)
	get_random_rbs(teams, players)

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

def get_random_qbs(teams, players):
	""" Randomly selects 1 top quarterbacks for each team.

	:param teams: The information about the teams.
	:param players: Stats on players this season
	"""
	top_qbs = str(players.passing().sort('passing_yds').limit(len(teams) * 4))
	top_qbs = top_qbs[1:-2].split(", ")
	for team in teams:
		if not team.starred_position == "qb1":
			qb1 = random.choice(top_qbs)
			team.qb1 = qb1
			top_qbs.remove(qb1)
		if not team.starred_position == "qb2":
			qb2 = random.choice(top_qbs)
			team.qb2 = qb2
			top_qbs.remove(qb2)

def get_random_wrs(teams, players):
	""" Randomly selects 2 top wide receivers for each team.

	:param teams: The information about the teams.
	:param players: Stats on players this season
	"""
	top_wrs = str(players.receiving().sort('receiving_yds').limit(len(teams) * 6))
	top_wrs = top_wrs[1:-1].split(", ")
	for team in teams:
		if not team.starred_position == "wr1":
			wr1 = random.choice(top_wrs)
			team.wr1 = wr1
			top_wrs.remove(wr1)
		if not team.starred_position == "wr2":
			wr2 = random.choice(top_wrs)
			team.wr2 = wr2
			top_wrs.remove(wr2)
		if not team.starred_position == "wr3":
			wr3 = random.choice(top_wrs)
			team.wr3 = wr3
			top_wrs.remove(wr3)

def get_random_rbs(teams, players):
	""" Randomly selects 2 top running backs for each team.

	:param teams: The information about the teams.
	:param players: Stats on players this season
	"""
	top_rbs = str(players.rushing().sort('rushing_yds').limit(len(teams) * 6))
	top_rbs = top_rbs[1:-1].split(", ")
	for team in teams:
		if not team.starred_position == "rb1":
			rb1 = random.choice(top_rbs)
			team.rb1 = rb1
			top_rbs.remove(rb1)
		if not team.starred_position == "rb2":
			rb2 = random.choice(top_rbs)
			team.rb2 = rb2
			top_rbs.remove(rb2)
		if not team.starred_position == "rb3":
			rb3 = random.choice(top_rbs)
			team.rb3 = rb3
			top_rbs.remove(rb3)

# teams = make_teams(5)
# i = 1
# for team in teams:
# 	print "------------------------------------------"
# 	print "Team %i" % i
# 	for position in team:
# 		print position, team[position]
# 	i += 1
# print "------------------------------------------"