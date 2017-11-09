from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bootstrap import Bootstrap
from config import config
from flask_moment import Moment
from flask_login import LoginManager
import eventlet
from device_mng import socketio
from flask_redis import FlaskRedis

redis_conn = FlaskRedis()
bootstrap = Bootstrap()
moment = Moment()

eventlet.monkey_patch()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    socketio.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    redis_conn.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .device import device as devices_blueprint
    app.register_blueprint(devices_blueprint, url_prefix='/device')

    return app