from flask import Flask, render_template, redirect, request, url_for, flash, session
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
def home():
    return redirect(url_for("register"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('user_info', username=session['username']))
        
        
    form = RegistrationForm()
    if form.validate_on_submit():
        # ensuring the user is authenticated
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        # add to db 
        new_user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        
        return redirect(url_for('user_info', username=username))

    return render_template("index.html", form=form, action_url=url_for('register'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('user_info', username=session['username']))
    
    form = LoginForm()
    error = request.args.get('error')
    if form.validate_on_submit():
        # ensuring the user is authenticated
        username = form.username.data
        password = form.password.data
        # user = User.query.get_or_404(username, description="User not found")
        user = User.query.get(username)
        if user:
            # check if user + pass is in database and is correct 
            if user.password == password :
                session['username'] = user.username
                return redirect(url_for('user_info', username=username))
            else :
                return redirect(url_for('login', error="password incorrect"))
        else:
            return redirect(url_for('login', error="username not found"))
            
    return render_template("index.html", form=form ,action_url=url_for('login'), error=error)

@app.route('/users/<username>')
def user_info(username):    
    user = session.get('username')
    # atm any login user can view any user 
    if user:
        get_user = User.query.get_or_404(username, description="User not found")
        return render_template("user_info.html", user=get_user)
    return "Not allow"
    
@app.route('/logout')
def logout():
    # only delete username session
    session.pop('username', None)
    return redirect(url_for("home"))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', error=error), 404
    
if __name__ == '__main__':
    app.run(debug=True)