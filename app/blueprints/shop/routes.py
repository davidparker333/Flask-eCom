from sqlalchemy.sql.elements import Null
from . import bp as shop
from app import db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .models import Cart, Product
import stripe
import os

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

@shop.route('/products/add/<product_sku>')
@login_required
def add_to_cart(product_sku):
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    prod = Product.query.filter_by(sku=product_sku).first()
    prod.cart_id = cart.id
    db.session.add(prod)
    db.session.commit()

    flash(f"{prod.name} has been added to your cart", 'success')

    return redirect(url_for('shop._shop'))

@shop.route('/cart', methods=['GET', 'POST'])
@login_required
def show_cart():
    title = "My Cart"
    cart =  Cart.query.filter_by(user_id=current_user.id).first()
    products = Product.query.filter_by(cart_id=cart.id).all()
    subtotal = 0
    for product in products:
        subtotal += product.amount
    tax = float(subtotal) * .05
    total = float(subtotal) + tax
    subtotal = "${:,.2f}".format(subtotal)
    tax = "${:,.2f}".format(tax)
    total = "${:,.2f}".format(total)
    key = os.environ.get('stripe_publishable_key')
    if request.method == 'POST':
        amount = total
        try:
            customer = stripe.Customer.create(
                email=current_user.email,
                source=request.form['stripeToken']
            )
            charge = stripe.Charge.create(
                customer=customer.id,
                amount=amount,
                currency='usd',
                description='Shopping Thyme'
            )
            flash("Your payment was successful", 'success')
            return redirect(url_for('main.index'))

        except stripe.error.CardError:
            flash("Error processing payment", 'danger')
            return redirect(url_for('shop.charge'))

    return render_template('cart.html', title=title, cart=cart, products=products, subtotal=subtotal, tax=tax, total=total, key=key)

@shop.route('/remove/<product_id>')
@login_required
def remove_from_cart(product_id):
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    prod = Product.query.filter_by(id=product_id).first()
    if prod.cart_id != cart.id:
        flash("You can't remove this item from your cart", 'danger')
        return redirect(url_for('shop.show_cart'))
    prod.cart_id = 0
    db.session.add(prod)
    db.session.commit()
    flash(f"{prod.name} removed from cart", 'warning')

    return redirect(url_for('shop.show_cart'))

@shop.route('/removeall')
@login_required
def remove_all():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    products_in_cart = Product.query.filter_by(cart_id=cart.id).all()
    for product in products_in_cart:
        product.cart_id = 0
        db.session.add(product)
        db.session.commit()
    flash("You've removed all items from your cart", 'warning')

    return redirect(url_for('shop.show_cart'))
    


