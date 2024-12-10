from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

players = Blueprint('players', __name__)

@players.route('/players', methods=['GET', 'POST'])
def players_home():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new player
    if request.method == 'POST':
        uniform_number = request.form['uniform_number']
        player_name = request.form['player_name']
        player_country = request.form['player_country']
        player_active = request.form['player_active']
        player_il = request.form['player_il']
        player_age = request.form['player_age']
        player_hitting = request.form['player_hitting']
        player_throwing = request.form['player_throwing']
        player_height = request.form['player_height']
        player_weight = request.form['player_weight']
        player_dob = request.form['player_dob']
        player_firstyear = request.form['player_firstyear']
        player_position = request.form['player_position']

        cursor.execute('''
            INSERT INTO players (uniform_number, player_name, player_country, player_active, player_il, 
                                 player_age, player_hitting, player_throwing, player_height, player_weight, 
                                 player_dob, player_firstyear, player_position)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (uniform_number, player_name, player_country, player_active, player_il, player_age, player_hitting,
              player_throwing, player_height, player_weight, player_dob, player_firstyear, player_position))
        db.commit()

        flash('New player added successfully!', 'success')
        return redirect(url_for('players.players_home'))

    # Handle GET request to display all players
    cursor.execute('SELECT * FROM players')
    all_players = cursor.fetchall()
    return render_template('players.html', all_players=all_players)

@players.route('/update_player/<int:player_id>', methods=['GET', 'POST'])
def update_player(player_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        uniform_number = request.form['uniform_number']
        player_name = request.form['player_name']
        player_country = request.form['player_country']
        player_active = request.form['player_active']
        player_il = request.form['player_il']
        player_age = request.form['player_age']
        player_hitting = request.form['player_hitting']
        player_throwing = request.form['player_throwing']
        player_height = request.form['player_height']
        player_weight = request.form['player_weight']
        player_dob = request.form['player_dob']
        player_firstyear = request.form['player_firstyear']
        player_position = request.form['player_position']

        cursor.execute('''
            UPDATE players
            SET uniform_number = %s, player_name = %s, player_country = %s, player_active = %s, player_il = %s, 
                player_age = %s, player_hitting = %s, player_throwing = %s, player_height = %s, 
                player_weight = %s, player_dob = %s, player_firstyear = %s, player_position = %s
            WHERE player_id = %s
        ''', (uniform_number, player_name, player_country, player_active, player_il, player_age, player_hitting,
              player_throwing, player_height, player_weight, player_dob, player_firstyear, player_position, player_id))
        db.commit()

        flash('Player updated successfully!', 'success')
        return redirect(url_for('players.players_home'))

    # GET method: fetch player data for pre-populating the form
    cursor.execute('SELECT * FROM players WHERE player_id = %s', (player_id,))
    current_player = cursor.fetchone()
    return render_template('update_player.html', current_player=current_player)

@players.route('/delete_player/<int:player_id>', methods=['POST'])
def delete_player(player_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the player
    cursor.execute('DELETE FROM players WHERE player_id = %s', (player_id,))
    db.commit()

    flash('Player deleted successfully!', 'danger')
    return redirect(url_for('players.players_home'))



