# A Simple Python Starter

This is a Flask starter template aimed at novice Python programmers who want to build a web app that leverages a micro API in Python. It features a simple web page that showcases how to use Flask to construct an API and comes bundled with two sample programs:

- A "Hello, world!" program
- A pig Latin translator that takes user input

These examples can be deleted or substituted with your own code. This template is intended to serve as a launchpad for building Flask-based projects, as well as running normal scripts on the command line.

## Installation and Setup

1. If you don't have Python installed, [install it from here](https://www.python.org/downloads/)

2. Clone this repository

3. Navigate into the project directory

    ```bash
        cd simple-flask-starter
    ```

4. Create a new environment

    ```bash
        # MAC OS / Linux
        python3 -m venv venv
        . venv/bin/activate
    
        # WINDOWS OS
        py -3 -m venv venv
        venv\Scripts\activate
    ```

5. Install the requirements

    ```bash
        pip install -r requirements.txt
    ```

6. Run the ap

    ```bash
        flask run --debug
    ```

You should be able to access the app at [http://127.0.0.1:5000](http://127.0.0.1:5000).  Check out below for understanding what more about the code.

## Project Structure

```bash
    |--- app
    |   |--- handle_greeting.py
    |--- static
    |    |--- main.css
    |--- templates
    |    |--- index.html
    |--- .env
    |--- .gitignore
    |--- LICENSES
    |--- README.txt
    |--- requirements.txt
```

- `app/`: This directory can be used to add additional Python files for your Flask app.
  - `handle_greeting.py`: A sample file that handles the logic of the `/test` URI with a request and response object.
- `static/`: This directory contains static files used by the app, including:
  - `main.css`: Contains the CSS style for the app.
  - `main.js`: Contains the JavaScript behavior for the app.
- `templates/`: This directory contains the HTML templates for the app, including:
  - `index.html`: The index.html file is the primary HTML file that loads when you access the local host. It includes an input textarea for request data, along with a button that sends a POST request to the main.py file. The output is displayed in a response textarea.
- `.flaskenv`: A Flask environment file that contains variables to globally configure Flask.
- `.gitignore`: The default GitHub Python file that ignores basic runtime Python files that aren't needed.
- `LICENSES`: The license file that allows others to use and borrow code.
- `main.py`: This is the primary Python file for the Flask framework, responsible for rendering the index.html file and handling AJAX calls for any custom functionality you desire. It also contains the routing logic for URI GET and POST requests.
- `normal.py`: A Python file that can run normal Python scripts and accepts input and output results. It includes a sample program that can be removed.
- `README.txt`: The README file that summarizes the project, explains its purpose, and provides instructions on how to use it.
- `requirements.txt`: A file that contains the Flask dependency needed to run the simple Flask starter.

## Usage Instructions

- To run the Flask and use request and response and different API

    ```bash
        flask run
    ```

- To run a normal python script

    ```bash
         # MAC OS / Linux
        python3 normal.py
    
        # WINDOWS OS
        py -3 normal.py
    ```

    also may run from your favorite editor for debugging

## Learning about Structure

- [Learn to Manage Library Dependencies](https://learnpython.com/blog/python-requirements-file/)
- [Flask Quick Start](https://flask.palletsprojects.com/en/2.2.x/quickstart)
- [Application Flask Setup](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure)

## Sample Project Ideas for Learning

- **Guess the number**: Create a game where the user has to guess a random number between 1 and 100. The program should provide hints to the user to help them guess the number.

- **ToDo List**: Create a program that allows users to add tasks to a to-do list, mark them as completed, and delete them.

- **Rock, Paper, Scissors**: Create a game of rock, paper, scissors, where the user plays against the computer.

- **Calculator**: Create a basic calculator that allows users to perform basic arithmetic operations such as addition, subtraction, multiplication, and division.

- **Weather App**: Create a program that allows users to enter a location and receive the current weather conditions.

- **Hangman**: Create a game where the user has to guess a word by guessing one letter at a time. The user has a limited number of incorrect guesses before the game ends.

- **Word Count**: Create a program that counts the number of words in a text file.

- **Password Generator**: Create a program that generates a random password for the user.

- **Currency Converter**: Create a program that converts one currency to another.

- **Tic Tac Toe**: Create a game of tic tac toe, where the user plays against the computer.
