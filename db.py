import os.path
import sqlite3
from datetime import datetime

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


# helper function that returns nothing
# because app.before_request must return nothing
def load_db():
    get_db()


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(base_dir, 'schema.sql')

    with open(schema_path, 'r', encoding='utf8') as file:
        db.executescript(file.read())


@click.command("init-db")
def init_db_command():
    init_db()
    click.echo('Successfully initialized database.')


# tell python how to interpret timestamp values
sqlite3.register_converter(
    'timestamp', lambda v: datetime.fromisoformat(v.decode())
)


def init_app(app):
    app.before_request(load_db)  # tell flask to get database on request
    app.teardown_appcontext(close_db)   # tell flask to call this when cleaning up after response
    app.cli.add_command(init_db_command)  # add new cli command
