from flask import Flask, render_template, redirect, request, url_for, flash, session, abort
from models import db, connect_db, User, Feedback
from sqlalchemy.exc import IntegrityError
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
from forms import RegistrationForm,LoginForm,FeedbackForm

@app.route('/')
def home():
    get_feedback = Feedback.query.all()
    
    return render_template("index.html", feedbacks=get_feedback )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for("home"))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        # ensuring the user is authenticated
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        # add to db 
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            # Add an error message to the form
            form.username.errors.append('Username or email taken, please pick another')
            return render_template('registerNlogin.html', form=form, action_url=url_for('register'))
        session['username'] = new_user.username
        
        return redirect(url_for('user_info', username=new_user.username))

    return render_template("registerNlogin.html", form=form, action_url=url_for('register'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for("home"))

    form = LoginForm()
    error = request.args.get('error')
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # ensuring the user is authenticated
        user, error_message = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(url_for('user_info', username=username))
        else:
            if error_message == "Wrong password":
                form.password.errors = ["Wrong password"]
            elif error_message == "User does not exist":
                form.username.errors = ["User does not exist"]
            else:
                form.username.errors = ["Unknown error"]
            
    return render_template("registerNlogin.html", form=form ,action_url=url_for('login'), error=error)

@app.route('/users/<username>')
def user_info(username):    
    user = session.get('username')
    if user: 
        get_user = User.query.get_or_404(username, description="User not found")
        get_feedback = Feedback.query.filter_by(username=user)
        return render_template("user_info.html", user=get_user, feedbacks=get_feedback)
    redirect(url_for("home"))
    
@app.route('/logout')
def logout():
    # only delete username session
    session.pop('username', None)
    return redirect(url_for("home"))

@app.route('/users/<username>/delete')
def delete_username(username):
    # delete user 
    user = session.get('username')
    # if you enter your own link 
    if user != username: 
        return redirect(url_for("home")) 
    # only can delete your own acount
    get_user = User.query.get_or_404(username)
    if get_user.username == user:
        db.session.delete(get_user)
        db.session.commit()
        session.pop('username', None)
    return redirect(url_for("home"))
    

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    user = session.get('username')
    if user != username: 
        flash("can't submit for other users")
        return redirect(url_for("home")) 
    
    form = FeedbackForm()
    if form.validate_on_submit():
        # add to db
        title = form.title.data
        content = form.content.data
        # add to db 
        new_feedback = Feedback(username=user, title=title, content=content)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(url_for("user_info", username=user))
    return render_template("feedback_form.html", form=form, action_url=url_for('add_feedback', username=username))

    
@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    user = session.get('username')
    feedback = Feedback.query.get_or_404(feedback_id)
    if user and user == feedback.username: 
        form = FeedbackForm(obj=feedback)
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.commit()
            return redirect(url_for("user_info", username=user))
        return render_template("feedback_form.html", form=form, action_url=url_for('update_feedback', feedback_id=feedback_id))
    
    
@app.route('/feedback/<feedback_id>/delete')
def delete_feedback(feedback_id):
    user = session.get('username')
    feedback = Feedback.query.get_or_404(feedback_id)
    if user and user == feedback.username: 
        db.session.delete(feedback)
        db.session.commit()
    return redirect(url_for("user_info", username=user))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', error=error), 404
    
if __name__ == '__main__':
    app.run(debug=True)

# //improvements
# The add_feedback route seems to have some issues.
# The form's username field is set manually, which might lead to inconsistencies. 
# There's a flash message, but it might be better to use flash in conjunction with get_flashed_messages() in the template.
# The update_feedback and delete_feedback routes are currently redirecting to user_info and is not yet implemented.
# The not_found_error function receives an error parameter but does not use it. You can apply more generic error message which could be provided to users in the 404 template.
