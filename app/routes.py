from flask import render_template
from .models import Article

def init_app(app):
    @app.route("/", methods=("GET", "POST"))
    def index():
        articles = Article.query.all()
        print(articles)
        return render_template('index.html', articles=articles)