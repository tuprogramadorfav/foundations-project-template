from great_project import db
from great_project.models import Atleta, Academia, Belt, Gender, Event, Order, Weight, Category, category_belt, category_weight

infanto1 = {'Pluma':14.99, 'Pena':17.99, 'Leve':20.99, 'Medio':23.99, 'Medio-Pesado':26.99, 'Pesado':29.99, 'Super Pesado':32.99, 'Pessadissimo':33}
infanto2 = {'Pluma':18.99, 'Pena':21.99, 'Leve':24.99, 'Medio':27.99, 'Medio-Pesado':30.99, 'Pesado':33.99, 'Super Pesado':36.99, 'Pessadissimo':37}
infanto3 = {'Pluma':24.99, 'Pena':27.99, 'Leve':30.99, 'Medio':33.99, 'Medio-Pesado':36.99, 'Pesado':39.99, 'Super Pesado':42.99, 'Pessadissimo':43}
infanto4 = {'Gallo':27.99, 'Pluma':30.99, 'Pena':33.99, 'Leve':36.99, 'Medio':39.99, 'Medio-Pesado':42.99, 'Pesado':45.99, 'Super Pesado':48.99, 'Pessadissimo':49}
infanto_juvenil1 = {'Gallo':33.99, 'Pluma':37.99, 'Pena':40.99, 'Leve':44.99, 'Medio':49.99, 'Medio-Pesado':53.99, 'Pesado':57.99, 'Super Pesado':61.99, 'Pessadissimo':62, 'Absoluto':1000 }
infanto_juvenil2 = {'Gallo':41.99, 'Pluma':45.99, 'Pena':49.99, 'Leve':53.99, 'Medio':57.99, 'Medio-Pesado':61.99, 'Pesado':65.99, 'Super Pesado':69.99, 'Pessadissimo':70, , 'Absoluto':1000}
juvenil = {'Gallo':50.99, 'Pluma':55.99, 'Pena':60.99, 'Leve':65.99, 'Medio':70.99, 'Medio-Pesado':75.99, 'Pesado':80.99, 'Super Pesado':85.99, 'Pessadissimo':86, , 'Absoluto':1000}
masculino = {'Gallo':54.99, 'Pluma':60.99, 'Pena':66.99, 'Leve':72.99, 'Medio':78.99, 'Medio-Pesado':84.99, 'Pesado':90.99, 'Super Pesado':96.99, 'Pessadissimo':97, 'Absoluto':1000}
femenino = {'Gallo':45.99, 'Pluma':50.99, 'Pena':55.99, 'Leve':60.99, 'Medio':65.99, 'Medio-Pesado':70.99, 'Pesado':75.99, 'Super Pesado':80.99, 'Pessadissimo':81, 'Absoluto':1000}

genders = [1,2]

categories = [['Infanto 1', 4, 5], ['Infanto 2', 6, 7], ['Infanto 3', 8, 9], ['Infanto 4', 10, 11], ['Infanto Juvenil 1', 12, 13], ['Infanto Juvenil 2', 14, 15], ['Juvenil', 16, 17], ['Adulto', 18, 80], ['Master', 30, 80]]
for category in categories:
    category_1 = Category(name = category[0], initial_age = category[1], top_age = category[2])
    db.session.add(category_1)
    db.session.commit()

belts = ['Blanco', 'Gris', 'Amarillo', 'Naranja', 'Verde', 'Azul', 'Violeta', 'Marron', 'Negro']

for belt in belts:
    belt_1 = Belt(name=belt)
    db.session.add(belt_1)
    db.session.commit()

for genero in genders:
    for nombre, value in infanto1:
        peso = Weight(name = nombre, weight = value, kimono = True, gender_id = genero)
        db.session.add(peso)
        db.session.commit()