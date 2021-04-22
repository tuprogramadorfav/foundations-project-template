from flask import render_template, request, url_for, flash, redirect, flash
from great_project.forms import  RegistrationForm, LoginForm
from great_project import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', page_title="My great website")

@app.route('/calendario')
def calendario():
    return render_template('calendario.html', page_title="Calendario")

@app.route('/login')
def login():
    return render_template('login.html', page_title="Calendario")

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


