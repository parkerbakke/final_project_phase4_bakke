from flask import Blueprint, render_template
from app.db_connect import get_db

team_stats = Blueprint('team_stats', __name__)

@team_stats.route('/team_stats', methods=['GET'])
def team_stats_home():
    db = get_db()
    cursor = db.cursor()

    # Fetch statistics for the team
    cursor.execute('SELECT * FROM team_stats LIMIT 1')  # Assuming only one team's stats are stored
    team_data = cursor.fetchone()

    if team_data:
        team_stats = {
            "team_name": team_data[1],           # Adjust indices based on your table's column order
            "games_played": team_data[2],
            "wins": team_data[3],
            "losses": team_data[4],
            "win_percentage": team_data[5],
            "runs_scored": team_data[6],
            "runs_allowed": team_data[7],
            "home_runs": team_data[8],
            "rbis": team_data[9],
            "stolen_bases": team_data[10],
            "batting_avg": team_data[11],
            "era": team_data[12],
            "strikeouts": team_data[13],
        }
    else:
        team_stats = None

    return render_template('team_stats.html', team_stats=team_stats)

