from flask_bcrypt import Bcrypt
from flask import Blueprint, render_template, request, url_for

auth_bp = Blueprint('auth', __name__)

from models import User
@auth_bp.route("/register", methods=["GET","POST"])
def register():
    if request.method == 'POST':
        email = request.forms.get("email")
        password = request.forms.get("password")
    return render_template('auth/register.html')

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=username).first()
        if user:
            if Bcrypt.check_password_hash(user.password, password):
                return 1
            else:
                return "Wrong password"
        else:
            return "User does not exists."
    return render_template('auth/login.html')

@auth_bp.route("/admin/login", methods=["GET","POST"])
def admin_login():
    if request.method == 'POST':
        user = User.query.filter_by(username=username).first()
        if user:
            if Bcrypt.check_password_hash(user.password, password):
                return 1
            else:
                return "Wrong password"
        else:
            return "User does not exists."
    return render_template('auth/admin.html')