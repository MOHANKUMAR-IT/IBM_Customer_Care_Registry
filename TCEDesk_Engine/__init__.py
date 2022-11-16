from flask import Flask


from .Profile.routes import profile_bp
from .User.routes import user_bp
from .Agent.routes import agent_bp
from .Admin.routes import admin_bp
from .home.routes import home_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "StrongPixel1090"
    app.config['SESSION_TYPE'] = 'filesystem'

    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(agent_bp, url_prefix='/agent')
    app.register_blueprint(admin_bp,url_prefix='/admin')
    app.register_blueprint(home_bp,url_prefix='/')

    return app


