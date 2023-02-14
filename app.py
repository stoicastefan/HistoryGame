from datetime import datetime


import bcrypt as bcrypt
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
with app.app_context():
    db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    data_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<User %r>' % self.id


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        exists = db.session.query(
            db.session.query(User).filter_by(username=username).exists()
        ).scalar()

        if not exists:
            new_user = User(username=username, password=hashed_password)
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect('/')
            except():
                return "error creating user"
        else:
            return "username already used"

    else:
        return render_template('sign_in.html')


@app.route('/', methods=['POST', 'GET'])
def log_in():
    return "home page"



if __name__ == "__main__":
    app.run(debug=True)