from great_project import db


class Atleta(db.model):
    id = db.column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer(50), nullable=False)
    month = db.Column(db.String(50), nullable=False)
    day = db.Column(db.Integer(50), nullable=False)
    gender_id = db.Column(db.Integer, db.ForeignKey(gender.id), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nacionalidad = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(100), nullable=False)
    provincia = db.Column(db.String(50), nullable=False)
    pais = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    belt_id = db.Column(db.Integer, db.ForeignKey(belt.id), nullable=False)
    academia_id = db.Column(db.Integer, db.ForeignKey(academia.id), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    points = db.Column(db.Integer(50), nullable=False, default=0)
    orders = db.relationship('Order', backref = 'atleta', lazy=True)


class Academia(db.model):
    id = db.column(db.Integer, primary_key=True)
    pais = db.Column(db.String(60), nullable=False)
    provincia = db.Column(db.String(60), nullable=False)
    ciudad = db.Column(db.String(60), nullable=False)
    nombre = db.Column(db.String(60), nullable=False, unique=True)
    points = db.Column(db.Integer(50), nullable=False, default=0)
    atletas = db.relationship('Atleta', backref = 'academia', lazy=True)

class Belt(db.model):
    id = db.column(db.Integer, primary_key=True)
    belt = db.Column(db.String(60), nullable=False)
    atletas = db.relationship('Atleta', backref = 'belt', lazy=True)

class Gender(db.model):
    id = db.column(db.Integer, primary_key=True)
    sex = db.Column(db.String(20), nullable=False, unique=True)
    atletas = db.relationship('Atleta', backref = 'gender', lazy=True)
    weights = db.relationship('Weight', backref = 'gender', lazy=True)

class Event(db.model):
    id = db.column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    place = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    orders = db.relationship('Order', backref = 'event', lazy=True)

class Order(db.Model):
    id = db.column(db.Integer, primary_key=True)
    weight_id = db.Column(db.Integer, db.ForeignKey(weight.id), nullable=False)
    atleta_id = db.Column(db.Integer, db.ForeignKey(atleta.id), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey(event.id), nullable=False)
    __table_args__ = (db.UniqueConstraint('atleta_id', 'event-id', name='atleta_order_uc'),)

class Weight(db.model):
    id = db.column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    weight = db.Column(db.Integer(50), nullable=False)
    gender_id = db.Column(db.Integer, db.ForeignKey(gender.id), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(category.id), nullable=False)
    orders = db.relationship('Order', backref = 'weight', lazy=True)

class Category(db.model):
    id = db.column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    initial_age = db.Column(db.Integer(50), nullable=False)
    top_age = db.Column(db.Integer(50), nullable=False)
    weights = db.relationship('Weight', backref = 'category', lazy=True)