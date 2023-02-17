import random
import time

import bcrypt


from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from openai_api import OpenaiApi


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
with app.app_context():
    db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    data_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<User %r>' % self.id


@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        exists = db.session.query(
            db.session.query(User).filter_by(username=username).exists()
        ).scalar()

        if not exists:
            new_user = User(username=username, password=hashed_password, email=email)
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect('/')
            except():
                return "error creating user"
        return "username already used"
    return render_template('sign_up.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        user_db_row = User.query.filter_by(username=username).first()

        if user_db_row:
            if bcrypt.checkpw(password, user_db_row.password):
                return f"Login successful as {user_db_row.username}"
            return "Wrong password"
        return "username not in db"
    return render_template('login.html')


@app.route('/guessing_game', methods=['POST', 'GET'])
def guessing_game():
    openai_api = OpenaiApi()
    answers = openai_api.get_a_list_of_answers("Give me 4 major events from prehistory.", 1, 1000)
    correct_answer = random.choice(answers)
    time.sleep(1)
    hints = openai_api.get_a_list_of_answers(f"Give me 5 hints about {correct_answer}.", 1, 1000)

    return render_template("guessing_game.html", answers=answers, correct_answer=correct_answer, hints=hints)


@app.route('/submit_guess/<string:user_answer>/<string:correct_answer>/<int:hints>', methods=['POST', 'GET'])
def submit_guess(user_answer, correct_answer, hints):
    if user_answer == correct_answer:
        return f"You won using {hints} hints!"
    return "You lose"


if __name__ == "__main__":
    app.run(debug=True)
