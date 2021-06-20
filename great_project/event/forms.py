from great_project.models import Registration
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from flask_login import current_user


class EventRegistration(FlaskForm):
    weight = SelectField('Peso', validators=[DataRequired()], choices=[], validate_choice=False)
    age_division = SelectField('Division de Edad', validators=[DataRequired()], choices=[], validate_choice=False)
    submit = SubmitField('Registrarse')

    def validate_weight(self, weight):
        print(current_user.id)
        user = Registration.query.filter_by(atleta_id=current_user.id).first()
        if user:
            raise ValidationError('Ya te has registrado a este evento')