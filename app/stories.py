# -*- coding: utf-8 -*-
"""
    Another Stories
    ~~~~~~~~~~~~~~~

    Simple web-application for cute short stories

    :copyright: (c) 2014 by Llama on the Boat (llamaontheboat.com)
    :license: Apache License 2.0
"""
# from __future__ import unicode_literals
from flask import Flask, g, render_template, redirect, url_for, \
    request, session, flash, abort, jsonify
from werkzeug import check_password_hash
from forms import LoginForm, AddStoryForm
import sqlite3

# application
app = Flask(__name__)
app.config.from_object('config')
app.config.from_envvar('ANOTHER-STORIES_SETTINGS', silent=True)


# database staff
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    try:
        cur = get_db().execute(query, args)
        rv = cur.fetchall()
        return (rv[0] if rv else None) if one else rv
    except sqlite3.OperationalError:
        print "Something goes wrong with database. \
            Be sure you've executed init_db.py before run system"
        abort(404)
        return None


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = query_db('select * from user where user_id = ?',
                          [session['user_id']], one=True)


# application routes
@app.route('/', methods=['GET', 'POST'])
def index():
    stories = query_db(
        "SELECT * FROM story WHERE 1 ORDER BY story_id DESC LIMIT 5")
    if g.user:
        # создаем форму для добавления новой истории
        add_story_form = AddStoryForm()
        if request.method == 'POST' and add_story_form.validate():
            db = get_db()
            db.execute("INSERT INTO story (title, text) VALUES (?, ?)",
                       [request.form['title'], request.form['text']])
            db.commit()
            flash(u'Ура! Новую историю увидят все.')
            return redirect(url_for('index'))
        return render_template('stories.html', form=add_story_form, stories=stories)
    else:
        return render_template('stories.html', stories=stories)


@app.route('/story/get_more/<int:last_story_id>', methods=['POST'])
def get_more_stories(last_story_id):
    stories = query_db(
        "SELECT * FROM story WHERE story_id<? ORDER BY story_id DESC LIMIT 5", [last_story_id])
    return stories


@app.route('/story/<int:story_id>')
def show_story(story_id):
    story = query_db("SELECT * FROM story WHERE story_id = ?",
                     [story_id], True)
    return render_template('story.html', story=story)


@app.route('/story/like/<int:story_id>', methods=['POST'])
def like_story(story_id):
    try:
        db = get_db()
        db.execute("UPDATE story SET like=like+1 WHERE story_id = ?",
                   [story_id])
        db.commit()
        result_likes = query_db(
            "SELECT like FROM story WHERE story_id = ?", [story_id], True)
        return jsonify({'result': 'OK', 'likes': result_likes['like']})
    except sqlite3.OperationalError:
        return jsonify({'result': 'FAILED'})


@app.route('/story/edit/<int:story_id>')
def edit_story(story_id):
    if g.user:
        story = query_db("SELECT * FROM story WHERE story_id = ?", [story_id], True)
        edit_story_form = AddStoryForm()
        if request.method == 'POST' and edit_story_form.validate():
            db = get_db()
            db.execute("UPDATE story SET(title = ?, text = ?) WHERE story_id = ?", \
                [request.form['title'], request.form['text'], story_id])
            db.commit()
            flash(u'История успешно изменина ')
            return redirect(url_for('index'))
        return render_template('edit_story.html', story=story, form=edit_story_form)
    return redirect(url_for('index'))



@app.route('/story/remove/<int:story_id>', methods=['POST'])
def remove_story(story_id):
    try:
        db = get_db()
        db.execute("DELETE FROM story WHERE story_id = ?", [story_id])
        return jsonify({'result': 'OK'})
    except sqlite3.OperationalError:
        return jsonify({'result': 'FAILED'})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('index'))
    login_form = LoginForm()
    if request.method == 'POST' and login_form.validate():
        user = query_db('''SELECT * FROM user WHERE
            username = ?''', [request.form['username']], one=True)
        if check_password_hash(user["pw_hash"], request.form["password"]):
            session['user_id'] = user['user_id']
            return redirect(url_for('index'))
        else:
            login_form.password.errors += [u'Не похоже на правду..']
    return render_template('login.html', form=login_form)


@app.route('/logout')
def logout():
    """Logs the user out"""
    flash(u'Всего хорошего! Возвращайся скорее ')
    session.pop('user_id', None)
    return redirect(url_for('index'))

# run!
if __name__ == '__main__':
    app.run(host='0.0.0.0')
