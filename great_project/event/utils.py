from great_project.models import Age_division
import datetime
from datetime import date
from flask_login import current_user
from great_project import db, mail
from flask_login import current_user
from flask import current_app
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message


def age_division_choices():
    current_year = date.today().year
    age = current_year - current_user.birth_date.year
    return Age_division.query.filter(Age_division.initial_age <= age, Age_division.top_age >= age)


def generate_confirmation_token(id):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(id, salt=current_app.config['EVENT_CONFIRMATION_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        id = serializer.loads(
            token,
            salt=current_app.config['EVENT_CONFIRMATION_SALT'],
            max_age=expiration
        )
        print(id)
    except:
        return False
    return id


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
