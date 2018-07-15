import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row 
    return g.db
    
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()



def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


"""allows for a command line command called init-db
the definition of that command is given below (which invokes our init_db)"""
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')



""" these functions need to be registered with the app
factory instance is not available at the time of writing these functions
writing an app that does the registration; see __init__.py"""
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command) #adds new command that can be called from flask command