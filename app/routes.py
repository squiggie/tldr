from flask import render_template, jsonify, request
from .models import Article, Category

def init_app(app):
    @app.route("/", methods=("GET", "POST"))
    def index():
        # Retrieve the latest 100 articles from the database
        articles = Article.query.order_by(Article.added_date.desc()).limit(100).all()
        return render_template('index.html', articles=articles)
    
    @app.route("/articles/newest/", methods=("GET",))
    def newest_articles():
        guid = request.args.get('guid')
        article = Article.query.get(guid)
        last_date = article.added_date
        articles = Article.query.filter(Article.added_date > last_date).all()
        dict = [article.as_dict() for article in articles]
        return jsonify(dict)

    @app.route('/category/<category_name>')
    def category_page(category_name):
        category = Category.query.filter_by(name=category_name).first_or_404()
        articles = Article.query.filter_by(category_id=category.id).all()
        return render_template('category.html', category=category, articles=articles)