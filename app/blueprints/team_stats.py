from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

team_stats = Blueprint('team_stats', __name__)

@team_stats.route('/team_stats', methods=['GET', 'POST'])
def team_stats_home():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new team stat
    if request.method == 'POST':
        team_name = request.form['team_name']
        team_abbreviation = request.form['team_abbreviation']
        season_year = request.form['season_year']
        games_played = request.form['games_played']
        wins = request.form['wins']
        losses = request.form['losses']
        runs = request.form['runs']
        home_runs = request.form['home_runs']
        batting_average = request.form['batting_average']
        on_base_percentage = request.form['on_base_percentage']
        slugging_percentage = request.form['slugging_percentage']
        era = request.form['era']
        whip = request.form['whip']
        strikeouts = request.form['strikeouts']
        save_opportunities = request.form['save_opportunities']
        stolen_bases = request.form['stolen_bases']
        fielding_percentage = request.form['fielding_percentage']

        # Insert the new team stat into the database
        query = """
            INSERT INTO team_stats (
                team_name, team_abbreviation, season_year, games_played, wins, losses, runs, home_runs,
                batting_average, on_base_percentage, slugging_percentage, era, whip, strikeouts,
                save_opportunities, stolen_bases, fielding_percentage
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            team_name, team_abbreviation, season_year, games_played, wins, losses, runs, home_runs,
            batting_average, on_base_percentage, slugging_percentage, era, whip, strikeouts,
            save_opportunities, stolen_bases, fielding_percentage
        ))
        db.commit()

        flash('New team stats added successfully!', 'success')
        return redirect(url_for('team_stats.team_stats_home'))

    # Handle GET request to display all team stats
    cursor.execute('SELECT * FROM team_stats')
    all_team_stats = cursor.fetchall()
    return render_template('team_stats.html', all_team_stats=all_team_stats)


@team_stats.route('/update_team_stats/<int:team_id>', methods=['GET', 'POST'])
def update_team_stats(team_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the team's stats
        team_name = request.form['team_name']
        team_abbreviation = request.form['team_abbreviation']
        season_year = request.form['season_year']
        games_played = request.form['games_played']
        wins = request.form['wins']
        losses = request.form['losses']
        runs = request.form['runs']
        home_runs = request.form['home_runs']
        batting_average = request.form['batting_average']
        on_base_percentage = request.form['on_base_percentage']
        slugging_percentage = request.form['slugging_percentage']
        era = request.form['era']
        whip = request.form['whip']
        strikeouts = request.form['strikeouts']
        save_opportunities = request.form['save_opportunities']
        stolen_bases = request.form['stolen_bases']
        fielding_percentage = request.form['fielding_percentage']

        query = """
            UPDATE team_stats
            SET team_name = %s, team_abbreviation = %s, season_year = %s, games_played = %s, wins = %s,
                losses = %s, runs = %s, home_runs = %s, batting_average = %s, on_base_percentage = %s,
                slugging_percentage = %s, era = %s, whip = %s, strikeouts = %s, save_opportunities = %s,
                stolen_bases = %s, fielding_percentage = %s
            WHERE team_id = %s
        """
        cursor.execute(query, (
            team_name, team_abbreviation, season_year, games_played, wins, losses, runs, home_runs,
            batting_average, on_base_percentage, slugging_percentage, era, whip, strikeouts,
            save_opportunities, stolen_bases, fielding_percentage, team_id
        ))
        db.commit()

        flash('Team stats updated successfully!', 'success')
        return redirect(url_for('team_stats.team_stats_home'))

    # GET method: fetch team's current stats for pre-populating the form
    cursor.execute('SELECT * FROM team_stats WHERE team_id = %s', (team_id,))
    current_team_stats = cursor.fetchone()
    return render_template('update_team_stats.html', current_team_stats=current_team_stats)


@team_stats.route('/delete_team_stats/<int:team_id>', methods=['POST'])
def delete_team_stats(team_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the team stats
    cursor.execute('DELETE FROM team_stats WHERE team_id = %s', (team_id,))
    db.commit()

    flash('Team stats deleted successfully!', 'danger')
    return redirect(url_for('team_stats.team_stats_home'))

