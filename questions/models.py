from questions import db

class Answer(db.Model):
        __tablename__ = 'answers'
        id = db.Column(db.Integer, primary_key=True)
        q1 = db.Column(db.Integer)
        q2 = db.Column(db.Integer)
        type1 = db.Column(db.Text)
        q3 = db.Column(db.Integer)
        q4 = db.Column(db.Integer)
        type2 = db.Column(db.Text)
        q5 = db.Column(db.Integer)
        q6 = db.Column(db.Integer)

def init():
    db.create_all()
