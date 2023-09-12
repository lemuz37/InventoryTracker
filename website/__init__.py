from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import logging

SCRIPTS_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ksjxchalsikdjuhf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Devices

    with app.app_context():
        db.create_all()

    # Create folder for the log if it doesn't exist
    log_folder = os.path.join(os.path.dirname(SCRIPTS_FOLDER_PATH), "Log")
    if not os.path.exists(log_folder):
        os.mkdir(log_folder)

    # Configure the logging system and mark the beginning of the log file
    log_file = os.path.join(log_folder, "Inventory_Tracking_Tool.log")
    logging.basicConfig(
        filename=log_file,
        encoding='utf-8',
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Suppress Werkzeug's logs by adjusting its logging level
    # werkzeug_logger = logging.getLogger('werkzeug')
    # werkzeug_logger.setLevel(logging.ERROR)

    # Log your custom message
    logging.info("----- Midmark Inventory Tracking System -----\n\n")
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
