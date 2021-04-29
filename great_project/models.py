from great_project import db, login_manager
from flask_login import UserMixin
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView

@login_manager.user_loader
def load_user(atleta_id):
    return Atleta.query.get(int(atleta_id))


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

# gender_agedivision_belt_weight = db.Table('gender_agedivision_belt_weight',
#     db.Column('weight_id', db.Integer, db.ForeignKey('weight.id')),
#     db.Column('gender_agedivison_belt_id', db.Integer, db.ForeignKey('gender_agedivision_belt.id'))
#     )


class Gender(db.Model):
    __tablename__ = 'gender'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    atletas = db.relationship('Atleta', backref = 'gender', lazy=True)
    # age_divisions = db.relationship('Age_division', secondary=Gender_agedivision, backref=db.backref('gender', lazy = 'dynamic'))

    def __repr__(self):
        return f"Gender('{self.name}')"

class Age_division(db.Model):
    __tablename__ = 'age_division'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    initial_age = db.Column(db.Integer, nullable=False)
    top_age = db.Column(db.Integer, nullable=False)
    registration = db.relationship('Registration', backref = 'category', lazy=True)

    

    def __repr__(self):
        return f"{self.name}', '{self.inital_age}', '{self.top_age}'"    
        
class Atleta(db.Model, UserMixin):
    __tablename__ = 'atleta'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    cedula = db.Column(db.String(60), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.String(50), nullable=False)
    day = db.Column(db.Integer, nullable=False)
    gender_id = db.Column(db.Integer, db.ForeignKey('gender.id'), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nacionality = db.Column(db.String(50), nullable=False)
    adress = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(60), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    belt_id = db.Column(db.Integer, db.ForeignKey('belt.id'), nullable=False)
    academia_id = db.Column(db.Integer, db.ForeignKey('academia.id'), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    atleta_conf = db.Column(db.Boolean)
    profesor_conf = db.Column(db.Boolean)
    points = db.Column(db.Integer, nullable=False, default=0)
    is_admin = db.Column(db.Boolean, default=False)
    registrations = db.relationship('Registration', backref = 'atleta', lazy=True)

    def __repr__(self):
        return f"Atleta('{self.name}' '{self.apellido}', '{self.email}', '{self.year}', '{self.gender}', '{self.belt_id}', '{self.academia_id}', '{self.points}')"



class Academia(db.Model):
    __tablename__ = 'academia'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    country = db.Column(db.String(60), nullable=False)
    province = db.Column(db.String(60), nullable=False)
    city = db.Column(db.String(60), nullable=False)
    points = db.Column(db.Integer, nullable=False, default=0)
    atletas = db.relationship('Atleta', backref = 'academia', lazy=True)

    def __repr__(self):
        return {self.name}

class Belt(db.Model):
    __tablename__ = 'belt'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    atletas = db.relationship('Atleta', backref = 'belt', lazy=True)
    # gender_agedivisions = db.relationship('Gender_agedivision', secondary=Gender_agedivision_belt, backref=db.backref('belt', lazy = 'dynamic'))

    def __repr__(self):
        return {self.name}


class Weight(db.Model):
    __tablename__ = 'weight'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    kimono = db.Column(db.Boolean, nullable=False)
    registrations = db.relationship('Registration', backref = 'weight', lazy=True)
    # gender_agedivisions_belts = db.relationship('Gender_agedivison_belt', secondary=Gender_agedivision_belt_weight, backref=db.backref('weights', lazy = 'dynamic'))

    def __repr__(self):
        return f"{self.name}, {self.weight}, {self.gender_id.name}, {self.category_id.name}"


class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    place = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(60), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.String(50), nullable=False)
    days = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False, default=40)
    reg_limit = db.Column(db.DateTime, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    kimono = db.Column(db.Boolean, nullable=False)
    registrations = db.relationship('Registration', backref='event', lazy=True)

    def __repr__(self):
        return f"Event('{self.name}', '{self.place}', '{self.date}')"    

class Registration(db.Model):
    __tablename__ = 'registration'

    id = db.Column(db.Integer, primary_key=True)
    weight_id = db.Column(db.Integer, db.ForeignKey('weight.id'), nullable=False)
    atleta_id = db.Column(db.Integer, db.ForeignKey('atleta.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    age_division_id = db.Column(db.Integer, db.ForeignKey('age_division.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('atleta_id', 'event_id', name='unique_constraint_atleta_event'), )

    def __repr__(self):
        return f"{self.weight_id.name}, {self.atleta_id.name}, {self.event_id.name}"    

