from flask_bcrypt import Bcrypt
from flask import Blueprint, render_template, request, url_for, flash
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
        dob = datetime.strptime(dob, '%Y-%m-%d').date()
        if User.query.filter_by(email=email).first():
            return "User already exists!"

        else:
            try:
                print(dob)
                print(bcrypt.generate_password_hash(password))
                user = User(email=email, 
                            first_name=first, 
                            last_name=last, 
                            dob=dob,
                            role="user", 
                            password = bcrypt.generate_password_hash(password)
                            )
                db.session.add(user)
                db.session.commit()
                print(1)
                return url_for("login")
            except Exception as e:
                print(e)
                return "Unsuccessful"

    return render_template('auth/register.html')

@auth_bp.route("/login", methods=["GET","POST"])
def login():

    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            if bcrypt.check_password_hash(user.password, password):
                return "Login successful"
            else:
                return "Wrong password"
        else:
            return "User does not exists."

    return render_template('auth/login.html')

@auth_bp.route("/admin/login", methods=["GET","POST"])
def admin_login():

    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            if Bcrypt.check_password_hash(user.password, password):
                return flash("Login successful")
            else:
                return "Wrong password"
        else:
            return "User does not exists."

    return render_template('auth/admin.html')