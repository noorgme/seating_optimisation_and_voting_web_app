from app import db

class User(db.Model):
    email = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    convey_guru = db.Column(db.Integer, default=0)
    ekai = db.Column(db.Integer, default=0)
    fluenio = db.Column(db.Integer, default=0)
    guliva = db.Column(db.Integer, default=0)
    hitcoach = db.Column(db.Integer, default=0)
    hybridcredit = db.Column(db.Integer, default=0)
    matrx = db.Column(db.Integer, default=0)
    neutrally = db.Column(db.Integer, default=0)
    omniabiosystems = db.Column(db.Integer, default=0)
    presalesai = db.Column(db.Integer, default=0)
    propx = db.Column(db.Integer, default=0)
    roma = db.Column(db.Integer, default=0)
    round_1 = db.Column(db.Integer, nullable = True)
    round_2 = db.Column(db.Integer, nullable = True)
    round_3 = db.Column(db.Integer, nullable = True)
    
    def __repr__(self):
        return '<User %r>' % self.email
