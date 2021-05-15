from . import bp as shop
from app import db
from flask import render_template, redirect, url_for, flash, request
#from .forms import [WHATEVER FORMS YOU NEED]
from .models import Cart, Product

@shop.route('/shop')
def shop():
    title = "Shop"
    products = Product.query.all()

    return render_template('products.html', title=title, products=products)