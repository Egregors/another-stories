# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, TextAreaField
from wtforms import validators
from config import DATABASE
import sqlite3

class LoginForm(Form):

    """Form for user authorization"""
    username = TextField(
        'Это ты?', [validators.InputRequired()])
    password = PasswordField('А пароль знаешь?', [validators.InputRequired()])

    def validate_username(form, field):
        """Verify the existence of the user in the database"""
        try:
            rv = sqlite3.connect(DATABASE)
            cur = rv.execute(
                'SELECT * FROM user WHERE username = ?', [field.data])
            rv = cur.fetchall()
            user = (rv[0] if rv else None)
        except sqlite3.OperationalError:
            raise validators.ValidationError('хм.. а где база данных?')
        if user is None:
            raise validators.ValidationError('Это не ты')

class AddStoryForm(Form):
	"""Form for adding new cute short story"""
	title = TextField('Как корабль назовешь..', [validators.InputRequired()])
	text = TextAreaField('В далекой далекой галактике')
		