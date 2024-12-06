from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

players = Blueprint('players', __name__)

@players.route('/players', methods=['GET', 'POST'])
def players_home():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new player
    if request.method == 'POST':
        player_name = request.form['player_name']
        position = request.form['position']
        team = request.form['team']
        games_played = request.form['games_played']
        at_bats = request.form['at_bats']
        runs = request.form['runs']
        hits = request.form['hits']
        doubles = request.form['doubles']
        triples = request.form['triples']
        home_runs = request.form['home_runs']
        rbis = request.form['rbis']
        stolen_bases = request.form['stolen_bases']
        batting_avg = request.form['batting_avg']

        # Insert the new player into the database
        cursor.execute(
            '''INSERT INTO players (
                player_name, position, team, games_played, at_bats, runs, hits, doubles, triples, 
                home_runs, rbis, stolen_bases, batting_avg
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
            (player_name, position, team, games_played, at_bats, runs, hits, doubles, triples,
             home_runs, rbis, stolen_bases, batting_avg)
        )
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
        # Update the player's details
        player_name = request.form['player_name']
        position = request.form['position']
        team = request.form['team']
        games_played = request.form['games_played']
        at_bats = request.form['at_bats']
        runs = request.form['runs']
        hits = request.form['hits']
        doubles = request.form['doubles']
        triples = request.form['triples']
        home_runs = request.form['home_runs']
        rbis = request.form['rbis']
        stolen_bases = request.form['stolen_bases']
        batting_avg = request.form['batting_avg']

        cursor.execute(
            '''UPDATE players SET 
                player_name = %s, position = %s, team = %s, games_played = %s, at_bats = %s, runs = %s, hits = %s, 
                doubles = %s, triples = %s, home_runs = %s, rbis = %s, stolen_bases = %s, batting_avg = %s 
                WHERE player_id = %s''',
            (player_name, position, team, games_played, at_bats, runs, hits, doubles, triples,
             home_runs, rbis, stolen_bases, batting_avg, player_id)
        )
        db.commit()

        flash('Player updated successfully!', 'success')
        return redirect(url_for('players.players_home'))

    # GET method: fetch player's current data for pre-populating the form
    cursor.execute('SELECT * FROM players WHERE player_id = %s', (player_id,))
    current_player = cursor.fetchone()
    return render_template('update_player_modal.html', current_player=current_player)

@players.route('/delete_player/<int:player_id>', methods=['POST'])
def delete_player(player_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the player
    cursor.execute('DELETE FROM players WHERE player_id = %s', (player_id,))
    db.commit()

    flash('Player deleted successfully!', 'danger')
    return redirect(url_for('players.players_home'))

