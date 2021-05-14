from . import bp as main
from flask import render_template

@main.routes('/')
def index():
    title = 'Home'

    return render_template('index.html', title=title)