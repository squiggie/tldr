from flask import Flask, request, jsonify, render_template
from app.handle_greeting import handle_greeting

app = Flask(__name__)

# when a request to base url happens (either GET or POST) return the index.html page
@app.route("/", methods=("GET", "POST"))
def index():
    return render_template("index.html")

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