from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db
import json

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

        if not selected_option_id:
            flash('Please select an option before voting!', 'danger')
        else:
            # Record the vote for the selected option
            poll_id = request.form.get('poll_id')
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

        if not question or not options:
            flash('Poll question and options are required!', 'danger')
            return redirect(url_for('polls.add_poll'))

        db = get_db()
        cursor = db.cursor()

        # Insert the new poll question
        cursor.execute('INSERT INTO polls (question) VALUES (%s)', (question,))
        poll_id = cursor.lastrowid

        # Insert the options for the poll
        for option in options:
            cursor.execute('INSERT INTO poll_options (poll_id, poll_option, votes) VALUES (%s, %s, 0)',
                           (poll_id, option))

        db.commit()
        flash('Poll created successfully!', 'success')
        return redirect(url_for('polls.polls_home'))

    return render_template('add_poll.html')


# Route for editing a poll
@polls.route('/edit_poll', methods=['GET', 'POST'])
def edit_poll():
    if request.method == 'POST':
        poll_id = request.form['poll_id']
        new_question = request.form['question']
        new_options = request.form.getlist('options[]')

        if not new_question or not new_options:
            flash('Poll question and options are required!', 'danger')
            return redirect(url_for('polls.edit_poll', poll_id=poll_id))

        db = get_db()
        cursor = db.cursor()

        # Update the poll question
        cursor.execute('UPDATE polls SET question = %s WHERE poll_id = %s', (new_question, poll_id))

        # Delete existing options
        cursor.execute('DELETE FROM poll_options WHERE poll_id = %s', (poll_id,))

        # Insert new options
        for option in new_options:
            cursor.execute('INSERT INTO poll_options (poll_id, poll_option, votes) VALUES (%s, %s, 0)',
                           (poll_id, option))

        db.commit()
        flash('Poll updated successfully!', 'success')
        return redirect(url_for('polls.polls_home'))

    # If GET request, show poll details for editing
    poll_id = request.args.get('poll_id')
    db = get_db()
    cursor = db.cursor()

    # Fetch poll details
    cursor.execute('SELECT * FROM polls WHERE poll_id = %s', (poll_id,))
    poll = cursor.fetchone()

    cursor.execute('SELECT * FROM poll_options WHERE poll_id = %s', (poll_id,))
    poll_options = cursor.fetchall()

    return render_template('edit_poll.html', poll=poll, poll_options=poll_options)


# Route for deleting a poll
@polls.route('/delete_poll', methods=['POST'])
def delete_poll():
    poll_id = request.form['poll_id']

    db = get_db()
    cursor = db.cursor()

    # Delete options associated with the poll
    cursor.execute('DELETE FROM poll_options WHERE poll_id = %s', (poll_id,))

    # Delete the poll
    cursor.execute('DELETE FROM polls WHERE poll_id = %s', (poll_id,))

    db.commit()
    flash('Poll deleted successfully!', 'success')
    return redirect(url_for('polls.polls_home'))










