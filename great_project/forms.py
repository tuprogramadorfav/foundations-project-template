from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from great_project.models import Atleta
import pycountry
from wtforms.fields.html5 import TelField

# def validate_email(form, email):
#     print('inside')
#     user = Atleta.query.filter_by(email=email.data.upper()).first()
#     print(user)
#     if user:
#         raise ValidationError('Esta direccion de correo electronico ya esta registrada. Porfavor usa una direccion de correo electronico diferente')

class CountrySelectField(SelectField):
    def __init__(self, *args, **kwargs):
        super(CountrySelectField, self).__init__(*args, **kwargs)
        self.choices = [(country.alpha_2, country.name) for country in pycountry.countries]

class RegistrationForm(FlaskForm):
    name = StringField('Nombres', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Apellidos', validators=[DataRequired(), Length(min=2, max=50)])
    month = SelectField('Fecha de Nacimiento', validators=[DataRequired()], choices=[('', 'Mes'), ('0', 'Enero'), ('1', 'Febrero'), ('2', 'Marzo'), ('3', 'Abril'), ('4', 'Mayo'), ('5', 'Junio'), ('6', 'Julio'), ('7', 'Agosto'), ('8', 'Septiembre'), ('9', 'Octubre'), ('10', 'Noviembre'), ('11', 'Diciembre')], validate_choice=False)
    cedula = StringField('Cedula', validators=[DataRequired(), Length(min=2, max=15)])
    day = SelectField('Fecha de Nacimiento', validators=[DataRequired()], choices=[('', 'Dia')], validate_choice=False)
    year = SelectField('Fecha de Nacimiento', validators=[DataRequired()], choices=[('', 'Año')], validate_choice=False)
    gender = SelectField('Genero', validators=[DataRequired()], choices=[('', 'Genero'), ('Masculino', 'Masculino'), ('Femenino', 'Femenino')])
    email = StringField('Correo Electronico', validators=[DataRequired(), Email()])
    confirm_email = StringField('Confirmar Correo Electronico', validators=[DataRequired(), EqualTo('email')])
    nacionality = StringField('Nacionalidad', validators=[DataRequired(), Length(min=2, max=25)])
    address = StringField('Direccion', validators=[DataRequired(), Length(min=2, max=50)])
    province = StringField('Provincia', validators=[DataRequired(), Length(min=2, max=50)])
    country = CountrySelectField('Pais', validators=[DataRequired()])
    city = StringField('Ciudad', validators=[DataRequired(), Length(min=2, max=50)])
    phone = TelField('Numero de Telefono', validators=[DataRequired()])
    belt = SelectField('Cinturon', validators=[DataRequired()], choices=[('', 'Cinturon')], validate_choice=False)
    academy = SelectField('Academia', validators=[DataRequired()], choices=[('', 'Academia'), ('1', 'Alliance') ])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    atleta_conf = BooleanField('Atleta')
    profesor_conf = BooleanField('Profesor')
    terms = BooleanField('Terms', validators=[DataRequired()])
    submit = SubmitField('Registrarse')
    
    def validate_email(self, email):
        user = Atleta.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Esta direccion de correo electronico ya esta registrada. Porfavor usa una direccion de correo electronico diferente')
    
    def validate_profesor_conf(self, profesor_conf):
        if profesor_conf.data == False and self.atleta_conf.data == False:
            raise ValidationError('Al menos una de las dos opciones debe ser seleccionada')

    def validate_atleta_conf(self, atleta_conf):
        if atleta_conf.data == False and self.profesor_conf.data == False:
            raise ValidationError('Al menos una de las dos opciones debe ser seleccionada')


class LoginForm(FlaskForm):

    email = StringField('Correo Electronico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesion')

class EventRegistration(FlaskForm):
    weight = SelectField('Peso', validators=[DataRequired()], choices=[], validate_choice=False)
    age_division = SelectField('Division de Edad', validators=[DataRequired()], choices=[], validate_choice=False)
    submit = SubmitField('Registrarse')

class AcademyRegistration(FlaskForm):
    name = StringField('Nombres', validators=[DataRequired(), Length(min=2, max=50)])
    country = CountrySelectField('Pais', validators=[DataRequired(), Length(min=2, max=50)])
    province = StringField('Provincia', validators=[DataRequired(), Length(min=2, max=50)])
    city = StringField('Ciudad', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Registrarse')

class UpdateAccount(FlaskForm):
    email = StringField('Correo Electronico', validators=[DataRequired(), Email()])
    address = StringField('Direccion', validators=[DataRequired(), Length(min=2, max=50)])
    province = StringField('Provincia', validators=[DataRequired(), Length(min=2, max=20)])
    country = StringField('Pais', validators=[DataRequired(), Length(min=2, max=50)])
    phone = StringField('Numero de Telefono', validators=[DataRequired(), Length(min=2, max=25)])
    belt = SelectField('Cinturon', validators=[DataRequired()], choices=[('', 'Cinturon')], validate_choice=False)
    academy = SelectField('Academia', validators=[DataRequired()], choices=[('', 'Academia'), ('1', 'Alliance') ])
    submit = SubmitField('Actualizar')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Atleta.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Esta direccion de correo electronico ya esta registrada. Porfavor usa una direccion de correo electronico diferente')


class RequestResetFrom(FlaskForm):
    email = StringField('Correo Electronico', validators=[DataRequired(), Email()])
    submit = SubmitField('Solicitar cambio de contraseña')
    def validate_email(self, email):
        user = Atleta.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Esta cuenta de correo electronico no esta registrada.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cambiar Contraseña')

