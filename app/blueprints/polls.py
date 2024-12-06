from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db

polls = Blueprint('polls', __name__)

# Route for displaying all polls and voting
@polls.route('/polls', methods=['GET', 'POST'])
def polls_home():
    db = get_db()
    cursor = db.cursor()

    # Fetch all polls and their options
    cursor.execute('SELECT * FROM polls')
    all_polls = cursor.fetchall()

    for poll in all_polls:
        cursor.execute('SELECT * FROM poll_options WHERE poll_id = %s', (poll['poll_id'],))
        poll['options'] = cursor.fetchall()

    if request.method == 'POST':
        selected_option_id = request.form.get('selected_option')
        poll_id = request.form.get('poll_id')

        if not selected_option_id:
            flash('Please select an option before voting!', 'danger')
        else:
            cursor.execute('UPDATE poll_options SET votes = votes + 1 WHERE option_id = %s', (selected_option_id,))
            db.commit()
            flash('Your vote has been recorded!', 'success')
            return redirect(url_for('polls.polls_home'))

    return render_template('polls.html', all_polls=all_polls)

# Route for creating a new poll
@polls.route('/add_poll', methods=['GET', 'POST'])
def add_poll():
    if request.method == 'POST':
        question = request.form['question']
        options = request.form.getlist('options[]')

        db = get_db()
        cursor = db.cursor()

        # Insert the new poll question
        cursor.execute('INSERT INTO polls (question) VALUES (%s)', (question,))
        poll_id = cursor.lastrowid

        # Insert the options for the poll
        for option in options:
            cursor.execute('INSERT INTO poll_options (poll_id, poll_option, votes) VALUES (%s, %s, 0)', (poll_id, option))

        db.commit()
        flash('Poll created successfully!', 'success')
        return redirect(url_for('polls.polls_home'))

    return render_template('add_poll.html')









