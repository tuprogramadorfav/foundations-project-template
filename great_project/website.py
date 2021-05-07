from flask import render_template, request, url_for, flash, redirect, flash, request, jsonify, json
from great_project import app, db, bcrypt, login_manager
from great_project.forms import  RegistrationForm, LoginForm, EventRegistration, AcademyRegistration, UpdateAccount
from great_project.models import Atleta, Academy, Belt, Gender, Event, Registration, Weight, Age_division, Weight_age_division_gender, Age_division_belt
from flask_login import login_user, current_user, logout_user, login_required
import datetime
from datetime import date


@login_manager.user_loader
def load_user(atleta_id):
    return Atleta.query.get(int(atleta_id))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', page_title="My great website")

@app.route('/calendario')
def calendario():
    return render_template('calendario.html', page_title="Calendario")

@app.route('/admin')
@login_required
def admin():
    if current_user.is_admin:
        return render_template('admin.html', page_title="Calendario")
    else:
        return render_template('index.html', page_title="My great website")

def belt_choices():
    current_year = date.today().year
    age = current_year - current_user.birth_date.year
    return db.session.query(Belt).join(Age_division_belt).join(Age_division).filter(Age_division.initial_age <= age, Age_division.top_age >= age)

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccount()
    form.academy.choices = [(academy.name, academy.name) for academy in Academy.query.all()]
    form.academy.choices.insert(0, ('Academia', 'Academia'))
    form.belt.choices = [(belt.id, belt.name) for belt in belt_choices().all()]
    form.belt.choices.insert(0, ('Cinturon', 'Cinturon'))
    if form.validate_on_submit():
        current_user.email = form.email.data.lower()
        current_user.address = form.address.data
        current_user.province = form.province.data
        current_user.country = form.country.data
        current_user.phone = form.phone.data
        current_user.belt = form.belt.data
        current_user.academy = form.academy.data
        db.session.commit()
        flash('Tu cuenta ha sido actualizada!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.province.data = current_user.province
        form.country.data = current_user.country
        form.phone.data = current_user.phone
        form.belt.data = current_user.belt
        form.academy.data = current_user.academy
    return render_template('account.html', page_title="Calendario", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Atleta.query.filter_by(email=form.email.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Hola {current_user.name}, has iniciado sesion', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Inicio de sesion invalido. Porfavor revisa tu correo electronico y contraseña')
    return render_template('login.html', page_title="Calendario", form=form)

@app.route('/evento1')
def evento1():
    return render_template('evento1.html', page_title="Calendario")



def age_division_choices():
    current_year = date.today().year
    age = current_year - current_user.birth_date.year
    return Age_division.query.filter(Age_division.initial_age <= age, Age_division.top_age >= age)

@app.route('/event_reg1', methods=['GET', 'POST'])
@login_required
def event_reg1():
    event = Event.query.filter_by(id=1).first()
    beltId = current_user.belt_id
    belt = Belt.query.filter_by(id=beltId).first()
    academyId = current_user.academy_id
    academy = Academy.query.filter_by(id=academyId).first()
    form = EventRegistration()
    form.age_division.choices = [(age_division.id, age_division.name) for age_division in age_division_choices().all()]
    form.age_division.choices.insert(0, ('Division de Edad', 'Division de Edad'))
    if form.validate_on_submit():
        registration = Registration(atleta_id=current_user.id, event_id=event.id, age_division_id=form.age_division.data, weight_id=form.weight.data)
        db.session.add(registration)
        db.session.commit()
        flash(f'Te has registrado para la {event.name}', 'success')
        return redirect(url_for('index'))
    return render_template('event_reg.html', page_title="Calendario", form=form, belt=belt.name, academia=academy.name)

@app.route('/weight/<age_division>')
def weight(age_division):
    print(age_division)
    weightArray = []
    weights = db.session.query(Weight).join(Weight_age_division_gender).join(Age_division).join(Gender).filter(Age_division.id == age_division, Gender.id == current_user.gender_id).all()

    for weight in weights:
        weightObj = {}
        weightObj['id'] = weight.id
        weightObj['name'] = f"{weight.name}: {weight.weight}kg"
        weightArray.append(weightObj)

    return jsonify({'weights': weightArray})

@app.route('/atletas_table')
def atletas_table():
    headers = ['Nombre', 'Equipo']
    event_id = db.session.query(Event).filter_by(id=1).first()
    belts = db.session.query(Belt.name).all()
    weights = db.session.query(Weight.id, Weight.name).all()
    age_divisions = db.session.query(Age_division.id, Age_division.name).order_by(Age_division.id).all()
    genders = db.session.query(Gender.id, Gender.name).all()
    dicts = {}
    belt_dicts = {}
    gender_dicts = {}
    weight_dicts = {}
    tables = []
    for age_division in age_divisions:
        dicts[age_division[1]] = {}
        for belt in db.session.query(Belt.id, Belt.name).join(Age_division_belt).filter(Age_division_belt.age_division_id == age_division[0]).all():
            belt_dicts[belt[1]] = {}
            for gender in genders:
                gender_dicts[gender[1]] = {}
                for weight in db.session.query(Weight.id, Weight.name).join(Weight_age_division_gender).filter(Weight_age_division_gender.age_division_id == age_division[0], Weight_age_division_gender.gender_id == gender[0]).all():
                    atletas = db.session.query(Atleta.name, Academy.name).join(Registration.atleta).join(Atleta.academy).filter(Atleta.gender_id == gender[0], Atleta.belt_id == belt[0], Registration.age_division_id == age_division[0], Atleta.gender_id == gender[0], Registration.weight_id == weight[0], Atleta.id == Registration.atleta_id).all()
                    weight_dicts[weight[1]] = atletas
                gender_dicts[gender[1]] = weight_dicts
                weight_dicts = {}
            belt_dicts[belt[1]] = gender_dicts
            gender_dicts = {}
        dicts[age_division[1]] = belt_dicts
        belt_dicts = {} 

    return render_template('atletas_table.html', page_title="Calendario", headers=headers, dicts=dicts)

# belts=belts, age_divisions=age_divisions, gender=genders, weights=weights, atletas=atletas, headers=headers
@app.route('/rankingaca')
def rankingaca():
    return render_template('rankingaca.html', page_title="Calendario")

@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    form.academy.choices = [(academy.name, academy.name) for academy in Academy.query.all()]
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        gender_choice = Gender.query.filter_by(name=form.gender.data).first()
        belt_choice = Belt.query.filter_by(name=form.belt.data).first()
        academy_choice = Academy.query.filter_by(name=form.academy.data).first()
        date = datetime.date(int(form.year.data), (int(form.month.data)+1), int(form.day.data))
        atleta = Atleta(name = form.name.data, last_name = form.last_name.data, birth_date=date, gender = gender_choice, 
                    email = form.email.data.lower(), nacionality = form.nacionality.data.upper(), 
                    address = form.address.data.upper(), province = form.province.data.upper(), country = form.country.data, 
                    phone = form.phone.data, city = form.city.data.upper(), cedula = form.cedula.data, atleta_conf = form.atleta_conf.data,
                    belt = belt_choice, profesor_conf = form.profesor_conf.data, academy = academy_choice, password = hashed_password)
        db.session.add(atleta)
        db.session.commit()
        flash('Tu cuenta ha sido creada', 'success')
        return redirect(url_for('index'))
    return render_template('registrarse.html', page_title="Calendario", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/create_academy')
@login_required
def create_academy():
    form = AcademyRegistration()
    if form.validate_on_submit():
        atleta = Academy(name = form.name.data, province = form.province.data.upper(), country = form.country.data, city = form.city.data.upper())
        db.session.add(academy)
        db.session.commit()
        flash(f'La academia {form.name.data} ha sido registrada con exito', 'success')
        return redirect(url_for('index'))
    return render_template('academy_reg.html', page_title="Calendario", form=form)
