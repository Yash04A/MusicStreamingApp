from flask import Flask, render_template, url_for, redirect, request
from flask_login import login_required
from config import app,db
from auth import auth_bp
app.register_blueprint(auth_bp)


@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template("home.html")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
