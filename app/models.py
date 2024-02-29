from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Association tables
favorites = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('article_guid', db.String, db.ForeignKey('article.guid'), primary_key=True)
)

class Article(db.Model):
    guid = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    published_date = db.Column(db.String, nullable=False)
    added_date = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    synopsis = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class ArticleQueue(db.Model):
    url = db.Column(db.String, unique=True, nullable=False)
    processed = db.Column(db.Boolean, default=False, nullable=False)
    guid = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    articles = db.relationship('Article', backref='category', lazy=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String())
    favorite_articles = db.relationship('Article', secondary=favorites, backref=db.backref('liked_by', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
         return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User %r>' % self.username