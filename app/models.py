from extensions import db

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON)
