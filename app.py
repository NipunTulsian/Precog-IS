from flask import Flask
from config import Config
from models import db, Mentee, Mentor, Admin
from mail import mail
from auth_bp import auth_bp
from flask_login import LoginManager
from signup import signup_bp
from dashboard_bp import dashboard_bp
from register import register_bp

UPLOAD_FOLDER = 'uploads'

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config.from_object(Config)
    db.init_app(app)
    mail.init_app(app)
    
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        role, id = user_id.split("-")
        if(role=="mentor"):
            return Mentor.query.get(int(id))
        elif(role=="mentee"):
            return Mentee.query.get(int(id))
        elif(role=="admin"):
            return Admin.query.get(int(id))
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(signup_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(register_bp)
    with app.app_context():
        db.create_all()
    return app
