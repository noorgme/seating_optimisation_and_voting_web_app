from app import db

class User(db.Model):
    email = db.Column(db.String(120), primary_key=True)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email
