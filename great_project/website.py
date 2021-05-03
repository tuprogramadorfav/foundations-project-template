from flask import render_template, request, url_for, flash, redirect, flash, request, jsonify, json
from great_project import app, db, bcrypt, login_manager
from great_project.forms import  RegistrationForm, LoginForm, EventRegistration, AcademyRegistration, UpdateAccount
from great_project.models import Atleta, Academy, Belt, Gender, Event, Registration, Weight, Age_division, Weight_age_division_gender
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

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccount()
    if form.validate_on_submit():
        current_user.email = form.email.data.lower()
        current_user.address = form.address.data.upper()
        current_user.provincia = form.provincia.data.upper()
        current_user.pais = form.pais.data.upper()
        current_user.telefono = form.telefono.data.upper()
        current_user.belt = form.belt.data.upper()
        current_user.academy = form.academy.data.upper()
        db.session.commit()
        flash('Tu cuenta ha sido actualizada!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.provincia.data = current_user.provincia
        form.pais.data = current_user.pais
        form.telefono.data = current_user.telefono
        form.belt.data= current_user.belt
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
    belts = db.session.query(Belt.id).all()
    age_divisions = db.session.query(Age_division.id).all()
    genders = db.session.query(Gender.id).all()
    weights = db.session.query(Weight.id).all()
    tables = []
    atletas = db.session.query(Atleta.name, Atleta.academy).join(Registration.event).join(Registration.atleta).join(Registration.age_division).join(Atleta.belt).join(Registration.weight).join(Atleta.gender).filter(event_id == event_id.id, Gender.id == gender.id, Weight.id == weight.id, Age_division.id == age_division.id, Belt.id == belt.id).all()

    return render_template('atletas_table.html', page_title="Calendario", tables=tables, headers=headers)

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



