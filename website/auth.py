from flask import Blueprint, render_template, request,flash ,redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,login_required,logout_user,current_user
auth = Blueprint('auth', __name__)


@auth.route('/login',methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Login in Successfully!',category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))

            else:
                flash('Invalid password',category='error')
        else:
            flash('Email does not exits Sign in to create a account',category='error')
    return render_template("login.html",user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=["GET", "POST"])

def signup():
    if request.method == "POST":
        email = request.form.get('email')
        full_name = request.form.get('fullname')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user = User.query.filter_by(email=email).first()

        # Form validation
        if user:
            flash('Email already exits.',category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters','error')
        elif len(full_name) < 2:
            flash('Name is too short', 'error')
        elif password != confirm_password:
            flash('Password does not match', 'error')
        elif len(password) < 7:
            flash('Password is too short', 'error')
        else:
            # Registration successful
            new_user = User(email=email,first_name=full_name,password=generate_password_hash(password=password,method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account is created!', 'success')
            login_user(new_user, remember=True)
            print("After flash statement")
            return redirect(url_for('views.home'))

            # Redirect to the home page after successful registration

    return render_template("signup.html",user=current_user)
def shop():
    return render_template("shop.html",user=current_user)