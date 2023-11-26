from flask import Blueprint, render_template, request, url_for, flash,redirect, abort
from flask_login import login_user, login_required, logout_user, current_user, confirm_login
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

from models import User
from config import bcrypt, db, app
from forms import RegistrationForm, LoginForm, UpdateProfileForm
from utils import uploadData

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
                        password = bcrypt.generate_password_hash(form.password.data),
                        pfp = app.config['PFP_UPLOADS'] +'/default.jpg'
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

@auth_bp.route('/edit/<int:user_id>', methods=["GET","POST"])
@login_required
def update_user(user_id):
    if current_user.id!=user_id:
        abort(403)
    form = UpdateProfileForm(obj=current_user)
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.password.data):
            user = User.query.filter_by(id=current_user.id).first()
            if current_user.first_name != form.first_name.data:
                new_fname = form.fname.data
                user.first_name = new_fname
                flash("First name updated sucessfully!")
            if current_user.last_name != form.last_name.data:
                new_lname = form.lname.data
                user.last_name = new_lname
                flash("Last name updated sucessfully!")
            if current_user.dob != form.dob.data:
                new_dob = form.dob.data
                user.dob = new_dob
                flash("Birth date updated sucessfully!")
            if form.img.data:
                new_path = uploadData(form.img.data, app.config['PFP_UPLOADS'], f'{current_user.id}.jpg')
                user.pfp = new_path
                flash("Profile picture updated sucessfully!")
            db.session.commit()
            # confirm_login()
            return redirect(url_for('auth.update_user', user_id=current_user.id))
            
        else:
            flash("Wrong password!")
            return redirect(url_for('auth.update_user', user_id=current_user.id))

    return render_template("auth/update_user.html", form=form)
    


@auth_bp.route('/logout')
@login_required
def logout():

    logout_user()
    flash("You have successfully logged out!")
    return redirect(url_for('auth.login'))