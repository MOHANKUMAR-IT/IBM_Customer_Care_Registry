from flask import Flask, render_template, request, redirect, url_for, session ,flash,Blueprint

home_bp = Blueprint('home_bp',__name__,static_folder='static',static_url_path='/',template_folder='templates')


@home_bp.route('/',methods=['POST','GET'])
def home():
    if 'email_id' in request.form:
        return redirect(url_for('user_bp.register',email_id=request.form['email_id']))
    return render_template('home.html')