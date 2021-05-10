from flask import render_template, Blueprint
from great_project.models import Event

main = Blueprint('main', __name__)

#  home route
@main.route('/')
@main.route('/index')
def index():
    
    return render_template('index.html', page_title="Inicio")

# calendar toute
@main.route('/calendario')
def calendario():
    events = Event.query.order_by(Event.id).all()
    return render_template('calendario.html', page_title="Calendario", events=events)

# academies ranking route
@main.route('/rankingaca')
def rankingaca():
    return render_template('rankingaca.html', page_title="Ranking Academias")

# results route
@main.route('/resultados')
def resultados():
    return render_template('resultados.html', page_title="Resultados")

# no results availible route
@main.route('/no_results')
def no_results():
    return render_template('no_results.html', page_title="Resultados")