from app.blueprints.shop.models import Product
from . import bp as main
from flask import render_template

@main.route('/')
def index():
    title = 'Home'
    top_4 = Product.query.limit(4).all()

    return render_template('index.html', title=title, top_4=top_4)