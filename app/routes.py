from flask import render_template
from . import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game_viewer')
def game_viewer():
    return render_template('game_viewer.html')




