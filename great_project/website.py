from flask import render_template, request, url_for, flash, redirect

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

@app.route('/registrarse')
def registrarse():
    
    return render_template('registrarse.html', page_title="Calendario")


