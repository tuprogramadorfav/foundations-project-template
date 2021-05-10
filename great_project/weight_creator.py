from great_project import create_app
from great_project.__init__ import db
from great_project.models import current_app, Atleta, Academy, Belt, Gender, Event, Registration, Weight, Age_division, Weight_age_division_gender, Age_division_belt
from faker import Faker
import random
import datetime
from datetime import date

app = create_app()
app.app_context().push()

fake = Faker()

def add_atletas(start_year, end_year):
    current_year = date.today().year
    for _ in range(800):
        start_date = datetime.date(start_year, 1, 1)
        end_date = datetime.date(end_year, 2, 1)
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)
        age = current_year - random_date.year
        genders = Gender.query.all()
        gender_choice = random.choice(genders)
        if age >= 4 and age <= 5:
            belts_id = db.session.query(Age_division_belt.belt_id).filter(Age_division_belt.age_division_id == 1).all()
            belt_choice = random.choice(belts_id)
        elif age >= 6 and age <= 7:
            belts_id = db.session.query(Age_division_belt.belt_id).filter(Age_division_belt.age_division_id == 2).all()
            belt_choice = random.choice(belts_id)
        elif age >= 8 and age <= 9:
            belts_id = db.session.query(Age_division_belt.belt_id).filter(Age_division_belt.age_division_id == 3).all()
            belt_choice = random.choice(belts_id)
        elif age >= 10 and age <= 11:
            belts_id = db.session.query(Age_division_belt.belt_id).filter(Age_division_belt.age_division_id == 4).all()
            belt_choice = random.choice(belts_id)
        elif age >= 12 and age <= 13:
            belts_id = db.session.query(Age_division_belt.belt_id).filter(Age_division_belt.age_division_id == 5).all()
            belt_choice = random.choice(belts_id)
        elif age >= 14 and age <= 15:
            belts_id = db.session.query(Age_division_belt.belt_id).filter(Age_division_belt.age_division_id == 6).all()
            belt_choice = random.choice(belts_id)
        elif age >= 16 and age <= 17:
            belts_id = db.session.query(Age_division_belt.belt_id).filter(Age_division_belt.age_division_id == 7).all()
            belt_choice = random.choice(belts_id)
        elif age >= 18 and age <= 29:
            belts_id = db.session.query(Age_division_belt.belt_id).filter(Age_division_belt.age_division_id == 8).all()
            belt_choice = random.choice(belts_id)
        elif age >= 30:
            belts_id = db.session.query(Age_division_belt.belt_id).filter(Age_division_belt.age_division_id == 9).all()
            belt_choice = random.choice(belts_id)
        academies = Academy.query.all()
        academy_choice = random.choice(academies)
        atleta = Atleta(name=fake.name(), last_name=fake.last_name(), cedula='0000000', birth_date=random_date, gender_id=gender_choice.id, 
                 address='aasdfghhlkj', email=fake.email(), nacionality=fake.country(), province='Guayas',
                 country='EC', city='Guayaquil', phone='00000000', belt_id=belt_choice[0], academy_id=academy_choice.id, password=fake.password(), 
                 atleta_conf=True, profesor_conf=False)
        db.session.add(atleta)
    db.session.commit()

def add_registration(x_value):
    atletas = Atleta.query.all()
    weights = Weight.query.all()
    x = x_value
    current_year = date.today().year
    for _ in range(799):
        age = current_year - atletas[x].birth_date.year
        age_division_choice = random.choice(Age_division.query.filter(Age_division.initial_age <= age, Age_division.top_age >= age).all())
        weight_choice = random.choice( db.session.query(Weight).join(Weight_age_division_gender).join(Age_division).join(Gender).filter(Age_division.id == age_division_choice.id, Gender.id == atletas[x].gender_id).all())
        atleta = atletas[x]
        registration = Registration(weight_id=weight_choice.id, atleta_id=atleta.id, event_id=1, age_division_id=age_division_choice.id)
        db.session.add(registration)
        x+=1
    db.session.commit()

genders = ['Masculino', 'Femenino']
for gender in genders:
    genero = Gender(name=gender)
    db.session.add(genero)
    db.session.commit()

belts = ['Blanco', 'Gris', 'Amarillo', 'Naranja', 'Verde', 'Azul', 'Violeta', 'Marron', 'Negro']

for belt in belts:
    belt_1 = Belt(name=belt)
    db.session.add(belt_1)
    db.session.commit()

academia1 = Academy(name='Team Alfa', province='Guayas', city='Guayaquil', country='EC')
academia2 = Academy(name='Alliance LDE', province='Guayas', city='Guayaquil', country='EC')
academia3 = Academy(name='Dojo Leo Iturralde', province='Guayas', city='Guayaquil', country='EC')
academia4 = Academy(name='Team Cascagrossa', province='Guayas', city='Guayaquil', country='EC')
academia5 = Academy(name='Mantra', province='Guayas', city='Guayaquil', country='EC')
db.session.add(academia1)
db.session.add(academia2)
db.session.add(academia3)
db.session.add(academia4)
db.session.add(academia5)
db.session.commit()

