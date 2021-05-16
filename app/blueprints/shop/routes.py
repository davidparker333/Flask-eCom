from . import bp as shop
from app import db
from flask import render_template, redirect, url_for, flash, request
#from .forms import [WHATEVER FORMS YOU NEED]
from .models import Cart, Product

@shop.route('/products')
def _shop():
    title = "Shop"
    products = Product.query.distinct(Product.sku)

    return render_template('products.html', title=title, products=products)

@shop.route('/product_spotlight/<product_sku>')
def product_detail(product_sku):
    prod = Product.query.filter_by(sku=product_sku).first_or_404()
    top_4 = Product.query.filter(Product.sku != product_sku).limit(4).distinct(Product.sku)
    title = f'{prod.name}'

    return render_template('product_detail.html', title=title, prod=prod, top_4=top_4)
