from flask import Flask, render_template, url_for, redirect, request

from config import app
from auth import auth_bp
app.register_blueprint(auth_bp)


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
