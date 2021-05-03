from great_project import db
from great_project.models import Atleta, Academy, Belt, Gender, Event, Registration, Weight, Age_division
from faker import Faker
import random
import datetime

fake = Faker()

def add_atletas():
    for _ in range(500):
        start_date = datetime.date(1970, 1, 1)
        end_date = datetime.date(2017, 2, 1)
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)
        genders = Gender.query.all()
        gender_choice = random.choice(genders)
        belts = Belt.query.all()
        belt_choice = random.choice(belts)
        academies = Academy.query.all()
        academy_choice = random.choice(academies)
        atleta = Atleta(name=fake.name(), last_name=fake.last_name(), cedula='0000000', birth_date=random_date, gender_id=gender_choice.id, 
                 address='aasdfghhlkj', email=fake.email(), nacionality=fake.country(), province='Guayas',
                 country='EC', city='Guayaquil', phone='00000000', belt_id=belt_choice.id, academy_id=academy_choice.id, password=fake.password(), 
                 atleta_conf=True, profesor_conf=False)
        db.session.add(atleta)
    db.session.commit()

def add_registration():
    atletas = Atleta.query.all()
    weights = Weight.query.all()
    age_divisions = Age_division.query.all()
    x = 1
    for _ in range (1000):
        weight_choice = random.choice(weights)
        age_division_choice = random.choice(age_divisions)
        atleta = atletas[x]
        registration = Registration(weight_id=weight_choice.id, atleta_id=atleta.id, event_id=1, age_division_id=age_division_choice.id)
        db.session.add(registration)
        x+=1
    db.session.commit()

pesos = [{'Pluma':14.99, 'Pena':17.99, 'Leve':20.99, 'Medio':23.99, 'Medio-Pesado':26.99, 'Pesado':29.99, 'Super Pesado':32.99, 'Pessadissimo':33}, 
        {'Pluma':18.99, 'Pena':21.99, 'Leve':24.99, 'Medio':27.99, 'Medio-Pesado':30.99, 'Pesado':33.99, 'Super Pesado':36.99, 'Pessadissimo':37},
        {'Pluma':24.99, 'Pena':27.99, 'Leve':30.99, 'Medio':33.99, 'Medio-Pesado':36.99, 'Pesado':39.99, 'Super Pesado':42.99, 'Pessadissimo':43},
        {'Gallo':27.99, 'Pluma':30.99, 'Pena':33.99, 'Leve':36.99, 'Medio':39.99, 'Medio-Pesado':42.99, 'Pesado':45.99, 'Super Pesado':48.99, 'Pessadissimo':49},
        {'Gallo':33.99, 'Pluma':37.99, 'Pena':40.99, 'Leve':44.99, 'Medio':49.99, 'Medio-Pesado':53.99, 'Pesado':57.99, 'Super Pesado':61.99, 'Pessadissimo':62, 'Absoluto':1000 },
        {'Gallo':41.99, 'Pluma':45.99, 'Pena':49.99, 'Leve':53.99, 'Medio':57.99, 'Medio-Pesado':61.99, 'Pesado':65.99, 'Super Pesado':69.99, 'Pessadissimo':70, 'Absoluto':1000},
        {'Gallo':50.99, 'Pluma':55.99, 'Pena':60.99, 'Leve':65.99, 'Medio':70.99, 'Medio-Pesado':75.99, 'Pesado':80.99, 'Super Pesado':85.99, 'Pessadissimo':86, 'Absoluto':1000},
        {'Gallo':54.99, 'Pluma':60.99, 'Pena':66.99, 'Leve':72.99, 'Medio':78.99, 'Medio-Pesado':84.99, 'Pesado':90.99, 'Super Pesado':96.99, 'Pessadissimo':97, 'Absoluto':1000},
        {'Gallo':45.99, 'Pluma':50.99, 'Pena':55.99, 'Leve':60.99, 'Medio':65.99, 'Medio-Pesado':70.99, 'Pesado':75.99, 'Super Pesado':80.99, 'Pessadissimo':81, 'Absoluto':1000},
        ]

