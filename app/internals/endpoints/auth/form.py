from app.internals.endpoints.__init__ import *

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    phone_number = IntegerField('Phone Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    pin_code = StringField('Pin Code', validators=[DataRequired()])
    role = SelectField('Role', choices=[('user', 'User')], default='user')
    submit = SubmitField('Register')