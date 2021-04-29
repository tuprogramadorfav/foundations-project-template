from flask import render_template, request, url_for, flash, redirect, flash, request
from great_project import app, db, bcrypt
from great_project.forms import  RegistrationForm, LoginForm, EventRegistration, AcademyRegistration, UpdateAccount
from great_project.models import Atleta, Academia, Belt, Gender, Event, Registration, Weight, Age_division
from flask_login import login_user, current_user, logout_user, login_required


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
        current_user.email = form.email.data.upper()
        current_user.direccion = form.direccion.data.upper()
        current_user.provincia = form.provincia.data.upper()
        current_user.pais = form.pais.data.upper()
        current_user.telefono = form.telefono.data.upper()
        current_user.belt = form.belt.data.upper()
        current_user.academia = form.academia.data.upper()
        db.session.commit()
        flash('Tu cuenta ha sido actualizada!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.direccion.data = current_user.direccion
        form.provincia.data = current_user.provincia
        form.pais.data = current_user.pais
        form.telefono.data = current_user.telefono
        form.belt.data= current_user.belt
        form.academia.data = current_user.academia
    return render_template('account.html', page_title="Calendario", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Atleta.query.filter_by(email=form.email.data.upper()).first()
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

@app.route('/event_reg1')
@login_required
def event_reg1():
    beltId = current_user.belt_id
    belt = Belt.query.filter_by(id=beltId).first()
    academiaId = current_user.academia_id
    academia = Academia.query.filter_by(id=academiaId).first()
    form = EventRegistration()
    return render_template('event_reg.html', page_title="Calendario", form=form, belt=belt.name, academia=academia.name)

@app.route('/rankingaca')
def rankingaca():
    return render_template('rankingaca.html', page_title="Calendario")

@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    form.academia.choices = [(academia.name, academia.name) for academia in Academia.query.all()]
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        gender_choice = Gender.query.filter_by(name=form.gender.data.upper()).first()
        belt_choice = Belt.query.filter_by(name=form.belt.data.upper()).first()
        academia_choice = Academia.query.filter_by(name=form.academia.data).first()
        atleta = Atleta(name = form.name.data.upper(), apellido = form.apellido.data.upper(), year=int(form.year.data), month = form.year.data, 
                    day = int(form.day.data), gender = gender_choice, email = form.email.data.upper(), nacionalidad = form.nacionalidad.data.upper(), 
                    direccion = form.direccion.data.upper(), provincia = form.provincia.data.upper(), pais = form.pais.data.upper(), 
                    telefono = form.telefono.data, ciudad = form.ciudad.data.upper(), cedula = form.cedula.data, atleta_conf = form.atleta_conf.data,
                    belt = belt_choice, profesor_conf = form.profesor_conf.data, academia = academia_choice, password = hashed_password)
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



