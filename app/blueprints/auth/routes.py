from . import bp as auth
from app import db, mail
from flask_mail import Message
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
#from .models import User [CREATE MODELS AND UNCOMMENT]
#from .forms import [THE FORMS YOU NEED]