from flask import render_template
from . import auth_bp

@auth_bp.route('/login')
def login():
    return render_template('auth/login.html')

