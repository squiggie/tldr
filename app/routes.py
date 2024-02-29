from flask import render_template, jsonify, request, session, flash, redirect, url_for
from flask_login import current_user, login_required
from .forms import SignupForm, LoginForm
from .models import Article, Category, User
from extensions import db
from flask_login import login_user, login_required, logout_user
from flask_login import LoginManager

def init_app(app):
    login_manager = LoginManager(app)

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
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', session.get('per_page', 10), type=int)
        session['per_page'] = per_page
        category = Category.query.filter_by(name=category_name).first_or_404()
        articles = Article.query.filter_by(category_id=category.id).paginate(page=page, per_page=per_page, error_out=False)
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

    @app.route('/protected')
    @login_required
    def protected():
        return 'This is a protected view.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('index'))
        return render_template('login.html', title='Sign In', form=form)