# infanto1 = {'Pluma':14.99, 'Pena':17.99, 'Leve':20.99, 'Medio':23.99, 'Medio-Pesado':26.99, 'Pesado':29.99, 'Super Pesado':32.99, 'Pessadissimo':33}
# infanto2 = {'Pluma':18.99, 'Pena':21.99, 'Leve':24.99, 'Medio':27.99, 'Medio-Pesado':30.99, 'Pesado':33.99, 'Super Pesado':36.99, 'Pessadissimo':37}
# infanto3 = {'Pluma':24.99, 'Pena':27.99, 'Leve':30.99, 'Medio':33.99, 'Medio-Pesado':36.99, 'Pesado':39.99, 'Super Pesado':42.99, 'Pessadissimo':43}
# infanto4 = {'Gallo':27.99, 'Pluma':30.99, 'Pena':33.99, 'Leve':36.99, 'Medio':39.99, 'Medio-Pesado':42.99, 'Pesado':45.99, 'Super Pesado':48.99, 'Pessadissimo':49}
# infanto_juvenil1 = {'Gallo':33.99, 'Pluma':37.99, 'Pena':40.99, 'Leve':44.99, 'Medio':49.99, 'Medio-Pesado':53.99, 'Pesado':57.99, 'Super Pesado':61.99, 'Pessadissimo':62, 'Absoluto':1000 }
# infanto_juvenil2 = {'Gallo':41.99, 'Pluma':45.99, 'Pena':49.99, 'Leve':53.99, 'Medio':57.99, 'Medio-Pesado':61.99, 'Pesado':65.99, 'Super Pesado':69.99, 'Pessadissimo':70, Absoluto':1000}
# juvenil = {'Gallo':50.99, 'Pluma':55.99, 'Pena':60.99, 'Leve':65.99, 'Medio':70.99, 'Medio-Pesado':75.99, 'Pesado':80.99, 'Super Pesado':85.99, 'Pessadissimo':86, 'Absoluto':1000}
# masculino = {'Gallo':54.99, 'Pluma':60.99, 'Pena':66.99, 'Leve':72.99, 'Medio':78.99, 'Medio-Pesado':84.99, 'Pesado':90.99, 'Super Pesado':96.99, 'Pessadissimo':97, 'Absoluto':1000}
# femenino = {'Gallo':45.99, 'Pluma':50.99, 'Pena':55.99, 'Leve':60.99, 'Medio':65.99, 'Medio-Pesado':70.99, 'Pesado':75.99, 'Super Pesado':80.99, 'Pessadissimo':81, 'Absoluto':1000}



categories = [['Infanto 1', 4, 5], ['Infanto 2', 6, 7], ['Infanto 3', 8, 9], ['Infanto 4', 10, 11], ['Infanto Juvenil 1', 12, 13], ['Infanto Juvenil 2', 14, 15], ['Juvenil', 16, 17], ['Adulto', 18, 80], ['Master', 30, 80]]
for category in categories:
    category_1 = Age_division(name = category[0], initial_age = category[1], top_age = category[2])
    db.session.add(category_1)
    db.session.commit()

belts = ['Blanco', 'Gris', 'Amarillo', 'Naranja', 'Verde', 'Azul', 'Violeta', 'Marron', 'Negro']

for belt in belts:
    belt_1 = Belt(name=belt)
    db.session.add(belt_1)
    db.session.commit()

x = 0
age_divisions = db.session.query(Age_division).order_by(Age_division.id).all()


academia = Academy(name='Alliance LDE', province='Guayas', city='Guayaquil', country='EC')
db.session.add(academia)
db.session.commit()

genders = ['Masculino', 'Femenino']
for gender in genders:
    genero = Gender(name=gender)
    db.session.add(genero)
    db.session.commit(

for age_division in age_divisions:
    for belt in belts:
        for weight in weights:
            for gender in genders:
                all = db.session.query(Atleta.name).join(Registration.atleta).join(Registration.category).join(Atleta.belt).join(Registration.weight).join(Atleta.gender).filter(Age_division.name == age_division[0], Belt.name == belt[0], Weight.name == weight[0], Weight.weight == weight[1], Gender.name == gender[0]).all()
                if all != []:
                    print(f"[{age_division}, {belt}, {weight}, {gender}]: {all}")


for belt in belts:
    for age_division in age_divisions:
        for gender in genders:
            for weight in weights:
                atletas = db.session.query(Atleta.name).join(Registration.event).join(Registration.atleta).join(Registration.age_division).join(Atleta.belt).join(Registration.weight).join(Atleta.gender).filter(event_id == event_id.id, Gender.id == gender, Weight.id == weight.id, Age_division.id == age_division, Belt.id == belt).all()
                tables.append(atletas