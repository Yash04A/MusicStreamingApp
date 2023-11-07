from models import User
from flask_bcrypt import Bcrypt
from flask import Blueprint, render_template, request, url_for

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", method=["GET","POST"])
def register():
    if request.method == 'POST':
        email = request.forms.get("email")
        password = request.forms.get("password")
    return render_template(url_for('register.html'))

@auth_bp.route("/login", method=["GET","POST"])
def login(username, password):
    if request.method == 'POST':
        user = User.query.filter_by(username=username).first()
        if user:
            if Bcrypt.check_password_hash(user.password, password):
                return 1
            else:
                return "Wrong password"
        else:
            return "User does not exists."
