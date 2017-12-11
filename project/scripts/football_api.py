# Simple Fantasy Football API Functions
import datetime
import math
import nflgame
import random
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
    for week_num in range(17):       
       games = nflgame.games(2017, week=(week_num+1))      
       if len(games) == 0:     
           break
    return now.year, week_num


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

def get_high_scores(teams, expected_week_num):
    """ Return an ordered list of high scores for each team.

    :param teams: The information abou the teams.
    :return: A list of team names and scores.
    """
    for team in teams:
        get_player_scores(team, expected_week_num)
    high_scores = []
    for team in teams:
        high_scores.append([team.team_name, team.this_week_score])
    high_scores.sort()
    return high_scores

def get_player_scores(team, expected_week_num):
    """ Get scores of all players for current week.

    :param team: Team who's players' scores are being queried
    """    
    team.this_week_score = 0
    team.qb1 = update_live_player_score(team, team.qb1, expected_week_num)
    team.qb2 = update_live_player_score(team, team.qb2, expected_week_num)
    team.wr1 = update_live_player_score(team, team.wr1, expected_week_num)
    team.wr2 = update_live_player_score(team, team.wr2, expected_week_num)
    team.wr3 = update_live_player_score(team, team.wr3, expected_week_num)
    team.rb1 = update_live_player_score(team, team.rb1, expected_week_num)
    team.rb2 = update_live_player_score(team, team.rb2, expected_week_num)
    team.rb3 = update_live_player_score(team, team.rb3, expected_week_num)


def update_live_player_score(team, player, expected_week_num):
    """ Get Live Player Score for current week
    :param team: Team who's players' scores are being queried
    :param player: Player who's score is being queried
    :return: Player object with updated live score
    """
    year, week_num = get_year_week()
    player_score = 0
    if week_num == expected_week_num:
        player_obj = nflgame.find(player[0])[0]
        player_stats = player_obj.stats(year, week=week_num)
        player_score = get_player_score(player_stats)
    player = [player[0], player[1], [week_num, player_score]]
    team.this_week_score += player[2][1]
    return player


def get_player_score(player):
    """ Gets a player's score based on stats provided

    :param player: Player who's score is being queried
    :return: Player's Fantasy Score
    """
    return player.passing_yds * 0.04 + (player.rushing_yds + player.receiving_yds) * 0.1 \
        + player.passing_tds * 4 + (player.rushing_tds + player.receiving_tds) * 6 \
        - (player.passing_ints + player.fumbles_lost) * 2


def trade_in_players(team, game, trade_players, expected_week_num):
    """ Randomly selects top players to replace the trade in players.

    :param trade_players: The players to be traded in.
    :return: new random players to replace the traded players
    """
    players = get_players()
    for position in trade_players:
        if position == "qb1":
            team.qb1, game.available_qbs = trade_in(
                game.available_qbs, team.qb1, team, expected_week_num)
        elif position == "qb2":
            team.qb2, game.available_qbs = trade_in(
                game.available_qbs, team.qb2, team, expected_week_num)
        elif position == "wr1":
            team.wr1, game.available_wrs = trade_in(
                game.available_wrs, team.wr1, team, expected_week_num)
        elif position == "wr2":
            team.wr2, game.available_wrs = trade_in(
                game.available_wrs, team.wr2, team, expected_week_num)
        elif position == "wr3":
            team.wr3, game.available_wrs = trade_in(
                game.available_wrs, team.wr3, team, expected_week_num)
        elif position == "rb1":
            team.rb1, game.available_rbs = trade_in(
                game.available_rbs, team.rb1, team, expected_week_num)
        elif position == "rb2":
            team.rb2, game.available_rbs = trade_in(
                game.available_rbs, team.rb2, team, expected_week_num)
        elif position == "rb3":
            team.rb3, game.available_rbs = trade_in(
                game.available_rbs, team.rb3, team, expected_week_num)


def trade_in(top_player_stats, player, team, expected_week_num):
    """ Trade in an individual player with a new random player.

    :param top_player_stats: Information about an available top player.
    :param player: The current player who is being traded in.
    :return: the new player, the updated stats
    """
    new_player = random.choice(top_player_stats)
    top_player_stats.append(player)
    top_player_stats.remove(new_player)
    new_player = update_live_player_score(team, new_player, expected_week_num)
    return new_player, top_player_stats


def player_assignment(player, available_players):
    """ Confirms players are available in the data before assigning.

    Certain players, mostly rookies, are not available in the nflgame live json
    data, thus causing issues with live score calculation. 
    :param player: The player position being assigned.
    :param available_players: The available players to pick from. 
    """
    not_assigned = True
    while not_assigned:
        player = random.choice(available_players)
        try:
            nflgame.find(player[0])[0]
            not_assigned = False
        except:
            not_assigned = True
        available_players.remove(player)


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
            player_assignment(team.qb1, top_qb_stats)
        if not team.starred_position == "qb2":
            player_assignment(team.qb2, top_qb_stats)
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
            player_assignment(team.wr1, top_wr_stats)
        if not team.starred_position == "wr2":
            player_assignment(team.wr2, top_wr_stats)
        if not team.starred_position == "wr3":
            player_assignment(team.wr3, top_wr_stats)
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
            player_assignment(team.rb1, top_rb_stats)
        if not team.starred_position == "rb2":
            player_assignment(team.rb2, top_rb_stats)
        if not team.starred_position == "rb3":
            player_assignment(team.rb3, top_rb_stats)
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
