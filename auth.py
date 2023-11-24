from flask import Blueprint, render_template, request, url_for, flash,redirect
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

from models import User
from config import bcrypt, db
from forms import RegistrationForm, LoginForm

@auth_bp.route("/register", methods=["GET","POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(email=form.email.data, 
                        first_name=form.fname.data, 
                        last_name=form.lname.data, 
                        dob=form.dob.data,
                        role="user", 
                        password = bcrypt.generate_password_hash(form.password.data)
                        )
            db.session.add(user)
            db.session.commit()

            login_user(user)
            return redirect(url_for('home'))
        
        except Exception as e:
            flash("Some error occured! Contact admin.")
            return redirect(url_for('auth.register'))

    return render_template("auth/register.html", form=form)

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash("Wrong password!")
                return redirect(url_for('auth.login'))
        else:
            flash("Sorry, we could not find your account.")
            return redirect(url_for('auth.login'))

    return render_template("auth/login.html", form=form)

@auth_bp.route("/admin/login", methods=["GET","POST"])
def admin_login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.role =='admin':
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for('home'))
                else:
                    flash("Wrong password!")
                    return redirect(url_for('auth.admin_login'))
            else:
                flash("access denied!")
                return redirect(url_for('auth.admin_login'))
        else:
            flash("Sorry, we could not find your account.")
            return redirect(url_for('auth.admin_login'))

    return render_template('auth/admin.html', form=form)

@auth_bp.route('/edit/<int:user_id>')
@login_required
def edit_user(user_id):
    form = RegistrationForm()
    


@auth_bp.route('/logout')
@login_required
def logout():

    logout_user()
    flash("You have successfully logged out!")
    return redirect(url_for('auth.login'))