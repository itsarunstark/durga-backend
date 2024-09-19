import sqlite3
from flask import current_app, g
from flask.app import Flask
import click
from typing import Union

class Resources:
    created_schema = './schema.sql'

def get_db()->sqlite3.Connection:
    if 'database' not in g:
        g.database = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.database.row_factory = sqlite3.Row
    
    return g.database

def close_db(e=None):
    db : Union[sqlite3.Connection, None] = g.pop('database', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource(Resources.created_schema) as f:
        db.executescript(
            f.read().decode('utf-8')
        )

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initializing the databse.....')

def init_app(app:Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)