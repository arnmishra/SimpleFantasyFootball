# Simple Fantasy Football API Functions
import datetime
import math
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
	for week_num in range(17):
		games = nflgame.games(2017, week=(week_num+1))
		if len(games) == 0:
			break
	players = get_players()
	get_random_qbs(teams, players, week_num)
	get_random_wrs(teams, players, week_num)
	get_random_rbs(teams, players, week_num)

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

def get_random_qbs(teams, players, week_num):
	""" Randomly selects 1 top quarterbacks for each team.

	:param teams: The information about the teams.
	:param players: Stats on players this season
	"""
	top_qbs = players.passing().sort('passing_yds').limit(len(teams) * 4)
	top_qb_stats = []
	for qb in top_qbs:
		average_score = (qb.passing_yds*0.04 + qb.rushing_yds*0.01 + qb.passing_tds*4 + qb.rushing_tds*6 - qb.passing_int*2)/week_num
		top_qb_stats.append([qb, round(average_score,2)])
	for team in teams:
		if not team.starred_position == "qb1":
			qb1 = random.choice(top_qb_stats)
			# print qb1
			team.qb1 = qb1
			top_qb_stats.remove(qb1)
		if not team.starred_position == "qb2":
			qb2 = random.choice(top_qb_stats)
			team.qb2 = qb2
			top_qb_stats.remove(qb2)

def get_random_wrs(teams, players, week_num):
	""" Randomly selects 2 top wide receivers for each team.

	:param teams: The information about the teams.
	:param players: Stats on players this season
	"""
	top_wrs = players.receiving().sort('receiving_yds').limit(len(teams) * 6)
	top_wr_stats = []
	for wr in top_wrs:
		average_score = ((wr.receiving_yds+wr.rushing_yds)*0.1 + (wr.receiving_tds+wr.rushing_tds)*6 - wr.fumbles_lost*2)/week_num
		top_wr_stats.append([wr, round(average_score,2)])
	for team in teams:
		if not team.starred_position == "wr1":
			wr1 = random.choice(top_wr_stats)
			team.wr1 = wr1
			top_wr_stats.remove(wr1)
		if not team.starred_position == "wr2":
			wr2 = random.choice(top_wr_stats)
			team.wr2 = wr2
			top_wr_stats.remove(wr2)
		if not team.starred_position == "wr3":
			wr3 = random.choice(top_wr_stats)
			team.wr3 = wr3
			top_wr_stats.remove(wr3)

def get_random_rbs(teams, players, week_num):
	""" Randomly selects 2 top running backs for each team.

	:param teams: The information about the teams.
	:param players: Stats on players this season
	"""
	top_rbs = players.rushing().sort('rushing_yds').limit(len(teams) * 6)
	top_rb_stats = []
	for rb in top_rbs:
		average_score = ((rb.rushing_yds+rb.receiving_yds)*0.1 + (rb.rushing_tds+rb.receiving_tds)*6 - rb.fumbles_lost*2)/week_num
		top_rb_stats.append([rb, round(average_score,2)])
	for team in teams:
		if not team.starred_position == "rb1":
			rb1 = random.choice(top_rb_stats)
			team.rb1 = rb1
			top_rb_stats.remove(rb1)
		if not team.starred_position == "rb2":
			rb2 = random.choice(top_rb_stats)
			team.rb2 = rb2
			top_rb_stats.remove(rb2)
		if not team.starred_position == "rb3":
			rb3 = random.choice(top_rb_stats)
			team.rb3 = rb3
			top_rb_stats.remove(rb3)

# teams = make_teams(5)
# i = 1
# for team in teams:
# 	print "------------------------------------------"
# 	print "Team %i" % i
# 	for position in team:
# 		print position, team[position]
# 	i += 1
# print "------------------------------------------"