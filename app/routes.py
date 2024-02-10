from flask import render_template
from .models import Article  # Import your models as needed

def init_app(app):
    @app.route("/", methods=("GET", "POST"))
    def index():
        articles = Article.query.all()
        print(articles)
        return render_template('index.html', articles=articles)