from flask import render_template, jsonify, request, session, flash, redirect, url_for
from .forms import SignupForm, LoginForm
from .models import Article, Category, User
from extensions import db
from flask_login import login_user, login_required, logout_user, LoginManager, current_user, login_required

def init_app(app):
    @app.route("/", methods=("GET", "POST"))
    def index():
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', session.get('per_page', 10), type=int)
        session['per_page'] = per_page
        articles = Article.query.order_by(Article.added_date.desc()).paginate(page=page, per_page=per_page, error_out=False)
        if current_user.is_authenticated:
            favorite_articles = [article.id for article in current_user.favorite_articles]
            return render_template('index.html', articles=articles, pagination=articles, favorite_articles=favorite_articles)
        return render_template('index.html', articles=articles, pagination=articles)

    
    @app.route("/articles/newest/", methods=("GET",))
    def newest_articles():
        id = request.args.get('id')
        article = Article.query.get(id)
        last_date = article.added_date
        articles = Article.query.filter(Article.added_date > last_date).all()
        dict = [article.as_dict() for article in articles]
        return jsonify(dict)

    @app.route('/category/<category_name>')
    def category_page(category_name):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', session.get('per_page', 10), type=int)
        session['per_page'] = per_page
        category = Category.query.filter_by(name=category_name).first_or_404()
        articles = Article.query.filter_by(category_id=category.id).order_by(Article.added_date.desc()).paginate(page=page, per_page=per_page, error_out=False)
        if current_user.is_authenticated:
            favorite_articles = [article.id for article in current_user.favorite_articles]
            return render_template('category.html', category=category, articles=articles.items, pagination=articles, favorite_articles=favorite_articles)
        return render_template('category.html', category=category, articles=articles.items, pagination=articles)

    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        form = SignupForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        return render_template('signup.html', title='Sign Up', form=form)

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('index'))
        return render_template('login.html', title='Sign In', form=form)

    @app.route('/save_article/<article_id>')
    @login_required
    def save_article(article_id):
        article = Article.query.filter_by(id=article_id).first_or_404()
        if article in current_user.favorite_articles:
            flash('This article is already in your saved list.')
        else:
            current_user.favorite_articles.append(article)
            db.session.commit()
            flash('Article saved for later!')
        return redirect(url_for('index'))

