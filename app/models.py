from extensions import db

class Article(db.Model):
    guid = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    published_date = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    synopsis = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)

class ArticleQueue(db.Model):
    url = db.Column(db.String, unique=True, nullable=False)
    processed = db.Column(db.Boolean, default=False, nullable=False)
    guid = db.Column(db.String, unique=True, nullable=False, primary_key=True)