belts = db.session.query(Belt).order_by(Belt.id).all()
categories = [['Infanto 1', 4, 5], ['Infanto 2', 6, 7], ['Infanto 3', 8, 9], ['Infanto 4', 10, 11], ['Infanto Juvenil 1', 12, 13], ['Infanto Juvenil 2', 14, 15], ['Juvenil', 16, 17], ['Adulto', 18, 80], ['Master', 30, 80]]
for category in categories:
    print(category)
    category_1 = Age_division(name = category[0], initial_age = category[1], top_age = category[2])
    db.session.add(category_1)
    age_division_belt = Age_division_belt(belt=belts[0], age_division=category_1)
    db.session.add(age_division_belt)
    db.session.commit()
    if category[0] == 'Infanto 1':
        for belt in belts[1:2]:
            age_division_belt = Age_division_belt(belt=belt, age_division=category_1)
            db.session.add(age_division_belt)
            db.session.commit()
    elif category[0] == 'Infanto 2' or category[0] == 'Infanto 3':
        for belt in belts[1:3]:
            age_division_belt = Age_division_belt(belt=belt, age_division=category_1)
            db.session.add(age_division_belt)
            db.session.commit()
    elif category[0] == 'Infanto 4':
        for belt in belts[1:4]:
            age_division_belt = Age_division_belt(belt=belt, age_division=category_1)
            db.session.add(age_division_belt)
            db.session.commit()
    elif category[0] == 'Infanto Juvenil 1' or category[0] == 'Infanto Juvenil 2':
        for belt in belts[1:5]:
            age_division_belt = Age_division_belt(belt=belt, age_division=category_1)
            db.session.add(age_division_belt)
            db.session.commit()
    elif category[0] == 'Juvenil':
        for belt in belts[5:7]:
            age_division_belt = Age_division_belt(belt=belt, age_division=category_1)
            db.session.add(age_division_belt)
            db.session.commit()
    elif category[0] == 'Adulto' or category[0] == 'Master':
        for belt in belts[5:9]:
            age_division_belt = Age_division_belt(belt=belt, age_division=category_1)
            db.session.add(age_division_belt)
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
genders = db.session.query(Gender).all()
age_division = db.session.query(Age_division).order_by(Age_division.id).all()
x=0
for peso in pesos:
    if age_division[x].name != 'Adulto' and age_division[x].name != 'Master':
        for key, value in peso.items():
            row = Weight(name=key, weight=value, kimono=False)
            db.session.add(row)
            for gender in genders:
                row_1 = Weight_age_division_gender(weight=row, gender=gender, age_division=age_division[x])
                db.session.add(row_1)
                db.session.commit()
        x += 1
    elif age_division[x].name == 'Adulto':
        for key, value in peso.items():
            row = Weight(name=key, weight=value, kimono=False)
            db.session.add(row)
            row_1 = Weight_age_division_gender(weight=row, gender=genders[0], age_division=age_division[x])
            row_2 = Weight_age_division_gender(weight=row, gender=genders[0], age_division=age_division[x+1])
            db.session.add(row_1)
            db.session.add(row_2)
            db.session.commit()
        x += 1 
    elif age_division[x].name == 'Master':
        for key, value in peso.items():
            row = Weight(name=key, weight=value, kimono=False)
            db.session.add(row)
            row_1 = Weight_age_division_gender(weight=row, gender=genders[1], age_division=age_division[x-1])
            row_2 = Weight_age_division_gender(weight=row, gender=genders[1], age_division=age_division[x])
            db.session.add(row_1)
            db.session.add(row_2)
            db.session.commit()



# infanto1 = {'Pluma':14.99, 'Pena':17.99, 'Leve':20.99, 'Medio':23.99, 'Medio-Pesado':26.99, 'Pesado':29.99, 'Super Pesado':32.99, 'Pessadissimo':33}
# infanto2 = {'Pluma':18.99, 'Pena':21.99, 'Leve':24.99, 'Medio':27.99, 'Medio-Pesado':30.99, 'Pesado':33.99, 'Super Pesado':36.99, 'Pessadissimo':37}
# infanto3 = {'Pluma':24.99, 'Pena':27.99, 'Leve':30.99, 'Medio':33.99, 'Medio-Pesado':36.99, 'Pesado':39.99, 'Super Pesado':42.99, 'Pessadissimo':43}
# infanto4 = {'Gallo':27.99, 'Pluma':30.99, 'Pena':33.99, 'Leve':36.99, 'Medio':39.99, 'Medio-Pesado':42.99, 'Pesado':45.99, 'Super Pesado':48.99, 'Pessadissimo':49}
# infanto_juvenil1 = {'Gallo':33.99, 'Pluma':37.99, 'Pena':40.99, 'Leve':44.99, 'Medio':49.99, 'Medio-Pesado':53.99, 'Pesado':57.99, 'Super Pesado':61.99, 'Pessadissimo':62, 'Absoluto':1000 }
# infanto_juvenil2 = {'Gallo':41.99, 'Pluma':45.99, 'Pena':49.99, 'Leve':53.99, 'Medio':57.99, 'Medio-Pesado':61.99, 'Pesado':65.99, 'Super Pesado':69.99, 'Pessadissimo':70, Absoluto':1000}
# juvenil = {'Gallo':50.99, 'Pluma':55.99, 'Pena':60.99, 'Leve':65.99, 'Medio':70.99, 'Medio-Pesado':75.99, 'Pesado':80.99, 'Super Pesado':85.99, 'Pessadissimo':86, 'Absoluto':1000}
# masculino = {'Gallo':54.99, 'Pluma':60.99, 'Pena':66.99, 'Leve':72.99, 'Medio':78.99, 'Medio-Pesado':84.99, 'Pesado':90.99, 'Super Pesado':96.99, 'Pessadissimo':97, 'Absoluto':1000}
# femenino = {'Gallo':45.99, 'Pluma':50.99, 'Pena':55.99, 'Leve':60.99, 'Medio':65.99, 'Medio-Pesado':70.99, 'Pesado':75.99, 'Super Pesado':80.99, 'Pessadissimo':81, 'Absoluto':1000}






