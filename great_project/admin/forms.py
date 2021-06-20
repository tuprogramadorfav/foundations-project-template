from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from great_project.models import Atleta

class ResultsForm(FlaskForm):
    first_place = SelectField('Primer Lugar', validators=[DataRequired()], choices=[('', 'Primer Lugar')], validate_choice=False)
    second_place = SelectField('Segundo Lugar', validators=[DataRequired()], choices=[('', 'Segundo Lugar')], validate_choice=False)
    third_place = SelectField('Tercer Lugar', choices=[('', 'Tercer Lugar')], validate_choice=False)
    third_place1 = SelectField('Tercer Lugar', choices=[('', 'Tercer Lugar')], validate_choice=False)

    submit = SubmitField('Confirmar')
    
    # check if the provided email is already in the database
