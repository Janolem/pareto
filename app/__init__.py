"""Initialize Flask app."""
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_babel import Babel

def init_app():
    """Construct core flask application"""
    app = Flask(__name__)
    app.config.from_object("config.Config")
    bootstrap = Bootstrap()
    babel = Babel()

    bootstrap.init_app(app)
    babel.init_app(app)
    app.static_folder = 'static'
    with app.app_context():
        #Import parts of core flask app
        from . import routes
        
        #Import dash app
        from .dashplots.pareto1 import init_pareto1
        from .dashplots.pareto2 import init_pareto2
        app = init_pareto1(app)
        app = init_pareto2(app)

        return app
