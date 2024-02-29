from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from datetime import timedelta
import ast
import logging

from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)
custom_logger = logging.getLogger('custom')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('email') and request.form.get('password'):
            email = request.form.get('email').lower()
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    custom_logger.info(user.email + " logged in.")
                    flash('Welcome ' + user.first_name + "!", category='success')
                    login_user(user, remember=False)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password', category='error')
            else:
                flash('Email does not exist', category='error')
                
    return render_template("login.html", user=current_user)

@auth.route('/login_w_qr_code', methods=['POST'])
def login_w_qr_code():
    def is_valid_dict_string(s):
        """Check if string is a valid Python dict string."""
        try:
            d = ast.literal_eval(s)
            if isinstance(d, dict):
                return True
        except (ValueError, SyntaxError):
            return False
        return False

    def string_to_dict(s):
        """Convert string to dict and check for required keys."""
        if is_valid_dict_string(s):
            d = ast.literal_eval(s)
            required_keys = ["user_id", "user_email", "user_pw"]
            if all(key in d for key in required_keys):
                return d
        return None
    
    data = request.form.to_dict()
    scan_data = string_to_dict(data.get("scan_data_home"))

    if not scan_data:
        flash('Invalid input!', category='error')
    else:
        email = scan_data.get("user_email")

        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == scan_data.get("user_pw"):
                flash('Welcome ' + user.first_name +
                        "!", category='success')
                login_user(user, remember=False)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
                return redirect(request.referrer)
        else:
            flash('Email does not exist', category='error')
            return redirect(request.referrer)
    
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/update_password', methods=['POST'])
@login_required
def update_user_password():
    user_id = request.form.get('user_id')
    user = User.query.get(int(user_id))

    password1 = request.form.get("password1")
    password2 = request.form.get("password2")

    if password1 != password2:
        flash('Passwords do not match!', category='error')
    elif len(password1) < 7:
        flash('Password must be greater than 6 characters!', category='error')
    else:
        user.password = generate_password_hash(password1, method='sha256')
        db.session.commit()
        flash(user.first_name + " " + user.last_name + "'s password is updated!", category='success')
    return redirect(request.referrer)


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # For debugging POST requests
        # data = request.form
        # print(data)

        email = request.form.get('email').lower()
        first_name = request.form.get('firstName').lower()
        last_name = request.form.get('lastName').lower()
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        team = request.form.get('team')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 6 characters', category='error')
        elif team == "Select Team":
            flash('Please select a team.', category='error')
        else:
            user_name = first_name.title()[0] + last_name.title()
            new_user = User(email=email, user_name=user_name, first_name=first_name.title(), last_name=last_name.title(), team=team,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=False)
            flash('Account created!', category='success')

            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)