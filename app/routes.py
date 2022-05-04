"""Routes for parent Flask app."""
from flask import render_template, url_for, current_app as app
from flask_babel import _, get_locale



@app.route('/')
@app.route('/home')
def home():
    """Landing page."""
    return render_template(
        'home.html',
        title=_('Home')
    )

@app.route('/explore')
def explore():
    """Explore page."""
    return render_template(
        'explore.html',
        title=_('Explore')
    )

@app.route('/pareto1')
def pareto1():
    """pareto front1"""
    return render_template(
        'pareto1.html',
        title=_('Pareto Front 1')
    )

@app.route('/pareto2')
def pareto2():
    """pareto front2"""
    return render_template(
        'pareto2.html',
        title=_('Pareto Front 2')
    )
