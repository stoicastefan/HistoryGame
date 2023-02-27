# importing the required modules
import random
import time
import bcrypt
from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from openai_api import OpenaiApi

# creating a Flask web application
app = Flask(__name__)

# configuring database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
with app.app_context():
    db = SQLAlchemy(app)

# Defining a database model for the user
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    data_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<User %r>' % self.id

# Defining a route for sign up page
@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == "POST":
        # Getting user input
        username = request.form['username']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        # Checking if the username and email already exist in the database
        username_exists = db.session.query(
            db.session.query(User).filter_by(username=username).exists()
        ).scalar()
        email_exists = db.session.query(
            db.session.query(User).filter_by(email=email).exists()
        ).scalar()

        # If the username and email do not exist in the database, create a new user
        if not username_exists:
            if not email_exists:
                new_user = User(username=username, password=hashed_password, email=email)
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    return redirect('/select_period')
                except():
                    return "error creating user"
            return render_template('sign_up.html', error="Email already used.")
        return render_template('sign_up.html', error="Username already used.")
    return render_template('sign_up.html')

# Defining a route for login page
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        # Getting user input
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        # Retrieving the user data from the database
        user_db_row = User.query.filter_by(username=username).first()

        # if the username exists in the database, check if the password is correct
        if user_db_row:
            if bcrypt.checkpw(password, user_db_row.password):
                return redirect('/select_period')       # TODO set user_db_row.username in cookies
            return render_template('login.html', error="Wrong password!")
        return render_template('login.html', error="Username not existing!")

    return render_template('login.html')

# defining a route for the guessing game page
@app.route('/guessing_game')
def guessing_game():
    # Creating an instance of the OpenaiApi class
    openai_api = OpenaiApi()
    # Generating a list of answers to the prompt using the OpenAI API
    answers = openai_api.get_a_list_of_answers(
        "Give me 4 major events from ancient history without mentioning the period of the event.",
        1,
        1000
    )
    # Selecting one of the answers as the correct answer for the game
    correct_answer = random.choice(answers).strip()
    # Sleeping for 1 second to avoid hitting the OpenAI API rate limit
    time.sleep(1)
    # Getting hints for the selected answer from the API
    hints = openai_api.get_a_list_of_answers(
        f"Give me 5 hints about {correct_answer} without mentioning '{correct_answer}'.", 1, 1000)
    # rendering the 'guessing_game.html' template and passing the list of answers, the correct answer, and the hints
    return render_template("guessing_game.html", answers=answers, correct_answer=correct_answer, hints=hints)


@app.route('/submit_guess/<string:user_answer>/<string:correct_answer>/<int:hints>', methods=['POST', 'GET'])
def submit_guess(user_answer, correct_answer, hints):
    # checking if the user's answer matches the correct answer
    if user_answer == correct_answer:
        # Rendering the 'win.html' template and passing the number of hints as a parameter
        return render_template('win.html', hints=hints)
    # if the user's answer does not match the correct answer, rendering the 'lose.html' template
    return render_template('lose.html')


@app.route('/selectTypeGame', methods=['POST', 'GET'])
def select_type_game():
    # rendering the 'selectTypeGame.html' template
    return render_template('selectTypeGame.html')


@app.route('/select_period', methods=['POST', 'GET'])
def select_period():
    # rendering the 'select_period.html' template
    return render_template('select_period.html')


if __name__ == "__main__":
    # starting the Flask application with debug mode enabled
    app.run(debug=True)