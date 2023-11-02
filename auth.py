from models import User
from flask_bcrypt import Bcrypt

def register():
    email = request.forms.get("email")
def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        if Bcrypt.check_password_hash(user.password, password):
            return 1
        else:
            return "Wrong password"
    else:
        return "User does not exists."
