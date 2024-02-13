from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, IntegerField, DecimalField, SubmitField 
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[ DataRequired(), Email()])
    password = PasswordField('Password', validators=[ DataRequired() ])
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    username = StringField('Username', validators=[ DataRequired() ])
    email = StringField('Email', validators= [ DataRequired(), Email()])
    password = PasswordField('Password', validators = [ DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[ DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class ProductForm(FlaskForm):
    name = StringField('Pokemon Name', validators=[ DataRequired() ] )
    image = StringField('Img url **Optional')
    description = StringField('Description **Optional')
    type = StringField('Type', validators=[ DataRequired() ])
    ability = StringField('Ability', validators=[ DataRequired() ])
    height = IntegerField('Height', validators=[DataRequired()])
    submit = SubmitField('Submit')