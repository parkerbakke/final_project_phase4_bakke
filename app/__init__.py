from flask import Flask, g
import datetime
from .app_factory import create_app
from .db_connect import close_db, get_db

app = create_app()
app.secret_key = 'your-secret'  # Replace with an environment variable

@app.template_filter('datetimeformat')
def datetimeformat(value):
    if value:
        return datetime.datetime.utcfromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
    return value

# Register Blueprints
from app.blueprints.players import players
from app.blueprints.team_stats import team_stats
from app.blueprints.polls import polls
from app.blueprints.game_viewer import game_viewer

app.register_blueprint(players)
app.register_blueprint(team_stats)
app.register_blueprint(polls)
app.register_blueprint(game_viewer)


from . import routes

@app.before_request
def before_request():
    g.db = get_db()

# Setup database connection teardown
@app.teardown_appcontext
def teardown_db(exception=None):
    close_db(exception)

