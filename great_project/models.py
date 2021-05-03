import datetime
from great_project import db
from flask_login import UserMixin
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from sqlalchemy_utils import force_auto_coercion
from babel import Locale
from sqlalchemy_utils import Country, CountryType, EmailType, DateRangeType

force_auto_coercion()




# class Gender_agedivision(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     gender_id = db.Column(db.Integer, db.ForeignKey('gender.id'))
#     age_division_id = db.Column(db.Integer, db.ForeignKey('age_division.id'))

# class Gender_agedivision_belt(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     belt_id = db.Column(db.Integer, db.ForeignKey('belt.id'))
#     gender_agedivision_id = db.Column(db.Integer, db.ForeignKey('gender_agedivision.id'))

# class Gender_agedivision_belt_weight(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     weight_id = db.Column(db.Integer, db.ForeignKey('weight.id'))
#     gender_agedivison_belt_id = db.Column(db.Integer, db.ForeignKey('gender_agedivison_belt.id'))

# gender_agedivision = db.Table('gender_agedivision',
#     db.Column('id', db.Integer, primary_key=True),
#     db.Column('gender_id', db.Integer, db.ForeignKey('gender.id')),
#     db.Column('age_division_id', db.Integer, db.ForeignKey('age_division.id')),
#     db.relationship('Belt', secondary=gender_agedivision_belt, backref=db.backref('gender_agedivision', lazy = 'dynamic'))
#     )

# gender_agedivision_belt = db.Table('gender_agedivision_belt',
#     db.Column('id', db.Integer, primary_key=True),
#     db.Column('belt_id', db.Integer, db.ForeignKey('belt.id')),
#     db.Column('gender_agedivision_id', db.Integer, db.ForeignKey('gender_agedivision.id')),
#     db.relationship('Weight', secondary=gender_agedivision_belt_weight, backref=db.backref('gender_agedivision_belt', lazy = 'dynamic'))
#     )


class Weight_age_division_gender(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight_id = db.Column(db.Integer, db.ForeignKey('weight.id'))
    age_division_id = db.Column(db.Integer, db.ForeignKey('age_division.id'))
    gender_id = db.Column(db.Integer, db.ForeignKey('gender.id'))
    weight = db.relationship('Weight', back_populates='weight_agedivision_genders')
    age_division = db.relationship('Age_division', back_populates='weight_agedivision_genders')
    gender = db.relationship('Gender', back_populates='weight_agedivision_genders')


class Gender(db.Model):
    __tablename__ = 'gender'
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    atletas = db.relationship('Atleta', backref = 'gender', lazy=True)
    weight_agedivision_genders = db.relationship('Weight_age_division_gender', back_populates='gender')

    def __repr__(self):
        return self.name

class Age_division(db.Model):
    __tablename__ = 'age_division'
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    initial_age = db.Column(db.Integer, nullable=False)
    top_age = db.Column(db.Integer, nullable=False)
    registration = db.relationship('Registration', backref = 'age_division', lazy=True)
    weight_agedivision_genders = db.relationship('Weight_age_division_gender', back_populates='age_division')
    def __repr__(self):
        return f"{self.name}', '{self.initial_age}', '{self.top_age}'"    

class Academy(db.Model):
    __tablename__ = 'academy'
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    country = db.Column(db.String(60), nullable=False)
    province = db.Column(db.String(60), nullable=False)
    city = db.Column(db.String(60), nullable=False)
    points = db.Column(db.Integer, nullable=False, default=0)
    atletas = db.relationship('Atleta', backref = 'academy', lazy=True)

    def __repr__(self):
        return self.name


class Belt(db.Model):
    __tablename__ = 'belt'
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    atletas = db.relationship('Atleta', backref = 'belt', lazy=True)
    # gender_agedivisions = db.relationship('Gender_agedivision', secondary=Gender_agedivision_belt, backref=db.backref('belt', lazy = 'dynamic'))

    def __repr__(self):
        return self.name
        
class Atleta(db.Model, UserMixin):
    __tablename__ = 'atleta'
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    cedula = db.Column(db.String(60), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    gender_id = db.Column(db.Integer, db.ForeignKey('gender.id'), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    nacionality = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(50), nullable=False)
    country = db.Column(CountryType, nullable=False)
    city = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    belt_id = db.Column(db.Integer, db.ForeignKey('belt.id'), nullable=False)
    academy_id = db.Column(db.Integer, db.ForeignKey('academy.id'), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    atleta_conf = db.Column(db.Boolean)
    profesor_conf = db.Column(db.Boolean)
    points = db.Column(db.Integer, nullable=False, default=0)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    registrations = db.relationship('Registration', backref = 'atleta', lazy=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"Atleta('{self.name}' '{self.last_name}', '{self.email}', '{self.birth_date.year}', '{self.gender}', '{self.belt}', '{self.academy}', '{self.points}')"







class Weight(db.Model):
    __tablename__ = 'weight'
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    kimono = db.Column(db.Boolean, nullable=False)
    registrations = db.relationship('Registration', backref = 'weight', lazy=True)
    weight_agedivision_genders = db.relationship('Weight_age_division_gender', back_populates='weight')
    def __repr__(self):
        return f"{self.name}, {self.weight}"


class Event(db.Model):
    __tablename__ = 'event'
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    place = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(60), nullable=False)
    # date = db.Column(DateRangeType, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Integer, nullable=False, default=40)
    reg_limit = db.Column(db.DateTime, nullable=False)
    kimono = db.Column(db.Boolean, nullable=False)
    registrations = db.relationship('Registration', backref='event', lazy=True)

    def __repr__(self):
        return f"'{self.name}', '{self.place}', '{self.date}'"    

class Registration(db.Model):
    __tablename__ = 'registration'
    # __table_args__ =  (db.UniqueConstraint('atleta_id', 'event_id', name='unique_constraint_atleta_event'), )
    id = db.Column(db.Integer, primary_key=True)
    weight_id = db.Column(db.Integer, db.ForeignKey('weight.id'), nullable=False)
    atleta_id = db.Column(db.Integer, db.ForeignKey('atleta.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    age_division_id = db.Column(db.Integer, db.ForeignKey('age_division.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('atleta_id', 'event_id', name='unique_constraint_atleta_event'), )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"{self.weight}, {self.atleta}, {self.event}"    

