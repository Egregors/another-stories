"""
	Creating a database
"""

import sys
from stories import app, get_db
from werkzeug import generate_password_hash

# defoult login/pass
name = 'admin'
password = 'admin'

if len(sys.argv) == 2:
    # from args
    name = sys.argv[1]
    password = sys.argv[2]
    print 'Creation of a database for user: %s with pass: %s ...' % name, sys.argv[2]
else:
    # simple input
    name = raw_input("Enter a username (default: %s):\n" % name) or name
    password = raw_input("Enter a password (default: 'admin'):\n") or password
    print 'Creation of a database for user: %s with pass: %s ...' % (name, password)


def init_db(user, password):
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.execute("INSERT INTO user (username, pw_hash) VALUES (?, ?)",
                   [name, generate_password_hash(password)])
        db.commit()
        print 'Done'

init_db(name, password)
