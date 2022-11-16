from flask import Flask, render_template, request, redirect, url_for, session ,flash,Blueprint

home_bp = Blueprint('home_bp',__name__,static_folder='static',static_url_path='/',template_folder='templates')


@home_bp.route('/',methods=['POST','GET'])
def home():
    return render_template('home.html')