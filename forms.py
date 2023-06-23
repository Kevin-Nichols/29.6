from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length


class RegisterForm(FlaskForm):
    """Registration form for user."""
    username = StringField('Username', 
                           validators=[InputRequired(),
                                       Length(min=1, max=20)])
    password = PasswordField('Password', 
                             validators=[InputRequired(),
                                         Length(min=8, max=50)])
    email = StringField('Email',
                        validators=[InputRequired(),
                                    Email()])
    first_name = StringField('First Name',
                             validators=[InputRequired()])
    last_name = StringField('Last Name',
                             validators=[InputRequired()])

class LoginForm(FlaskForm):
    """Login form for user."""
    username = StringField('Username', 
                           validators=[InputRequired(),
                                       Length(min=1, max=20)])
    password = PasswordField('Password', 
                             validators=[InputRequired(),
                                         Length(min=8, max=50)])
    
class FeedbackForm(FlaskForm):
    """Add new feedback form."""
    title = StringField('Feedback Title',
                        validators=[InputRequired(),
                                    Length(max=65)])
    content = StringField('Feedback Content',
                        validators=[InputRequired()])
    
class DeleteForm(FlaskForm):
    """left blank"""