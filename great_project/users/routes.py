from flask import render_template, request, url_for, redirect, flash, request, Blueprint
from great_project import db, bcrypt, login_manager
import datetime
from datetime import date
from flask_login import current_user, login_user, logout_user, login_required
from great_project.users.forms import RegistrationForm, LoginForm, AcademyRegistration, UpdateAccount, RequestResetFrom, ResetPasswordForm
from great_project.models import Asociation, Atleta, Academy, Belt, Gender, Asociation
from great_project.users.utils import send_reset_email, belt_choices, generate_confirmation_token, confirm_token, send_email

# login manager to know the current user


@login_manager.user_loader
def load_user(atleta_id):
    return Atleta.query.get(int(atleta_id))


# set blueprints for user routes
users = Blueprint('users', __name__)

# route for the users to update their info


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccount()
    form.academy.choices = [(academy.id, academy.name)
                            for academy in Academy.query.all()]
    form.academy.choices.insert(0, ('Academia', 'Academia'))
    form.belt.choices = [(belt.id, belt.name) for belt in belt_choices().all()]
    form.belt.choices.insert(0, ('Cinturon', 'Cinturon'))

    # validate the form on submit
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
    # display current info
    elif request.method == 'GET':
        atleta_belt = Belt.query.filter_by(id=current_user.belt_id).first()
        atleta_academy = Academy.query.filter_by(
            id=current_user.academy_id).first()
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.province.data = current_user.province
        form.country.data = current_user.country
        form.phone.data = current_user.phone
        form.belt.data = atleta_belt
        form.academy.data = atleta_academy
    return render_template('account.html', page_title="Cuenta", form=form)

# route to login


@users.route('/login', methods=['GET', 'POST'])
def login():
    # don't allow users to access this route if they are already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    # validate the form on submit
    if form.validate_on_submit():
        user = Atleta.query.filter_by(email=form.email.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Hola {current_user.name}, has iniciado sesion', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash(
                'Inicio de sesion invalido. Porfavor revisa tu correo electronico y contraseña', 'danger')
    return render_template('login.html', page_title="Iniciar Sesion", form=form)

# route for the users to create a new account


@users.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()

    # create academy options from the database
    form.academy.choices = [(academy.name, academy.name)
                            for academy in Academy.query.all()]

    # validate the form on submit
    if form.validate_on_submit():
        # hash the password
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        gender_choice = Gender.query.filter_by(name=form.gender.data).first()
        belt_choice = Belt.query.filter_by(name=form.belt.data).first()
        academy_choice = Academy.query.filter_by(
            name=form.academy.data).first()
        date = datetime.date(int(form.year.data), (int(
            form.month.data)+1), int(form.day.data))

        # add new user to the database
        atleta = Atleta(name=form.name.data, last_name=form.last_name.data, birth_date=date, gender=gender_choice,
                        email=form.email.data.lower(), nacionality=form.nacionality.data.upper(),
                        address=form.address.data.upper(), province=form.province.data.upper(), country=form.country.data,
                        phone=form.phone.data, city=form.city.data.upper(), cedula=form.cedula.data, atleta_conf=form.atleta_conf.data,
                        belt=belt_choice, profesor_conf=form.profesor_conf.data, academy=academy_choice, password=hashed_password, confirmed=False)
        db.session.add(atleta)
        db.session.commit()
        print(atleta.email)
        token = generate_confirmation_token(atleta.email)
        print(token)
        confirm_url = url_for('users.confirm_email',
                              token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(atleta.email, subject, html)
        flash('Se ha enviado un correo de confirmacion via email', 'success')
        return redirect(url_for('users.login'))
    return render_template('registrarse.html', page_title="Registrarse", form=form)


@users.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
        print(email)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = Atleta.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('Tu cuenta ha sido confirmada, ahora puedes iniciar sesion!', 'success')
    return redirect(url_for('users.login'))


# route to logout
@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesion', 'warning')
    return redirect(url_for('main.index'))

# route to request for a reset password link in case they have forgotten the password


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    # allow only users that are not logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetFrom()

    # validate the form on submit
    if form.validate_on_submit():
        atleta = Atleta.query.filter_by(email=form.email.data).first()

        # call the dunction to send email from utils.py
        send_reset_email(atleta)
        flash('Se ha enviado un email con las instrucciones para reestablecer tu contraseña', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', page_title='Reestablecer contraseña', form=form)

# route to reset the password, opened from mail


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    # allow only users that are not logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    # verify that the token is valid or hasn't expired
    atleta = Atleta.verify_reset_token(token)

    # If token is invalid or expired redirect them to request for a new one
    if atleta is None:
        flash('Este token es invalido o ya ha expirado', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()

    # validate the form on submit
    if form.validate_on_submit():
        # create new hashed password
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        atleta.password = hashed_password
        db.session.commit()
        flash('Tu contraseña ha sido actualizada!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', page_title='Reestablecer contraseña', form=form)

# route for teachers/academy owners to register their academy


@users.route('/academy_reg', methods=['GET', 'POST'])
@login_required
def academy_reg():
    form = AcademyRegistration()
    form.asociation.choices = [(asociation.name, asociation.name)
                               for asociation in Asociation.query.all()]
    user = Atleta.query.filter_by(id=current_user.id).first()
    # validate the form on submit
    if form.validate_on_submit():
        user.academy_registered = True
        asociation_choice = Asociation.query.filter_by(
            name=form.asociation.data).first()
        academy = Academy(asociation_id=asociation_choice.id, name=form.name.data, province=form.province.data.upper(
        ), country=form.country.data, city=form.city.data.upper())
        db.session.add(academy)
        db.session.add(user)
        db.session.commit()
        flash(
            f'La academia {form.name.data} ha sido registrada con exito', 'success')
        return redirect(url_for('main.index'))
    return render_template('academy_reg.html', page_title="Registrar Academia", form=form)


@users.route('/admin')
@login_required
def admin():
    if current_user.is_admin:
        return render_template('users.admin.html', page_title="Admin")
    else:
        return render_template('main.index.html', page_title="Inicio")
