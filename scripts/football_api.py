# Simple Fantasy Football API Functions
import datetime
import nflgame
import random

def make_teams(num_teams):
	""" Randomly selects players for each team.

	:param num_teams: The number of teams needed.
	"""
	now = datetime.datetime.now()
	games = nflgame.games(now.year)
	players = nflgame.combine_game_stats(games)
	qbs = get_random_qb(num_teams, players)
	wrs = get_random_wrs(num_teams, players)
	rbs = get_random_rbs(num_teams, players)
	all_teams = []
	for i in range(num_teams):
		team = {}
		team["QB"] = qbs[i]
		team["WRs"] = wrs[i]
		team["RBs"] = rbs[i]
		all_teams.append(team)
	return all_teams

def get_random_qb(num_teams, players):
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

def trade_in_players(players):
	""" Randomly selects top players to replace the trade in players.

	:param players: The players to be traded in.
	"""
	print "a"

teams = make_teams(5)
i = 1
for team in teams:
	print "------------------------------------------"
	print "Team %i" % i
	for position in team:
		print position, team[position]
	i += 1
print "------------------------------------------"