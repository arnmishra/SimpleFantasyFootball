from project import db

class Team(db.Model):
    """ Team Model with all data about a team. """
    id = db.Column(db.Integer, primary_key=True)
    league_name = db.Column(db.String)
    team_name = db.Column(db.String)
    qb1 = db.Column(db.PickleType)
    qb2 = db.Column(db.PickleType)
    wr1 = db.Column(db.PickleType)
    wr2 = db.Column(db.PickleType)
    wr3 = db.Column(db.PickleType)
    rb1 = db.Column(db.PickleType)
    rb2 = db.Column(db.PickleType)
    rb3 = db.Column(db.PickleType)
    starred_position = db.Column(db.String)
    this_week_score = db.Column(db.Integer)

    def __init__(self, league_name, team_name, starred_position):
        self.league_name = league_name
        self.team_name = team_name
        self.starred_position = starred_position
        self.this_week_score = 0

    def __repr__(self):
        return "<Team(league_name='%s', team_name='%s', qb1='%s', qb2='%s', wr1='%s', wr2='%s', wr3='%s', rb1='%s', \
            rb2='%s', rb3='%s', starred_position='%s', this_week_score='%d')>" \
               % (self.league_name, self.team_name, self.qb1, self.qb2, self.wr1, self.wr2, self.wr3, self.rb1, 
                self.rb2, self.rb3, self.starred_position, self.this_week_score)

class League(db.Model):
    """ League Model to store available players. """
    id = db.Column(db.Integer, primary_key=True)
    league_name = db.Column(db.String)
    available_qbs = db.Column(db.PickleType)
    available_wrs = db.Column(db.PickleType)
    available_rbs = db.Column(db.PickleType)

    def __init__(self, league_name):
        self.league_name = league_name

    def __repr__(self):
        return "<Team(league_name='%s', available_qbs='%s', available_wrs='%s', available_rbs='%s')>" \
               % (self.league_name, self.available_qbs, self.available_wrs, self.available_rbs)
