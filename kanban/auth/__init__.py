import os
from flask import Flask
from .blueprints import auth
import db


def create_app(config=None):
    # create & configure app
    app = Flask(__name__, instance_relative_config=True)
    assert app.instance_path is not None, 'app.instance should not be "None"'
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.db')
    )
    
    # load instance config, unless passed custom config 
    if config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(config)
    
    # make sure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    
    # initialize database
    db.init_app(app)
    
    # register blueprints
    app.register_blueprint(auth.bp)
    
    return app
