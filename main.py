from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


class Config(object):
    # Other configurations
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# when a request to base url happens (either GET or POST) return the index.html page


@app.route("/", methods=("GET", "POST"))
def index():
    # List of dummy articles
    articles = [
        {
            'title': 'First Article',
            'author': 'Author One',
            'summary': 'This is a summary of the first article.',
            'image_path': 'images/article1.jpg',
            'publish_date': '2024-02-01',
            'read_more_link': '#'
        },
        {
            'title': 'Second Article',
            'author': 'Author Two',
            'summary': 'This is a summary of the second article.',
            'image_path': 'images/article2.jpg',
            'publish_date': '2024-02-02',
            'read_more_link': '#'
        },
        {
            'title': 'Third Article',
            'author': 'Author Three',
            'summary': 'This is a summary of the third article.',
            'image_path': 'images/article3.jpg',
            'publish_date': '2024-02-03',
            'read_more_link': '#'
        }
    ]

    # Pass the articles list to the template
    return render_template('index.html', articles=articles)

# When a request to url /test happens
# and if the method is a POST then return a response


@app.route("/test", methods=("GET", "POST"))
def test():
    if request.method == "POST":
        # Take the Request JSON and serialize in a content variable
        content = request.get_json()
        app.logger.debug(content)

        # Logic for this POST request is handled in app/handle_greeting.py
        # and method handle_greeting
        greeting = handle_greeting(content)

        # return a JSON request with greeting equal to a string value
        response = jsonify(greeting)
    return response
