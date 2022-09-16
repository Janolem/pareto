"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_babel import Babel

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
babel = Babel()

def init_app():
    """Construct core flask application"""
    app = Flask(__name__)
    app.config.from_object("config.Config")
    db = SQLAlchemy(app)
    migrate.init_app(app,db)
    bootstrap.init_app(app)
    babel.init_app(app)
    app.static_folder = 'static'
    with app.app_context():
        #Import parts of core flask app
        from . import routes, models
        db.create_all()
        #Import dash app
        from .dashplots.pareto1 import init_pareto1
        from .dashplots.pareto2 import init_pareto2
        from .dashplots.pareto3 import init_pareto3
        app = init_pareto1(app)
        app = init_pareto2(app)
        app = init_pareto3(app)

        return app