# x = 0
# age_divisions = db.session.query(Age_division).order_by(Age_division.id).all()






# age_divisions = db.session.query(Age_division.id, Age_division.name).all()
# genders = db.session.query(Gender.id, Gender.name).all()

# for age_division in age_divisions:
#     for belt in db.session.query(Belt.id, Belt.name).join(Age_division_belt).filter(Age_division_belt.age_division_id == age_division[0]).all():
#         for gender in genders:
#             for weight in db.session.query(Weight.id, Weight.name).join(Weight_age_division_gender).filter(Weight_age_division_gender.age_division_id == age_division[0], Weight_age_division_gender.gender_id == gender[0]).all():
#                 atletas = db.session.query(Atleta.name, Academy.name).join(Registration.atleta).join(Atleta.academy).filter(Atleta.gender_id == gender[0], Atleta.belt_id == belt[0], Registration.age_division_id == age_division[0], Atleta.gender_id == gender[0], Registration.weight_id == weight[0], Atleta.id == Registration.atleta_id).all()
#                 if atletas == []:
#                     print(f"[{age_division}, {belt}, {weight}, {gender}]: {atletas}") 




# atletas = db.session.query(Atleta.name, Academy.name).join(Registration.atleta).join(Atleta.academy).filter(Atleta.gender_id == 2, Atleta.belt_id == 9, Registration.age_division_id == 9, Atleta.gender_id == 2, Registration.weight_id == 80, Atleta.id == Registration.atleta_id).all()


# dicts = {}
# for age_division in age_divisions:
#     dicts[age_division[1]] = {}
#     for belt in db.session.query(Belt.id, Belt.name).join(Age_division_belt).filter(Age_division_belt.age_division_id == age_division[0]).all():
#         for gender in genders:
#             for weight in db.session.query(Weight.id, Weight.name).join(Weight_age_division_gender).filter(Weight_age_division_gender.age_division_id == age_division[0], Weight_age_division_gender.gender_id == gender[0]).all():
#                 atletas = db.session.query(Atleta.name, Academy.name).join(Registration.atleta).join(Atleta.academy).filter(Atleta.gender_id == gender[0], Atleta.belt_id == belt[0], Registration.age_division_id == age_division[0], Atleta.gender_id == gender[0], Registration.weight_id == weight[0], Atleta.id == Registration.atleta_id).all()
#                 if atletas == []:
#                     print(f"[{age_division}, {belt}, {weight}, {gender}]: {atletas}") 

# dicts = {}
# belt_dicts = {}
# gender_dicts = {}
# weight_dicts = {}
# belts = db.session.query(Belt.name).all()
# weights = db.session.query(Weight.id, Weight.name).all()
# age_divisions = db.session.query(Age_division.id, Age_division.name).order_by(Age_division.id).all()
# genders = db.session.query(Gender.id, Gender.name).all()

# for age_division in age_divisions:
#     dicts[age_division[1]] = {}
#     for belt in db.session.query(Belt.id, Belt.name).join(Age_division_belt).filter(Age_division_belt.age_division_id == age_division[0]).all():
#         belt_dicts[belt[1]] = {}
#         for gender in genders:
#             gender_dicts[gender[1]] = {}
#             for weight in db.session.query(Weight.id, Weight.name).join(Weight_age_division_gender).filter(Weight_age_division_gender.age_division_id == age_division[0], Weight_age_division_gender.gender_id == gender[0]).all():
#                 atletas = db.session.query(Atleta.name, Academy.name).join(Registration.atleta).join(Atleta.academy).filter(Atleta.gender_id == gender[0], Atleta.belt_id == belt[0], Registration.age_division_id == age_division[0], Atleta.gender_id == gender[0], Registration.weight_id == weight[0], Atleta.id == Registration.atleta_id).all()
#                 weight_dicts[weight[1]] = atletas
#             gender_dicts[gender[1]] = weight_dicts
#             weight_dicts = {}
#         belt_dicts[belt[1]] = gender_dicts
#         gender_dicts = {}
#     dicts[age_division[1]] = belt_dicts
#     belt_dicts = {}

