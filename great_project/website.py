from flask import render_template, request, url_for, flash, redirect, flash
from great_project import app
from great_project.forms import  RegistrationForm, LoginForm
from flaskblog.models import Atleta, Academia, Belt, Gender, Event, Order, Weight, Category

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', page_title="My great website")

@app.route('/calendario')
def calendario():
    return render_template('calendario.html', page_title="Calendario")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('Has iniciado sesion!', 'success')
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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Cuenta creada para{form.nombre.data} {form.apellido.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('registrarse.html', page_title="Calendario", form=form)


