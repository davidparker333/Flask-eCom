import re
from . import bp as auth
from app import db, mail
from flask_mail import Message
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from .models import User
from .forms import UserInfoForm, LoginForm

@auth.route('/register', methods=['GET', 'POST'])
def register():
    title = 'Register'
    form = UserInfoForm()
    if request.method == 'POST':

        if not form.validate_on_submit():
            flash("Hmm, something in your info isn't right. Please try again")
            return redirect(url_for('register'))

        username = form.username.data
        email = form.email.data
        fname = form.fname.data
        lname = form.lname.data
        password = form.password.data

        existing_user = User.query.filter((User.username == username) | (User.email == email)).all()
        if existing_user:
            flash("That username / email is already taken. Please try again or sign in if you have an account", 'warning')
            return redirect(url_for('register'))
        
        new_user = User(fname, lname, username, email, password)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Thank you {fname}. You have successfully registered!", 'success')

        msg = Message('Thank you for signing up for Shopping Thyme', recipients=[email])
        msg.body = f"Dear {fname}, the team at Shopping Thyme would like to thank you for registering for our site! Please enjoy our premium selection of spices and herbs."
        mail.send(msg)

        return redirect(url_for('main.index'))
    
    return render_template('register.html', title=title, form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Login'
    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password, password):
            flash("Incorrect username or password. Please try again", 'danger')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        flash("You have successfully logged in", 'success')
        return redirect(url_for('main.index'))

    return render_template('login.html', form=form, title=title)

@auth.route('/logout')
def logout():
    logout_user()
    flash("You have successfully been logged out", 'warning')
    return redirect(url_for('main.index'))