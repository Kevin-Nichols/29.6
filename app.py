from flask import Flask, render_template, redirect, session, flash 
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "sosecretithurts"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    """Website's home page."""
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles registering a new user."""
    if 'username' in session:
        return redirect(f'/users/{session["username"]}')
    
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username
        
        flash('You have created a new accout!', "info")
        return redirect(f"/users/{new_user.username}")
    else:
        return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles logging in an existing user."""
    if 'username' in session:
        return redirect(f'/users/{session["username"]}')
    
    form=LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            flash('Welcome back!', "info")
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password']
            
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    """Handles logging out a user that is logged in."""
    session.pop('username')
    flash('See you again soon!', "info")
    return redirect('/login')


@app.route("/users/<username>")
def show_user_data(username):
    """Displays feedback posted by the given user."""
    if 'username' not in session or username != session['username']:
        flash("You are not authorized for that user", "danger")
        return redirect(f'/users/{session["username"]}')
    
    user = User.query.get(username)
    form = DeleteForm()
    
    return render_template("show_user.html", user=user, form=form)


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Handles removal of a given user that iss logged in."""
    if 'username' not in session or username != session['username']:
        flash("You are not authorized for that user", "danger")
        return redirect(f'/users/{session["username"]}')
    
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """Handles adding a new feedback post."""
    if 'username' not in session or username != session['username']:
        flash("You are not authorized for that user", "danger")
        return redirect(f'/users/{session["username"]}')
    
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title,
                            content=content,
                            username=username)
        
        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    else:
        return render_template("new_feedback.html", form=form) 
    
    
@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Handles editing an existing feedback post."""
    feedback = Feedback.query.get(feedback_id)
    if 'username' not in session or feedback.username != session['username']:
        flash("You are not authorized for that user", "danger")
        return redirect(f'/users/{session["username"]}')
    
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        
        db.session.commit()
        
        return redirect(f"/users/{feedback.username}")
    
    return render_template("edit_feedback.html", form=form, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Handles removing a feedback post."""
    feedback = Feedback.query.get(feedback_id)
    if 'username' not in session or feedback.username != session['username']:
        flash("You are not authorized for that user", "danger")
        return redirect(f'/users/{session["username"]}')
    
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")