import datetime
from datetime import date
from flask import url_for
from flask_mail import Message
from great_project import mail, db
from great_project.models import Age_division_belt, Age_division, Belt
from flask_login import current_user

# function to send reset password emails
def send_reset_email(atleta):
    token = atleta.get_reset_token()
    print(token)
    msg = Message('Solicitud de Restablecimiento de Contraseña', sender='jarcmb2118@gmail.com', recipients=[atleta.email])
    msg.body = f'''Para restablecer su contraseña, ingrese al siguiente link:
{url_for('users.reset_token', token=token, _external=True)}

El link solo sera valido durante 30 minutos, si han pasado mas de 30 minutos desde que recibio este correo electronico porfavor vuelva a llenar lo solicitud de reestablecimiento de contraseña en el siguiente link:
 {url_for('users.reset_request', _external=True)}
Si usted no ha hecho esta solicitud simplemente ignore este correo electronico y no se hara ningun cambio.
'''
    mail.send(msg)

# function to determine the choices an athlete can choose depending on their birth date
def belt_choices():
    current_year = date.today().year
    age = current_year - current_user.birth_date.year
    return db.session.query(Belt).join(Age_division_belt).join(Age_division).filter(Age_division.initial_age <= age, Age_division.top_age >= age)