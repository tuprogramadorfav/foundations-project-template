from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired

class EventRegistration(FlaskForm):
    weight = SelectField('Peso', validators=[DataRequired()], choices=[], validate_choice=False)
    age_division = SelectField('Division de Edad', validators=[DataRequired()], choices=[], validate_choice=False)
    submit = SubmitField('Registrarse')