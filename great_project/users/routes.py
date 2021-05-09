from flask import render_template, request, url_for, redirect, flash, request, Blueprint
from great_project import db, bcrypt, login_manager
import datetime
from datetime import date
from flask_login import current_user, login_user, logout_user, login_required
from great_project.users.forms import  RegistrationForm, LoginForm, AcademyRegistration, UpdateAccount, RequestResetFrom, ResetPasswordForm
from great_project.models import Atleta, Academy, Belt, Gender, Event, Registration, Weight, Age_division
from great_project.users.utils import send_reset_email, belt_choices

@login_manager.user_loader
def load_user(atleta_id):
    return Atleta.query.get(int(atleta_id))

users = Blueprint('users', __name__)

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccount()
    form.academy.choices = [(academy.id, academy.name) for academy in Academy.query.all()]
    form.academy.choices.insert(0, ('Academia', 'Academia'))
    form.belt.choices = [(belt.id, belt.name) for belt in belt_choices().all()]
    form.belt.choices.insert(0, ('Cinturon', 'Cinturon'))
    if form.validate_on_submit():
        belt_choice = Belt.query.filter_by(id=form.belt.data).first()
        academy_choice = Academy.query.filter_by(id=form.academy.data).first()
        current_user.email = form.email.data.lower()
        current_user.address = form.address.data
        current_user.province = form.province.data
        current_user.country = form.country.data
        current_user.phone = form.phone.data
        current_user.belt = belt_choice
        current_user.academy = academy_choice
        db.session.commit()
        flash('Tu cuenta ha sido actualizada!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        atleta_belt = Belt.query.filter_by(id=current_user.belt_id).first()
        print(atleta_belt)
        atleta_academy = Academy.query.filter_by(id=current_user.academy_id).first()
        print(atleta_academy)
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.province.data = current_user.province
        form.country.data = current_user.country
        form.phone.data = current_user.phone
        form.belt.data = atleta_belt
        form.academy.data = atleta_academy
    return render_template('account.html', page_title="Calendario", form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Atleta.query.filter_by(email=form.email.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Hola {current_user.name}, has iniciado sesion', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Inicio de sesion invalido. Porfavor revisa tu correo electronico y contraseña', 'danger')
    return render_template('login.html', page_title="Calendario", form=form)

@users.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
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
        return redirect(url_for('users.login'))
    return render_template('registrarse.html', page_title="Calendario", form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesion', 'warning')
    return redirect(url_for('main.index'))


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetFrom()
    if form.validate_on_submit():
        atleta = Atleta.query.filter_by(email=form.email.data).first()
        send_reset_email(atleta)
        flash('Se ha enviado un email con las instrucciones para reestablecer tu contraseña', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', page_title='Reset Password', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    atleta = Atleta.verify_reset_token(token)
    print(atleta)
    if atleta is None:
        flash('Este token es invalido o ya ha expirado', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        atleta.password = hashed_password
        db.session.commit()
        flash('Tu contraseña ha sido actualizada!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', page_title='Reset Password', form=form)

@users.route('/academy_reg', methods=['GET', 'POST'])
@login_required
def academy_reg():
    form = AcademyRegistration()
    if form.validate_on_submit():
        academy = Academy(name = form.name.data, province = form.province.data.upper(), country = form.country.data, city = form.city.data.upper())
        db.session.add(academy)
        db.session.commit()
        flash(f'La academia {form.name.data} ha sido registrada con exito', 'success')
        return redirect(url_for('main.index'))
    return render_template('academy_reg.html', page_title="Calendario", form=form)

@users.route('/admin')
@login_required
def admin():
    if current_user.is_admin:
        return render_template('users.admin.html', page_title="Calendario")
    else:
        return render_template('main.index.html', page_title="My great website")