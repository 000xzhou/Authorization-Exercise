from flask import Flask, render_template, redirect, request, url_for, flash
from models import db, connect_db, User
from dotenv import load_dotenv
load_dotenv()
import os


app = Flask(__name__)
secret_key = os.environ.get('SECRET_KEY')
database_uri = os.environ.get('DATABASE_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.secret_key = secret_key

connect_db(app)
with app.app_context():
    db.create_all()

# -------------------forms --------------------
from forms import RegistrationForm,LoginForm

@app.route('/')
def homepage():
    return redirect(url_for("register"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # ensuring the user is authenticated
        return redirect(url_for('secret'))
    return render_template("index.html", form=form, action_url=url_for('register'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # ensuring the user is authenticated
        return redirect(url_for('secret'))
    return render_template("index.html", form=form ,action_url=url_for('login'))

@app.route('/secret')
def secret():
    return "Registration successful!"
    
if __name__ == '__main__':
    app.run(debug=True)