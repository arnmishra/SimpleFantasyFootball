from project import db

class Team(db.Model):
    """ Team Model with all data about a team. """
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String)
    team_name = db.Column(db.String)
    qb1 = db.Column(db.String)
    qb2 = db.Column(db.String)
    wr1 = db.Column(db.String)
    wr2 = db.Column(db.String)
    wr3 = db.Column(db.String)
    rb1 = db.Column(db.String)
    rb2 = db.Column(db.String)
    rb3 = db.Column(db.String)
    starred_position = db.Column(db.String)

    def __init__(self, game_name, team_name, starred_position):
        self.game_name = game_name
        self.team_name = team_name
        self.starred_position = starred_position

    def __repr__(self):
        return "<Team(game_name='%s', team_name='%s', qb1='%s', qb2='%s', wr1='%s', wr2='%s', wr3='%s', rb1='%s', \
            rb2='%d', rb3='%s', starred_position='%s')>" \
               % (self.game_name, self.team_name, self.qb1, self.qb2, self.wr1, self.wr2, self.wr3, self.rb1, 
                self.rb2, self.rb3, self.starred_position)

class Player(db.Model):
    """ Player Model stores data about specific players. """
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String)
    player_name = db.Column(db.String)
    average_score = db.Column(db.String)
    opposing_team = db.Column(db.String)

    def __init__(self, owner, player_name, average_score, opposing_team):
        self.owner = owner
        self.player_name = player_name
        self.average_score = average_score
        self.opposing_team = opposing_team

    def __repr__(self):
        return "<Player(owner='%s', player_name='%s', average_score='%s', opposing_team='%s')>" \
               % (self.owner, self.player_name, self.average_score, self.opposing_team)