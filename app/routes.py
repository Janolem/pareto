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