from flask import render_template, request, url_for, redirect, flash, request, jsonify, json, Blueprint
from flask_login import current_user, login_required
from great_project import db, login_manager
from great_project.admin.forms import  ResultsForm
from great_project.models import Atleta, Academy, Belt, Gender, Event, Age_division, Registration, Weight, Weight_age_division_gender, Age_division_belt
from great_project.event.utils import age_division_choices

# login manager to know the current user 
@login_manager.user_loader
def load_user(atleta_id):
    return Atleta.query.get(int(atleta_id))

# create blueprint for event routes
admin = Blueprint('admin', __name__)

@admin.route('/set_results')
@login_required
def set_results():
    age_divisions = db.session.query(Age_division.id, Age_division.name).order_by(Age_division.id).all()
    genders = db.session.query(Gender.id, Gender.name).all()
    dicts = {}
    belt_dicts = {}
    gender_dicts = {}
    weight_dicts = {}
    forms = []
    for age_division in age_divisions:
        # age_name = age_division[1]
        dicts[age_division[1]] = {}
        for belt in db.session.query(Belt.id, Belt.name).join(Age_division_belt).filter(Age_division_belt.age_division_id == age_division[0]).all():
            # belt_name = belt[1]
            belt_dicts[belt[1]] = {}
            for gender in genders:
                # gender_name = gender[1]
                gender_dicts[gender[1]] = {}
                for weight in db.session.query(Weight.id, Weight.name).join(Weight_age_division_gender).filter(Weight_age_division_gender.age_division_id == age_division[0], Weight_age_division_gender.gender_id == gender[0]).all():
                    atletas = db.session.query(Atleta.name, Academy.name, Atleta.id).join(Registration.atleta).join(Atleta.academy).filter(Atleta.gender_id == gender[0], Atleta.belt_id == belt[0], Registration.age_division_id == age_division[0], Atleta.gender_id == gender[0], Registration.weight_id == weight[0], Atleta.id == Registration.atleta_id, Registration.event_id == 1).all()
                    # weight_name = weight.name
                    if atletas != []:
                        form = ResultsForm()
                        form.first_place.choices = [(atleta[2], (atleta[0], atleta[1])) for atleta in atletas]
                        form.second_place.choices = [(atleta[2], (atleta[0], atleta[1])) for atleta in atletas]
                        form.third_place.choices = [(atleta[2], (atleta[0], atleta[1])) for atleta in atletas]
                        form.third_place1.choices = [(atleta[2], (atleta[0], atleta[1])) for atleta in atletas]  
                        weight_dicts[weight[1]] = form
                        forms.append(form)
                gender_dicts[gender[1]] = weight_dicts
                weight_dicts = {}
            belt_dicts[belt[1]] = gender_dicts
            gender_dicts = {}
        dicts[age_division[1]] = belt_dicts
        belt_dicts = {}
        for form in forms:
            if form.submit.data and form.validate_on_submit():
                first = Atleta.query.filter_by(id=form.first_place.data).first()
                first.points += 9
                second = Atleta.query.filter_by(id=form.second_place.data).first()
                second.points += 3
                if form.third_place.data:
                    third = Atleta.query.filter_by(id=form.third_place.data).first()
                    third.points += 1
                if form.third_place1.data: 
                    third1 = Atleta.query.filter_by(id=form.third_place1.data).first()
                    third1.points += 1 
                db.session.commit()
    print(dicts)           
    if current_user.is_admin:
        return render_template('set_results.html', page_title="Definir Resultados", dicts=dicts)