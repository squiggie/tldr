from app import db
from sqlalchemy.dialects.postgresql import JSONB


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(JSONB)

    def __repr__(self):
        return '<Article {}>'.format(self.id)
