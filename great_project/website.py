from flask import render_template, request, url_for, flash, redirect, flash
from great_project import app, db, bcrypt
from great_project.forms import  RegistrationForm, LoginForm
from great_project.models import Atleta, Academia, Belt, Gender, Event, Order, Weight, Category
from flask_login import login_user, current_user, logout_user

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', page_title="My great website")

@app.route('/calendario')
def calendario():
    return render_template('calendario.html', page_title="Calendario")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Atleta.query.filter_by(email=form.email.data.upper()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Inicio de sesion invalido. Porfavor revisa tu correo electronico y contraseña')
    return render_template('login.html', page_title="Calendario", form=form)

@app.route('/evento1')
def evento1():
    return render_template('evento1.html', page_title="Calendario")

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
        print(form.gender.data.upper())
        print(gender_choice)
        belt_choice = Belt.query.filter_by(name=form.belt.data.upper()).first()
        print(form.belt.data.upper())
        print(belt_choice)
        academia_choice = Academia.query.filter_by(name=form.academia.data).first()
        print(form.academia.data.upper())
        print(academia_choice)
        user = Atleta(name = form.name.data.upper(), apellido = form.apellido.data.upper(), year=int(form.year.data), month = form.year.data, 
                    day = int(form.day.data), gender = gender_choice, email = form.email.data.upper(), nacionalidad = form.nacionalidad.data.upper(), 
                    direccion = form.direccion.data.upper(), provincia = form.provincia.data.upper(), pais = form.pais.data.upper(), 
                    telefono = form.telefono.data, 
                    belt = belt_choice, 
                    academia = academia_choice, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Tu cuenta ha sido creada', 'success')
        return redirect(url_for('index'))
    return render_template('registrarse.html', page_title="Calendario", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



