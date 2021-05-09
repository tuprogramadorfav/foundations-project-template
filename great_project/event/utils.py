import datetime
from datetime import date
from flask_login import current_user
from great_project import db


def age_division_choices():
    current_year = date.today().year
    age = current_year - current_user.birth_date.year
    return Age_division.query.filter(Age_division.initial_age <= age, Age_division.top_age >= age)

from great_project.models import Age_division