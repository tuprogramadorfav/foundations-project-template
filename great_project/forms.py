from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    nombre = StringField('Nombres', validators=[DataRequired(), Length(min=2, max=50)])
    apellido = StringField('Apellidos', validators=[DataRequired(), Length(min=2, max=50)])
    month = SelectField('Fecha de Nacimiento', validators=[DataRequired()], choices=[('', 'Mes'), ('0', 'Enero'), ('1', 'Febrero'), ('2', 'Marzo'), ('3', 'Abril'), ('4', 'Mayo'), ('5', 'Junio'), ('6', 'Julio'), ('7', 'Agosto'), ('8', 'Septiembre'), ('9', 'Octubre'), ('10', 'Noviembre'), ('11', 'Diciembre')], validate_choice=False)
    day = SelectField('Fecha de Nacimiento', validators=[DataRequired()], choices=[('', 'Dia')], validate_choice=False)
    year = SelectField('Fecha de Nacimiento', validators=[DataRequired()], choices=[('', 'Año')], validate_choice=False)
    genero = SelectField('Genero', validators=[DataRequired()], choices=[('', 'Genero'), ('m', 'Masculino'), ('f', 'Femenino')])
    email = StringField('Correo Electronico', validators=[DataRequired(), Email()])
    confirm_email = StringField('Confirmar Correo Electronico', validators=[DataRequired(), EqualTo('email')])
    nacionalidad = StringField('Nacionalidad', validators=[DataRequired(), Length(min=2, max=25)])
    direccion = StringField('Direccion', validators=[DataRequired(), Length(min=2, max=50)])
    provincia = StringField('Provincia', validators=[DataRequired(), Length(min=2, max=20)])
    pais = StringField('Pais', validators=[DataRequired(), Length(min=2, max=20)])
    telefono = StringField('Numero de Telefono', validators=[DataRequired(), Length(min=2, max=25)])
    belt = SelectField('Cinturon', validators=[DataRequired()], choices=[('', 'Cinturon')], validate_choice=False)
    academia = SelectField('Academia', validators=[DataRequired()], choices=[('', 'Academia'), ('1', 'Alliance') ])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    terms = BooleanField('Terms', validators=[DataRequired()])
    submit = SubmitField('Registrarse')

class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')