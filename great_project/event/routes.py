from flask import render_template, request, url_for, redirect, flash, request, jsonify, json, Blueprint
from flask_login import current_user, login_required
from great_project import db, login_manager
from great_project.event.forms import  EventRegistration
from great_project.models import Atleta, Academy, Belt, Gender, Event, Age_division, Registration, Weight, Weight_age_division_gender, Age_division_belt
from great_project.event.utils import age_division_choices

@login_manager.user_loader
def load_user(atleta_id):
    return Atleta.query.get(int(atleta_id))

event = Blueprint('event', __name__)

@event.route('/evento1')
def evento1():
    return render_template('evento1.html', page_title="Evento")


@event.route('/event_reg1', methods=['GET', 'POST'])
@login_required
def event_reg1():
    print(current_user)
    event = Event.query.filter_by(id=1).first()
    print(event) 
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
        return redirect(url_for('main.index'))
    return render_template('event_reg.html', page_title="Inscripciones", form=form, belt=belt.name, academia=academy.name)

@event.route('/weight/<age_division>')
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

@event.route('/atletas_table')
def atletas_table():
    headers = ['Nombre', 'Academia']
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
                    atletas = db.session.query(Atleta.name, Academy.name).join(Registration.atleta).join(Atleta.academy).filter(Atleta.gender_id == gender[0], Atleta.belt_id == belt[0], Registration.age_division_id == age_division[0], Atleta.gender_id == gender[0], Registration.weight_id == weight[0], Atleta.id == Registration.atleta_id, Registration.event_id == 1).all()
                    weight_dicts[weight[1]] = atletas
                gender_dicts[gender[1]] = weight_dicts
                weight_dicts = {}
            belt_dicts[belt[1]] = gender_dicts
            gender_dicts = {}
        dicts[age_division[1]] = belt_dicts
        belt_dicts = {} 

    return render_template('atletas_table.html', page_title="Lista de atletas por Division", headers=headers, dicts=dicts)

@event.route('/atletas_team')
def atletas_team():
    dicts = {}
    academies = db.session.query(Academy.id, Academy.name).all()
    for academy in academies:
        atletas = db.session.query(Atleta.name, Belt.name, Age_division.name, Gender.name, Weight.name).join(Registration.atleta).join(Atleta.academy).join(Atleta.belt).join(Registration.age_division).join(Atleta.gender).join(Registration.weight).filter(Atleta.id == Registration.atleta_id, Atleta.academy_id == academy[0], Registration.event_id == 1).order_by(Belt.id, Age_division.id, Gender.id, Weight.id).all()
        dicts[academy[1]] = atletas
    
    return render_template('atletas_team.html', page_title="Lista de Atletas por Equipo",  dicts=dicts)

@event.route('/weights_nogi')
def weights_nogi():
    return render_template('weights_nogi.html', page_title="Pesos")

@event.route('/weight_in')
def weight_in():
    return render_template('weight_in.html', page_title="Pesaje")


@event.route('/ranking_atl')
def ranking_atl():
    headers = ['Nombre', 'Academia', 'Puntos']
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
                    atletas = db.session.query(Atleta.name, Academy.name, Atleta.points).join(Registration.atleta).join(Atleta.academy).filter(Atleta.gender_id == gender[0], Atleta.belt_id == belt[0], Registration.age_division_id == age_division[0], Atleta.gender_id == gender[0], Registration.weight_id == weight[0], Atleta.id == Registration.atleta_id).order_by(Atleta.points).all()
                    weight_dicts[weight[1]] = atletas
                gender_dicts[gender[1]] = weight_dicts
                weight_dicts = {}
            belt_dicts[belt[1]] = gender_dicts
            gender_dicts = {}
        dicts[age_division[1]] = belt_dicts
        belt_dicts = {} 

    return render_template('ranking_atl.html', page_title="Ranking Atletas", headers=headers, dicts=dicts)