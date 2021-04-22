from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    confirm_email = PasswordField('Confirmar Correo Electronico', validators=[DataRequired(), EqualTo('email')])
    nacionalidad = StringField('Nacionalidad', validators=[DataRequired(), Length(min=2, max=25)])
    direccion = StringField('Direccion', validators=[DataRequired(), Length(min=2, max=50)])
    provincia = StringField('Provincia', validators=[DataRequired(), Length(min=2, max=20)])
    pais = StringField('Pais', validators=[DataRequired(), Length(min=2, max=20)])
    telefono = StringField('Numero de Telefono', validators=[DataRequired(), Length(min=2, max=25)])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')