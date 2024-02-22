from extensions import db

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
