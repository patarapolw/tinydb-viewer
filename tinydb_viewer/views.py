from flask import render_template

from . import app
from .config import config


@app.route('/')
def index():
    return render_template('viewer.html', config=config['handsontable'])
