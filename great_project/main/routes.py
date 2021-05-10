from flask import render_template, Blueprint
from great_project.models import Event

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    
    return render_template('index.html', page_title="Inicio")

@main.route('/calendario')
def calendario():
    events = Event.query.order_by(Event.id).all()
    return render_template('calendario.html', page_title="Calendario", events=events)

@main.route('/rankingaca')
def rankingaca():
    return render_template('rankingaca.html', page_title="Ranking Academias")

@main.route('/resultados')
def resultados():
    return render_template('resultados.html', page_title="Resultados")