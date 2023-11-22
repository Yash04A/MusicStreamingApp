from flask_bcrypt import Bcrypt
from flask import Blueprint, render_template, request, url_for, flash,redirect, session
from flask_login import login_user, login_required, logout_user
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

from models import User
from config import bcrypt, db

@auth_bp.route("/register", methods=["GET","POST"])
def register():

    if request.method == 'POST':
        email = request.form.get("email")
        first = request.form.get("fname")
        last = request.form.get("lname")
        dob = request.form.get("dob")
        password = request.form.get("password")

        if dob:
            dob = datetime.strptime(dob, '%Y-%m-%d').date() 
        else:
            dob=None

        if User.query.filter_by(email=email).first():
            flash("User already exists! Try different email?")
            return redirect('/register')
        
        elif len(password)<8:
            flash("Password should be at least 8 characters.")
            return redirect('/register')
        else:
            try:
                user = User(email=email, 
                            first_name=first, 
                            last_name=last, 
                            dob=dob,
                            role="user", 
                            password = bcrypt.generate_password_hash(password)
                            )
                db.session.add(user)
                db.session.commit()

                login_user(user)
                return redirect('/')
            
            except Exception as e:
                flash("Some error occured! Contact admin.")
                return redirect('/register')

    return render_template('auth/register.html')

@auth_bp.route("/login", methods=["GET","POST"])
def login():

    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect('/')
            else:
                flash("Wrong password!")
                return redirect('/login')
        else:
            flash("Sorry, we could not find your account.")
            return redirect('/login')

    return render_template('auth/login.html')

@auth_bp.route("/admin/login", methods=["GET","POST"])
def admin_login():

    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if user.role =='admin':
                if bcrypt.check_password_hash(user.password, password):
                    login_user(user)
                    return redirect('/')
                else:
                    flash("Wrong password!")
                    return redirect('/login')
            else:
                flash("access denied!")
                return redirect('/login')
        else:
            flash("Sorry, we could not find your account.")
            return redirect('/login')

    return render_template('auth/admin.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect('/')