# Simple Fantasy Football API Functions
import datetime
import math
import nflgame
import random
from threading import Thread
import json


def get_players():
    """ Gets players with this year's combined stats

    :return: returns a list of the players
    """
    year, week_num = get_year_week()
    games = nflgame.games(year)
    players = nflgame.combine_game_stats(games)
    return players


def get_year_week():
    """ Get current NFL Year and Week """
    now = datetime.datetime.now()
    return now.year, 13


def make_teams(teams, game):
    """ Randomly selects players for each team.
    Keeps the starred player if there is one.

    :param teams: The information about the teams.
    :param game: The game object
    """
    year, week_num = get_year_week()
    players = get_players()
    top_qb_stats = get_random_qbs(teams, players, week_num)
    top_wr_stats = get_random_wrs(teams, players, week_num)
    top_rb_stats = get_random_rbs(teams, players, week_num)
    game.available_qbs = top_qb_stats
    game.available_wrs = top_wr_stats
    game.available_rbs = top_rb_stats


def get_player_scores(team):
    """ Get scores of all players for current week.

    :param team: Team who's players' scores are being queried
    """
    team.qb1 = update_live_player_score(team.qb1)
    team.qb2 = update_live_player_score(team.qb2)
    team.wr1 = update_live_player_score(team.wr1)
    team.wr2 = update_live_player_score(team.wr2)
    team.wr3 = update_live_player_score(team.wr3)
    team.rb1 = update_live_player_score(team.rb1)
    team.rb2 = update_live_player_score(team.rb2)
    team.rb3 = update_live_player_score(team.rb3)


def update_live_player_score(player):
    """ Get Live Player Score for current week

    :param player: Player who's score is being queried
    :return: Player object with updated live score
    """
    year, week_num = get_year_week()
    player_obj = nflgame.find(player[0])[0]
    player_stats = player_obj.stats(year, week=week_num)
    player = [player[0], player[1], [week_num, get_player_score(player_stats)]]
    return player


def get_player_score(player):
    """ Gets a player's score based on stats provided

    :param player: Player who's score is being queried
    :return: Player's Fantasy Score
    """
    return player.passing_yds * 0.04 + (player.rushing_yds + player.receiving_yds) * 0.1 \
        + player.passing_tds * 4 + (player.rushing_tds + player.receiving_tds) * 6 \
        - (player.passing_int + player.fumbles_lost) * 2


def trade_in_players(team, game, trade_players):
    """ Randomly selects top players to replace the trade in players.

    :param trade_players: The players to be traded in.
    :return: new random players to replace the traded players
    """
    players = get_players()
    for position in trade_players:
        if position == "qb1":
            team.qb1, game.available_qbs = trade_in(
                game.available_qbs, team.qb1)
        elif position == "qb2":
            team.qb2, game.available_qbs = trade_in(
                game.available_qbs, team.qb2)
        elif position == "wr1":
            team.wr1, game.available_wrs = trade_in(
                game.available_wrs, team.wr1)
        elif position == "wr2":
            team.wr2, game.available_wrs = trade_in(
                game.available_wrs, team.wr2)
        elif position == "wr3":
            team.wr3, game.available_wrs = trade_in(
                game.available_wrs, team.wr3)
        elif position == "rb1":
            team.rb1, game.available_rbs = trade_in(
                game.available_rbs, team.rb1)
        elif position == "rb2":
            team.rb2, game.available_rbs = trade_in(
                game.available_rbs, team.rb2)
        elif position == "rb3":
            team.rb3, game.available_rbs = trade_in(
                game.available_rbs, team.rb3)


def trade_in(top_player_stats, player):
    """ Trade in an individual player with a new random player.

    :param top_player_stats: Information about an available top player.
    :param player: The current player who is being traded in.
    :return: the new player, the updated stats
    """
    new_player = random.choice(top_player_stats)
    top_player_stats.append(player)
    top_player_stats.remove(new_player)
    new_player = update_live_player_score(new_player)
    return new_player, top_player_stats


def get_random_qbs(teams, players, week_num):
    """ Randomly selects 1 top quarterbacks for each team.

    :param teams: The information about the teams.
    :param players: Stats on players this season
    """
    top_qbs = players.passing().sort('passing_yds').limit(len(teams) * 4)
    top_qb_stats = []
    for qb in top_qbs:
        average_score = get_player_score(qb) / week_num

        name = qb.player
        if qb.player is None:
            name = qb
        else:
            name = qb.player.full_name

        top_qb_stats.append([name, round(average_score, 2)])

    for team in teams:
        if not team.starred_position == "qb1":
            qb1 = random.choice(top_qb_stats)
            team.qb1 = qb1
            top_qb_stats.remove(qb1)
        if not team.starred_position == "qb2":
            qb2 = random.choice(top_qb_stats)
            team.qb2 = qb2
            top_qb_stats.remove(qb2)
    return top_qb_stats


def get_random_wrs(teams, players, week_num):
    """ Randomly selects 2 top wide receivers for each team.

    :param teams: The information about the teams.
    :param players: Stats on players this season
    """
    top_wrs = players.receiving().sort('receiving_yds').limit(len(teams) * 6)
    top_wr_stats = []
    for wr in top_wrs:
        average_score = get_player_score(wr) / week_num
        name = wr.player
        if wr.player is None:
            name = wr
        else:
            name = wr.player.full_name

        top_wr_stats.append([name, round(average_score, 2)])
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
    return top_wr_stats


def get_random_rbs(teams, players, week_num):
    """ Randomly selects 2 top running backs for each team.

    :param teams: The information about the teams.
    :param players: Stats on players this season
    """
    top_rbs = players.rushing().sort('rushing_yds').limit(len(teams) * 6)
    top_rb_stats = []
    for rb in top_rbs:
        average_score = get_player_score(rb) / week_num
        name = rb.player
        if rb.player is None:
            name = rb
        else:
            name = rb.player.full_name

        top_rb_stats.append([name, round(average_score, 2)])
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
    return top_rb_stats


def get_games(week_num):
    data = json.load(open('./project/scripts/schedule.json'))
    curr_week_games = []
    for g in range(len(data['games'])):
		if data['games'][g][1]['week'] == week_num and data['games'][g][1]['year'] == 2017:
			curr_week_games.append(data['games'][g][1])
    return curr_week_games

    # teams = make_teams(5)
    # i = 1
    # for team in teams:
    # 	print "------------------------------------------"
    # 	print "Team %i" % i
    # 	for position in team:
    # 		print position, team[position]
    # 	i += 1
    # print "------------------------------------------"
