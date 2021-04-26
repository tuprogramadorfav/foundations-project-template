from great_project import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(atleta_id):
    return Atleta.query.get(int(atleta_id))


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
    nacionalidad = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(100), nullable=False)
    provincia = db.Column(db.String(50), nullable=False)
    pais = db.Column(db.String(50), nullable=False)
    ciudad = db.Column(db.String(60), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    belt_id = db.Column(db.Integer, db.ForeignKey('belt.id'), nullable=False)
    academia_id = db.Column(db.Integer, db.ForeignKey('academia.id'), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    atleta_conf = db.Column(db.Boolean)
    profesor_conf = db.Column(db.Boolean)
    points = db.Column(db.Integer, nullable=False, default=0)
    is_admin = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref = 'atleta', lazy=True)

    def __repr__(self):
        return f"Atleta('{self.name}' '{self.apellido}', '{self.email}', '{self.year}', '{self.gender}', '{self.belt_id}', '{self.academia_id}', '{self.points}')"

class Gender(db.Model):
    __tablename__ = 'gender'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    atletas = db.relationship('Atleta', backref = 'gender', lazy=True)
    weights = db.relationship('Weight', backref = 'gender', lazy=True)

    def __repr__(self):
        return f"Gender('{self.name}')"

class Academia(db.Model):
    __tablename__ = 'academia'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    pais = db.Column(db.String(60), nullable=False)
    provincia = db.Column(db.String(60), nullable=False)
    ciudad = db.Column(db.String(60), nullable=False)
    points = db.Column(db.Integer, nullable=False, default=0)
    atletas = db.relationship('Atleta', backref = 'academia', lazy=True)

    def __repr__(self):
        return f"Academia('{self.name}')"

class Belt(db.Model):
    __tablename__ = 'belt'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    atletas = db.relationship('Atleta', backref = 'belt', lazy=True)

    def __repr__(self):
        return f"Belt('{self.name}')"


class Weight(db.Model):
    __tablename__ = 'weight'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    kimono = db.Column(db.Boolean, nullable=False)
    gender_id = db.Column(db.Integer, db.ForeignKey('gender.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    orders = db.relationship('Order', backref = 'weight', lazy=True)

    def __repr__(self):
        return f"Weight('{self.name}', '{self.weight}', '{self.gender_id.name}', '{self.category_id.name}')"

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    initial_age = db.Column(db.Integer, nullable=False)
    top_age = db.Column(db.Integer, nullable=False)
    weights = db.relationship('Weight', backref = 'category', lazy=True)

    def __repr__(self):
        return f"Category('{self.name}', '{self.inital_age}', '{self.top_age}')"    


class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    place = db.Column(db.String(20), nullable=False)
    ciudad = db.Column(db.String(60), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.String(50), nullable=False)
    days = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False, default=40)
    reg_limit = db.Column(db.DateTime, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    kimono = db.Column(db.Boolean, nullable=False)
    orders = db.relationship('Order', backref='event', lazy=True)

    def __repr__(self):
        return f"Event('{self.name}', '{self.place}', '{self.date}')"    

class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    weight_id = db.Column(db.Integer, db.ForeignKey('weight.id'), nullable=False)
    atleta_id = db.Column(db.Integer, db.ForeignKey('atleta.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('atleta_id', 'event_id', name='unique_constraint_atleta_event'), )

    def __repr__(self):
        return f"Order('{self.weight_id.name}', '{self.atleta_id.name}', '{self.event_id.name}')"    

